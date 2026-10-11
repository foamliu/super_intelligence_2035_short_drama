#!/usr/bin/env python3
"""EP13 成片字幕：生成中英双语 .srt + 烧录硬字幕成片。

输入  : OUTPUT/13_外骨骼/EP13_外骨骼_成片_v2.mp4（已有旁白音轨）
输出  : OUTPUT/13_外骨骼/EP13_外骨骼_字幕.srt
        OUTPUT/13_外骨骼/EP13_外骨骼_成片_v3_字幕.mp4（硬字幕 + 原音轨）

台词时间轴与 scripts/synth_ep13.py 的 TTS_CUES 完全一致；
每条台词的中文原文取自 scripts/gen_ep13_tts.py（Sarah 1301 / 师兄 1303）。
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EP = ROOT / "OUTPUT" / "13_外骨骼"
AUD = EP / "audio"
SRC = EP / "EP13_外骨骼_成片_v2.mp4"
SRT = EP / "EP13_外骨骼_字幕.srt"
DST = EP / "EP13_外骨骼_成片_v3_字幕.mp4"

# 每镜：起始秒、TTS 音频文件、中文分段、英文分段（zh/en 段数一致）
# 分段按「句号 / 逗号 / 破折号」切，便于 libass 自动换行。
CUES = [
    {
        "start": 0.00,
        "audio": "13_tts_sarah_02_desk.flac",
        "zh": [
            "你知道外骨骼的定义是什么吗？",
            "不是让你变得更强——是帮你做你做不了的事。",
            "我训练了一个 AI，来看观众的表情、微动作、笑声强度。",
            "它帮我优化段子——实时分析哪里该停顿、哪里该加速。",
            "我管它叫外骨骼——帮我在台上站住。",
        ],
        "en": [
            "Do you know what an exoskeleton is?",
            "It's not about making you stronger — it's about helping you do what you can't do alone.",
            "I trained an AI to read the audience's expressions, micro-movements, and laughter intensity.",
            "It helps me refine my jokes — analyzing in real time where to pause, where to speed up.",
            "I call it my exoskeleton — it keeps me standing on stage.",
        ],
    },
    {
        "start": 18.19,
        "audio": "13_tts_shixiong_01_hefa.flac",
        "zh": ["合法吗？"],
        "en": ["Is it legal?"],
    },
    {
        "start": 19.87,
        "audio": "13_tts_shixiong_02_code.flac",
        "zh": ["你别把我的代码写进段子里。"],
        "en": ["Don't put my code in your jokes."],
    },
    {
        "start": 22.99,
        "audio": "13_tts_shixiong_03_bracket.flac",
        "zh": ["第 147 行，括号错了。", "那是真的。真的才好笑。"],
        "en": ["Line 147, the bracket is wrong.", "That's true. It's only funny if it's true."],
    },
    {
        "start": 70.79,
        "audio": "13_tts_sarah_05_hao.flac",
        "zh": ["好。"],
        "en": ["Okay."],
    },
    {
        "start": 80.85,
        "audio": "13_tts_sarah_04_bar.flac",
        "zh": [
            "他说，你今晚讲的不像脱口秀。",
            "像你在公司没说完的话。",
            "我说对。脱口秀，本来就是把公司里不能说的话，换个地方说出来。",
        ],
        "en": [
            "He said, tonight you weren't doing stand-up.",
            "It sounded like the things you never got to say at work.",
            "I said, exactly. Stand-up is just saying what you can't say at work — somewhere else.",
        ],
    },
]


def probe_dur(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    try:
        return float(r.stdout.strip())
    except Exception:
        return 3.0


def fmt_ts(sec: float) -> str:
    sec = max(0.0, sec)
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(video_dur: float):
    entries = []
    n = len(CUES)
    for i, cue in enumerate(CUES):
        start = cue["start"]
        # 台词实际时长 = 音频时长；与下一条起点留 0.2s 空隙；不超过成片尾
        audio_dur = probe_dur(AUD / cue["audio"])
        next_start = CUES[i + 1]["start"] if i + 1 < n else video_dur
        total = max(0.4, min(audio_dur, next_start - start - 0.2))
        total = min(total, video_dur - start)

        zh = cue["zh"]
        en = cue["en"]
        weights = [len(s) for s in zh]
        wsum = sum(weights) or 1
        t = start
        for j, (z, e) in enumerate(zip(zh, en)):
            seg_dur = total * weights[j] / wsum
            end = t + seg_dur
            entries.append((t, end, f"{z}\n{e}"))
            t = end
    return entries


def write_srt(entries, path: Path):
    lines = []
    for idx, (start, end, text) in enumerate(entries, 1):
        lines.append(str(idx))
        lines.append(f"{fmt_ts(start)} --> {fmt_ts(end)}")
        lines.append(text)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    if not SRC.exists():
        print(f"缺输入成片: {SRC}")
        return
    video_dur = probe_dur(SRC)
    print(f"输入成片: {SRC.name} ({video_dur:.2f}s)")

    entries = build_srt(video_dur)
    write_srt(entries, SRT)
    print(f"字幕已写: {SRT.name} ({len(entries)} 条)")

    # 烧录硬字幕（libass + 微软雅黑），保留原音轨
    vf = (
        f"subtitles={SRT.name}"
        f":fontsdir='C\\:/Windows/Fonts'"
        f":force_style='FontName=Microsoft YaHei,FontSize=21,"
        f"PrimaryColour=&H00FFFFFF,OutlineColour=&H90000000,"
        f"BorderStyle=1,Outline=2,Shadow=0,MarginV=30'"
    )
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", SRC.name, "-vf", vf,
         "-c:v", "libx264", "-crf", "18", "-preset", "fast",
         "-c:a", "copy", DST.name],
        cwd=str(EP), capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if DST.exists() and DST.stat().st_size > 0:
        d = probe_dur(DST)
        mb = DST.stat().st_size / 1024 / 1024
        print(f"✅ 硬字幕成片: {DST.name} ({d:.2f}s, {mb:.1f}MB)")
    else:
        print("❌ 烧录失败:\n", r.stderr[-1500:])


if __name__ == "__main__":
    main()
