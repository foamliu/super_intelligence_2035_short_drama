# -*- coding: utf-8 -*-
"""第18集《暖阳》配乐混音 —— 把纯器乐 BGM 铺进成片（**混音**，不替换画面/环境音）。

★ 本集特殊点（任务书 §4.5）：**无对白（TTS 禁用）**，叙事靠「影像 + 硬字幕 + 环境音
  + 纯器乐配乐」。画面自带音轨（H3 环境音，≈ −50 dBFS，README §4.4）几乎无声，
  配乐是唯一的主导音频层 —— 混音 = 「配乐打到舒适电平 + 环境音垫底」。

★ 铁律（沿用 stem_fest `_mix_bgm.py` 的成熟配方）：
  1. **只动音频，画面不动**：`-c:v copy` 直通 ⇒ 1056×608 / 24fps 画面零代际损失。
  2. **必须混音，不能替换**：成片音轨是 H3 环境音，替换掉等于全片哑掉。
  3. **电平三重保险**：① BGM 先降 `--level`；② `sidechaincompress` 用成片音轨当
     侧链闪避（本集侧链接近静默 ⇒ 实际不闪避，但保留以防未来叠人声）；
     ③ 总线上 `alimiter`（−1 dBFS 真峰守门）。
  4. **循环用 `acrossfade`**：60s 大提琴主题铺满 273s 需多段，交叉淡化接缝无痕。
  5. **产物另存**，绝不覆盖 `EP18_暖阳_成片.mp4`（保留无配乐母版，随时重铺）。

用法：
    py -3.10 scripts/mix_ep18_bgm.py                     # 默认：大提琴铺满全片
    py -3.10 scripts/mix_ep18_bgm.py --bgm 02            # 换数据流主题
    py -3.10 scripts/mix_ep18_bgm.py --level=-11         # 配乐更轻
    py -3.10 scripts/mix_ep18_bgm.py --dry-run           # 只打印滤镜图与命令
"""

import argparse
import json
import os
import subprocess
import sys

for _s in ("stdout", "stderr"):
    try:
        getattr(sys, _s).reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "OUTPUT", "18_暖阳")
AUDIO = os.path.join(OUT, "audio")
VIDEO = os.path.join(OUT, "videos")
TMP = os.path.join(VIDEO, "_mixbgm")

FILM = os.path.join(VIDEO, "EP18_暖阳_成片.mp4")
BGMS = {
    "01": os.path.join(AUDIO, "ep18_bgm_01_cello_00001.mp3"),
    "02": os.path.join(AUDIO, "ep18_bgm_02_datastream_00001.mp3"),
    "03": os.path.join(AUDIO, "ep18_bgm_03_finale_00001.mp3"),
}

SR = 48000
AC = 2
XFADE = 2.0
FADE_IN = 1.5
FADE_OUT = 4.0


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def probe(path, *entries):
    cmd = ["ffprobe", "-v", "error", "-print_format", "json"]
    for e in entries:
        cmd += ["-show_entries", e]
    cmd += [path]
    r = run(cmd)
    try:
        return json.loads(r.stdout or "{}")
    except ValueError:
        return {}


def durations(path):
    d = probe(path, "format=duration",
              "stream=codec_type,duration,nb_frames,avg_frame_rate")
    v = a = None
    for s in d.get("streams", []):
        try:
            dur = float(s.get("duration") or 0)
        except (TypeError, ValueError):
            dur = 0.0
        if s.get("codec_type") == "video":
            n, fr = s.get("nb_frames"), s.get("avg_frame_rate") or "0/0"
            if n and fr and fr != "0/0":
                num, den = fr.split("/")
                if float(den):
                    dur = float(n) * float(den) / float(num)
            v = dur
        elif s.get("codec_type") == "audio":
            a = dur
    f = float(d.get("format", {}).get("duration") or 0)
    return v or f, a or f, f


def song_body(path):
    r = run(["ffmpeg", "-nostats", "-v", "info", "-i", path, "-af",
             "silencedetect=n=-45dB:d=0.5", "-vn", "-f", "null", "-"])
    log = (r.stderr or "") + (r.stdout or "")
    starts, ends = [], []
    for line in log.splitlines():
        if "silence_start:" in line:
            try:
                starts.append(float(line.split("silence_start:")[1].split()[0]))
            except (IndexError, ValueError):
                pass
        elif "silence_end:" in line:
            try:
                ends.append(float(line.split("silence_end:")[1].split()[0]))
            except (IndexError, ValueError):
                pass
    all_d = durations(path)[0]
    b0 = ends[0] if starts and starts[0] <= 0.01 and ends else 0.0
    b1 = starts[-1] if starts and starts[-1] > (b0 + 1) else all_d
    return b0, b1, b1 - b0


def seg_count(need, body, xfade):
    if need <= body - 0.05:
        return 1
    n = 2
    while n * body - (n - 1) * xfade < need:
        n += 1
    return n
def build_filtergraph(film_dur, need, body, level_db, duck, start,
                      fade_out, fade_in, xfade, film_dip):
    """滤镜图：n 段 BGM → acrossfade 循环 → 铺到区间 → 闪避混音 → 限幅。"""
    fmt = ("aresample=%d,aformat=sample_fmts=fltp:sample_rates=%d:"
           "channel_layouts=stereo" % (SR, SR))
    n = seg_count(need, body, xfade)
    ln = need if n == 1 else body

    chains = []
    for i in range(n):
        chains.append("[%d:a]%s,atrim=0:%.3f,asetpts=N/SR/TB[s%d]"
                      % (i + 1, fmt, ln, i))
    if n == 1:
        chains.append("[s0]anull[bed]")
    else:
        prev = "[s0]"
        for i in range(1, n):
            tag = "[bed]" if i == n - 1 else "[x%d]" % i
            chains.append("%s[s%d]acrossfade=d=%.2f:c1=tri:c2=tri%s"
                          % (prev, i, xfade, tag))
            prev = tag

    fade = ""
    if fade_in > 0:
        fade += ",afade=t=in:st=0:d=%.2f" % fade_in
    if 0 < fade_out < need:
        fade += ",afade=t=out:st=%.3f:d=%.2f" % (need - fade_out, fade_out)
    chains.append("[bed]atrim=0:%.3f,asetpts=N/SR/TB%s,volume=%.1fdB[bedv]"
                  % (need, fade, level_db))

    bed = "[bedv]"
    if start > 0.001:
        chains.append("[bedv]adelay=%d:all=1[bedd0]" % int(round(start * 1000)))
        bed = "[bedd0]"

    # 成片音轨（裁到画面时长，去掉音频尾巴；主干轨归一到 -23 LUFS）
    film_gain = "" if abs(film_dip) < 0.01 else ",volume=%.1fdB" % film_dip
    chains.append("[0:a]%s,atrim=0:%.3f,asetpts=N/SR/TB%s[F]"
                  % (fmt, film_dur, film_gain))

    # 闪避（用画面音轨当侧链）+ 相加 + 限幅
    if duck:
        chains.append("[F]asplit=2[Fmain][Fsc]")
        chains.append("%s[Fsc]sidechaincompress=threshold=0.05:ratio=8:"
                      "attack=20:release=600:makeup=1[bedc]" % bed)
        bgm_in = "[bedc]"
    else:
        chains.append("[F]anull[Fmain]")
        bgm_in = bed
    chains.append("[Fmain]%samix=inputs=2:duration=first:"
                  "dropout_transition=0:normalize=0[mix]" % bgm_in)
    chains.append("[mix]alimiter=limit=0.891:level=0:attack=5:release=50[aout]")
    return ";\n".join(chains), n


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》配乐混音")
    ap.add_argument("--bgm", choices=["01", "02", "03"], default="01",
                    help="铺哪首配乐（01 大提琴主主题 / 02 数据流 / 03 尾声钢琴）")
    ap.add_argument("--level", type=float, default=-12.0,
                    help="BGM 相对电平 dB（越负越轻；大提琴 -16 LUFS → -12 命中 -28 LUFS）")
    ap.add_argument("--film-dip", type=float, default=-9.6,
                    help="主干轨（H3 音轨）压低 dB（-13.4 LUFS → -9.6 命中 -23 LUFS）")
    ap.add_argument("--start", type=float, default=0.0, help="BGM 起点（秒）")
    ap.add_argument("--end", type=float, default=0.0, help="BGM 终点（0=片尾）")
    ap.add_argument("--fade-in", type=float, default=FADE_IN)
    ap.add_argument("--fade-out", type=float, default=FADE_OUT)
    ap.add_argument("--xfade", type=float, default=XFADE)
    ap.add_argument("--no-duck", action="store_true", help="关侧链闪避")
    ap.add_argument("--dry-run", action="store_true", help="只打印，不执行")
    a = ap.parse_args()

    song = BGMS[a.bgm]
    out = os.path.join(VIDEO, "EP18_暖阳_成片_BGM%s.mp4" % a.bgm)
    for p, what in ((FILM, "成片"), (song, "配乐")):
        if not os.path.exists(p):
            print("找不到%s：%s" % (what, p))
            return 1

    film_dur, film_a_dur, _ = durations(FILM)
    b0, b1, body = song_body(song)
    end = a.end if a.end > 0 else film_dur
    need = end - a.start
    print("成片          画面 %.3f s / 音轨 %.3f s" % (film_dur, film_a_dur))
    print("配乐          正文 %.3f–%.3f s（%.3f s；首尾静音已排除）"
          % (b0, b1, body))
    print("BGM 区间      %.3f–%.3f s（%.3f s）  电平 %+.1f dB  闪避 %s  主干压低 %+.1f dB"
          % (a.start, end, need, a.level, "关" if a.no_duck else "开", a.film_dip))
    if need <= 0:
        print("BGM 区间长度必须为正")
        return 1

    fc, nseg = build_filtergraph(film_dur, need, body, a.level, not a.no_duck,
                                 a.start, a.fade_out, a.fade_in, a.xfade,
                                 a.film_dip)
    os.makedirs(TMP, exist_ok=True)
    fcfile = os.path.join(TMP, "filtergraph_bgm%s.txt" % a.bgm)
    with open(fcfile, "w", encoding="utf-8") as f:
        f.write(fc)
    print("BGM 循环      %d 段（交叉淡化 %.1f s）→ 滤镜图 %.1f KB 走文件"
          % (nseg, a.xfade, len(fc) / 1024.0))

    cmd = (["ffmpeg", "-y", "-v", "error", "-i", FILM] + ["-i", song] * nseg +
           ["-filter_complex_script", fcfile, "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-ar", str(SR), "-ac", str(AC), "-movflags", "+faststart", out])
    if a.dry_run:
        print("\n滤镜图 → %s\n\n%s\n\n命令：\n%s"
              % (fcfile, fc, " ".join(cmd)))
        return 0

    print("混音中（画面直通 copy，只重编码音轨）…")
    r = run(cmd)
    if r.returncode != 0:
        print("混音失败：\n%s" % (r.stderr or "")[:2000])
        return 1

    v, au, _ = durations(out)
    print("✅ 已出 %s" % out)
    print("   时长：画面 %.3f s / 音轨 %.3f s（差 %+.3f s） / %.1f MB"
          % (v, au, au - v, os.path.getsize(out) / 1e6))
    r = run(["ffmpeg", "-nostats", "-v", "info", "-i", out,
             "-filter_complex", "ebur128=peak=true", "-f", "null", "-"])
    for line in ((r.stderr or "") + (r.stdout or "")).splitlines():
        s = line.strip()
        if s.startswith("I:") or s.startswith("LRA:") or s.startswith("Peak:"):
            print("   %s" % s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
