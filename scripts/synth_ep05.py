#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第05集《临界点》成片合成：55 镜 concat（★音画钉长）+ 硬字幕烧录。

铁律（任务书 §4.7 / STEM_FEST_PLAYBOOK §7）：
- `帧数 ÷ 24` 是画面的权威时间轴；每段音频必须被钉到它：
  `aresample=32000,aformat=channel_layouts=stereo,apad,atrim=0:<本镜时长>,asetpts=N/SR/TB`
- 🚫 禁用 `-shortest`（实测砍的是视频）；🚫 禁用 TTS（人声已在视频轨内，不叠）。
- 拼接后闸门：|音轨长度 − 画面长度| < 0.15s（必要非充分，还需逐镜测内容偏移）。

用法:
  python scripts/synth_ep05.py --dry-run   # 仅列出 55 镜文件/时长/缺漏
  python scripts/synth_ep05.py             # 拼接 master + （若 SRT 在）烧硬字幕
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "OUTPUT" / "05_临界点" / "videos"
SRT = OUT / "EP05_临界点_字幕.srt"
MASTER = OUT / "EP05_临界点_master.mp4"
FINAL = OUT / "EP05_临界点_成片.mp4"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_ep05_h3_r2v import SHOTS as R2V_SHOTS  # noqa: E402
from gen_ep05_h3_t2v import SHOTS as T2V_SHOTS  # noqa: E402

ALL = {s["shot"]: s for s in R2V_SHOTS + T2V_SHOTS}


def h3_dur_sec(dur: float) -> float:
    """H3 帧数量化 `17k+5` 后的实际播放时长（= 帧数/24，画面权威时间轴）。"""
    raw = max(5, round(dur * 24))
    frames = raw + (5 - (raw % 17)) % 17
    return frames / 24.0


def resolve(shot: str):
    """返回该镜 mp4（R2V 或 T2V），缺失返回 None。"""
    hits = sorted(OUT.glob(f"EP05_SHOT-{shot}_H3_*.mp4"))
    return hits[0] if hits else None


def ffprobe(args, path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", *args, str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def build_concat_cmd(order):
    """构造 ffmpeg concat filter_complex（55 输入，音频逐段钉长）。"""
    n = len(order)
    parts = []
    for i, (shot, path) in enumerate(order):
        dur = h3_dur_sec(ALL[shot]["dur"])
        parts.append(f"[{i}:v]scale=1280:720:flags=lanczos,setsar=1,"
                     f"settb=AVTB,setpts=PTS-STARTPTS[v{i}]")
        parts.append(
            f"[{i}:a]aresample=32000,aformat=channel_layouts=stereo,"
            f"apad,atrim=0:{dur:.3f},asetpts=N/SR/TB[a{i}]"
        )
    concat_inputs = "".join(f"[v{i}][a{i}]" for i in range(n))
    fc = ";".join(parts) + f";{concat_inputs}concat=n={n}:v=1:a=1[v][a]"

    cmd = ["ffmpeg", "-y"]
    for _shot, path in order:
        cmd += ["-i", str(path)]
    cmd += [
        "-filter_complex", fc,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        str(MASTER),
    ]
    return cmd


def burn_subs():
    """硬字幕烧录（libass + 微软雅黑），保原音轨。

    ★ 踩坑（2026-10-18）：`fontsdir='C:/Windows/Fonts'` 里的冒号会破坏 ffmpeg
    subtitles 滤镜的选项解析（报 `No option name near '/Windows/Fonts'`）⇒ 一律
    不传 fontsdir，依赖 libass 走系统字体目录；中文 SRT 文件名也先复制成 ASCII
    名 `ep05_sub.srt`，规避滤镜解析里非 ASCII 路径的坑。
    """
    ascii_srt = OUT / "ep05_sub.srt"
    shutil.copyfile(SRT, ascii_srt)
    vf = (
        "subtitles=ep05_sub.srt"
        ":force_style='FontName=Microsoft YaHei,FontSize=21,"
        "PrimaryColour=&H00FFFFFF,OutlineColour=&H90000000,"
        "BorderStyle=1,Outline=2,Shadow=0,MarginV=30'"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", "EP05_临界点_master.mp4", "-vf", vf,
         "-c:v", "libx264", "-crf", "18", "-preset", "fast",
         "-c:a", "copy", "EP05_临界点_成片.mp4"],
        cwd=str(OUT), capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if FINAL.exists() and FINAL.stat().st_size > 0:
        d = ffprobe(["-show_entries", "format=duration", "-of", "csv=p=0"], FINAL)
        mb = FINAL.stat().st_size / 1024 / 1024
        print(f"✅ 硬字幕成片: {FINAL.name} ({d:.2f}s, {mb:.1f}MB)")
    else:
        print("❌ 字幕烧录失败")


def main():
    ap = argparse.ArgumentParser(description="第05集《临界点》成片合成")
    ap.add_argument("--dry-run", action="store_true", help="仅列出计划，不拼接")
    args = ap.parse_args()

    order = []          # [(shot, path)]
    missing = []
    total = 0.0
    for shot in sorted(ALL.keys(), key=int):
        path = resolve(shot)
        dur = h3_dur_sec(ALL[shot]["dur"])
        if path:
            order.append((shot, path))
            total += dur
        else:
            missing.append(shot)

    print("=" * 66)
    print(f" EP05《临界点》合成  |  {len(order)}/{len(ALL)} 镜在位  |  预计 {total:.2f}s")
    print("=" * 66)
    for shot, path in order:
        print(f"  SHOT-{shot:>2}  {path.name}  ({h3_dur_sec(ALL[shot]['dur']):.3f}s)")
    if missing:
        print(f"\n⚠️ 缺 {len(missing)} 镜: {', '.join(missing)}")
    if args.dry_run:
        print("\n[Dry-run] 未拼接。")
        return

    if missing:
        print("❌ 有缺镜，中止拼接（先补齐 R2V/T2V 缺失镜）。")
        return

    print("\n=== 1. 拼接 master（★音画钉长）===")
    cmd = build_concat_cmd(order)
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if not MASTER.exists() or MASTER.stat().st_size == 0:
        print("❌ 拼接失败:\n", r.stderr[-1500:])
        return

    vd = ffprobe(["-select_streams", "v:0", "-show_entries",
                  "stream=duration", "-of", "csv=p=0"], MASTER)
    ad = ffprobe(["-select_streams", "a:0", "-show_entries",
                  "stream=duration", "-of", "csv=p=0"], MASTER)
    drift = abs(ad - vd)
    print(f"   master: 视频 {vd:.3f}s / 音轨 {ad:.3f}s / 漂移 {drift:.3f}s")
    if drift >= 0.15:
        print(f"❌ 闸门未过：|音轨−画面| = {drift:.3f}s ≥ 0.15s（音画漂移铁律 §4.7）")
        return
    print(f"   ✅ 闸门通过（{drift:.3f}s < 0.15s）")

    if SRT.exists():
        print("\n=== 2. 硬字幕烧录 ===")
        burn_subs()
    else:
        print(f"\n⚠️ 无字幕文件 {SRT.name}，跳过烧录（先跑 gen_ep05_subtitles.py）。")


if __name__ == "__main__":
    main()
