#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第02集《经验》字幕生成：从各镜 H3 prompt 的 `Audio:` 提取台词 → 中文字幕 .srt。

- 时间轴 = 逐镜镜头时长（H3 `17k+5` 帧量化，任务书 §4.1）
- 台词 = 各镜 prompt 里 `Audio:` 字段的中文原文（台词**随 H3 生成**，🚫 禁用 TTS）
- ★ 无台词镜（`Audio:` 为中文音景描述，如「机台低鸣与洁净室通风底噪」）用 `SFX_ONLY`
  显式排除，🚫 不做「含中文即当台词」的启发式（会把音景描述误提成字幕）。
- 本集无「纯屏幕文字 / 收尾字幕」镜（台词均随 H3 出在音轨里）⇒ `CAPTION = {}`。
- 中文单语字幕（对齐本仓 EP01/EP18 口径）。

用法:
  python scripts/gen_ep02_subtitles.py --dry-run   # 仅打印字幕预览（镜号/起止/文本）
  python scripts/gen_ep02_subtitles.py             # 生成 .srt
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "OUTPUT" / "02_经验" / "videos"
SRT = OUT / "EP02_经验_字幕.srt"

# 复用两个生成脚本的 SHOTS（台词权威 = H3 prompt 的 Audio: 字段）
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_ep02_h3_r2v import SHOTS as R2V_SHOTS  # noqa: E402
from gen_ep02_h3_t2v import SHOTS as T2V_SHOTS  # noqa: E402

ALL = {s["shot"]: s for s in R2V_SHOTS + T2V_SHOTS}

# 无台词镜（Audio: 为纯音景描述，H3 不出人声）—— 与 `SCENES/02_经验.md` 逐镜表
# 「台词/音效」列核对一致（标「音效（后期）」的镜均在此列）。
SFX_ONLY = {"01", "14", "26", "34", "36", "41", "50", "51"}

# 纯字幕（后期 · 不在 H3 音轨里）：shot → 屏幕文字。本集无此镜。
CAPTION = {}

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
# 按句末标点切段（保标点），长句再按逗号/破折号切
SPLIT_RE = re.compile(r"([^。！？；!?;]*[。！？；!?;])")


def h3_dur_sec(dur: float) -> float:
    """H3 帧数量化 `17k+5` 后的实际播放时长（= 帧数/24，画面权威时间轴）。"""
    raw = max(5, round(dur * 24))
    frames = raw + (5 - (raw % 17)) % 17
    return frames / 24.0


def extract_dialogue(prompt: str) -> str:
    """提取 prompt 里 `Audio:` 字段的中文台词；无中文（纯音景）→ 空串。"""
    m = re.search(r"Audio:\s*(.*)$", prompt, flags=re.S)
    return m.group(1).strip() if m else ""


def split_segments(text: str) -> list:
    """把一句台词切成可读的分段（句末标点优先，长段再按逗号/破折号切）。"""
    parts = [p for p in SPLIT_RE.split(text) if p and p.strip()]
    segs = []
    for p in parts:
        if len(p) > 20:
            # 长段按逗号/破折号/冒号进一步切，保标点
            sub = re.split(r"(?<=[，,、：:—])", p)
            sub = [s for s in sub if s and s.strip()]
            segs.extend(sub)
        else:
            segs.append(p)
    # 合并「纯标点」分段到前一段（避免出现单独的「—」字幕条）
    merged = []
    for s in segs:
        if merged and not CJK_RE.search(s):
            merged[-1] += s
        else:
            merged.append(s)
    return [s for s in merged if s.strip()]


def fmt_ts(sec: float) -> str:
    sec = max(0.0, sec)
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_entries():
    """返回 [(start, end, text, shot), ...] 与全片总时长。"""
    entries = []
    t = 0.0
    for shot in sorted(ALL.keys(), key=int):
        s = ALL[shot]
        dur = h3_dur_sec(s["dur"])
        if shot in CAPTION:
            text = CAPTION[shot]
        elif shot not in SFX_ONLY:
            text = extract_dialogue(s["prompt"])
        else:
            text = ""
        if text:
            segs = split_segments(text)
            weights = [len(x) for x in segs]
            wsum = sum(weights) or 1
            seg_t = t
            for seg, w in zip(segs, weights):
                seg_dur = dur * w / wsum
                entries.append((seg_t, seg_t + seg_dur, seg, shot))
                seg_t += seg_dur
        t += dur
    return entries, t


def write_srt(entries, path: Path):
    lines = []
    for idx, (start, end, text, _shot) in enumerate(entries, 1):
        lines.append(str(idx))
        lines.append(f"{fmt_ts(start)} --> {fmt_ts(end)}")
        lines.append(text)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="第02集《经验》字幕生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印预览")
    args = ap.parse_args()

    entries, total = build_entries()
    print(f"EP02《经验》字幕  |  {len(entries)} 条  |  全片 {total:.2f}s")
    print("=" * 66)
    for start, end, text, shot in entries:
        print(f"  SHOT-{shot:>2}  {fmt_ts(start)} -> {fmt_ts(end)}  {text}")
    if args.dry_run:
        print(f"\n[Dry-run] 未写文件。目标: {SRT}")
        return
    write_srt(entries, SRT)
    print(f"\n✅ 字幕已写: {SRT}（{len(entries)} 条）")


if __name__ == "__main__":
    main()
