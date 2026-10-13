#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第13集《外骨骼》成片字幕：中英双语 .srt（去 TTS · 时间轴来自逐镜 17k+5 帧量化）。

推翻旧法（2026-10-12 用户令）：
- 旧版依赖 TTS 音频时长（`13_tts_*.flac`）+ 旧成片 v2/v3 文件名 —— 全部作废。
- 新版：台词随 MiniMax H3 一起生成（写进各镜 prompt 的 `Audio:`），字幕时间轴
  **由逐镜时长推得**（`h3_dur_sec` 累积），不再依赖任何 TTS 音频文件。

- 台词权威：`SCENES/13_外骨骼.md` 的 `## 逐镜表`「台词/音效」列（H3 只讲 L1 台词原文）。
- 无台词镜（纯音效：01/02/08/29/43）不生成对白字幕；镜 48 片尾文案按 `CAPTION` 单独烧录。

用法:
  python scripts/gen_ep13_subtitles.py --dry-run   # 仅打印字幕计划
  python scripts/gen_ep13_subtitles.py             # 生成 .srt（硬字幕烧录由 synth_ep13.py 做）
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "OUTPUT" / "13_外骨骼" / "videos"
SRT = OUT / "EP13_外骨骼_字幕.srt"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_ep13_h3_r2v import SHOTS as R2V_SHOTS  # noqa: E402
from gen_ep13_h3_t2v import SHOTS as T2V_SHOTS  # noqa: E402

ALL = {s["shot"]: s for s in R2V_SHOTS + T2V_SHOTS}


def h3_dur_sec(dur: float) -> float:
    """H3 帧数量化 `17k+5` 后的实际播放时长（= 帧数/24，画面权威时间轴）。"""
    raw = max(5, round(dur * 24))
    frames = raw + (5 - (raw % 17)) % 17
    return frames / 24.0


# 对白字幕（中英双语）：shot → [(zh, en), ...]（按句切分、一一对齐）。
# 台词原文与 gen_ep13_h3_{r2v,t2v}.py 各镜 prompt 的 `Audio:` 段逐字一致。
DIALOGUE = {
    "03": [("明天那个模型的上线评审，你准备一下。", "Tomorrow's model launch review — prepare for it."),
           ("在准备。", "I'm on it.")],
    "04": [("讲完了早点回去。", "Finish up and go home early."),
           ("明天九点。", "Tomorrow at nine.")],
    "05": [("那一年，自动驾驶行业正在经历一场静默的革命——从模块化架构，全面转向 VLA，端到端模型。",
            "That year, autonomous driving was going through a quiet revolution — from modular architecture, fully shifting to VLA, end-to-end models.")],
    "06": [("你觉得自动驾驶最难的是什么？", "What do you think is the hardest part of autonomous driving?"),
           ("让车开得像人。", "Making the car drive like a person."),
           ("不对。最难的是让别人相信你的车开得像人。", "No. The hardest part is making people believe your car drives like a person.")],
    "07": [("在前边那个便利店门口停一下。", "Stop in front of that convenience store up ahead."),
           ("已识别便利店，距离120米。正在减速。", "Convenience store identified, 120 meters ahead. Slowing down.")],
    "09": [("她的副业是脱口秀。一场15分钟，万把块钱。", "Her side job is stand-up comedy. Fifteen minutes a show, about ten thousand yuan.")],
    "10": [("以前写段子是因为我有话想说。现在写段子是因为我接了单。",
            "I used to write jokes because I had something to say. Now I write them because I took the gig.")],
    "11": [("那你还写吗？", "So do you still write?"),
           ("写。但我需要找到那个有话想说的东西。不是为了甲方，是为了自己。",
            "I do. But I need to find that thing I want to say — not for the client, for myself.")],
    "12": [("基座是一个世界模型。她只是在教模型，莎拉·赵的观众为什么笑。",
            "The base is a world model. She's only teaching it why Sarah Zhao's audience laughs.")],
    "13": [("意味着它在想象观众。它不是在分析我的文本，是在看我讲。",
            "It means it's imagining the audience. It's not analyzing my text — it's watching me perform.")],
    "14": [("不是大脑，不是心脏。是骨架。撑着她，让她不会散架。但走路，还是她自己走。",
            "Not a brain, not a heart. A skeleton. It holds her up so she won't fall apart. But the walking — she does that herself.")],
    "15": [("你拿公司的模型改的？", "You modified the company's model?"),
           ("嗯。", "Mm-hmm."),
           ("合法吗？", "Is that legal?"),
           ("我读了一遍用户协议。没说不让。", "I read the user agreement. It doesn't say I can't.")],
    "16": [("那你别用来赚钱。", "Then don't use it to make money."),
           ("我不赚。我只是用来筛段子。", "I'm not. I just use it to filter my jokes.")],
    "17": [("但你别把我的代码写进段子里。", "But don't put my code in your jokes."),
           ("我已经写了。", "Already did."),
           ("……哪段？", "...Which part?")],
    "18": [("第147行，括号错了。", "Line 147, the bracket is wrong."),
           ("那是真的。", "That's true."),
           ("真的才好笑。", "It's only funny if it's true.")],
    "19": [("你去睡。", "Go to sleep."),
           ("我不困。", "I'm not tired."),
           ("你眼睛红了。", "Your eyes are red."),
           ("那是屏幕反光。", "That's the screen glare.")],
    "20": [("师兄后来再也不劝了。只是每次她熬完夜，第二天桌上会多一杯咖啡。",
            "After that, her senior never tried to stop her again. Only — every time she pulled an all-nighter, a cup of coffee would appear on her desk the next morning.")],
    "21": [("训练数据来自开放麦的录像。但这里有一个问题。",
            "The training data comes from open-mic recordings. But there's a problem here.")],
    "22": [("观众席里，有两个人是她认识的。", "In the audience, there are two people she knows.")],
    "23": [("模型学到的是一个模式，认为这个位置应该响。但那两个人笑，不是因为段子好。",
            "The model learned a pattern — that this seat should get laughs. But those two laugh, not because the joke is good.")],
    "24": [("所以你是在教模型一个脏数据？", "So you're teaching the model dirty data?"),
           ("我在教模型看到数据，然后我自己来修正。", "I'm teaching the model to see the data, then I correct it myself.")],
    "25": [("样本量足够大的时候，小周的笑会被稀释。所以我用小剧场试新段子，用小周当托，然后去大场子验证。",
            "When the sample is large enough, Xiao Zhou's laugh gets diluted. So I test new jokes in the small theater, using Xiao Zhou as a plant, then validate in a big venue.")],
    "26": [("模型听不懂最新的梗。所以莎拉每周都要手动更新词表。",
            "The model can't understand the latest memes. So Sarah manually updates her word list every week.")],
    "27": [("你在教模型听懂新梗？", "You're teaching the model to understand new memes?"),
           ("我在教它听懂人话。我学得比它快。因为我有身体。",
            "I'm teaching it to understand people. I learn faster than it does — because I have a body.")],
    "28": [("身体会告诉我，一个词从别人嘴里说出来的时候，是冒犯还是玩笑。模型看不到那个。",
            "My body tells me whether a word, coming out of someone's mouth, is an insult or a joke. The model can't see that.")],
    "30": [("不存在的观众，在想象中笑着。绿色是安全，黄色是可能响，红色是大概率会响。",
            "Audiences that don't exist, laughing in imagination. Green is safe, yellow is might land, red is very likely to land.")],
    "31": [("但那张脸不存在。它不知道那个人是小周还是陌生人。",
            "But that face doesn't exist. It doesn't know if that person is Xiao Zhou or a stranger.")],
    "32": [("她想起师兄说的话。模型告诉你什么大概率是对的。但它不知道什么小概率。",
            "She remembers what her senior said. The model tells you what's probably right. But it doesn't know about the small probabilities.")],
    "33": [("我说，在前边那个便利店停一下。", "I said, stop in front of that convenience store up ahead."),
           ("车说，已识别便利店。", "The car said, convenience store identified."),
           ("我说，你认识便利店？", "I said, you know convenience stores?"),
           ("车说，我认识十二种便利店。", "The car said, I know twelve kinds of convenience stores."),
           ("我说，那你认识我常买的那种水吗？", "I said, then do you know the water I usually buy?"),
           ("车说，你常买的是农夫山泉。", "The car said, you usually buy Nongfu Spring."),
           ("我说，那不是水？", "I said, isn't that water?")],
    "34": [("不是0.52。是没想到。模型知道小周会笑，但不知道为什么。莎拉知道。这就是区别。",
            "It wasn't 0.52. It was the surprise. The model knows Xiao Zhou will laugh, but not why. Sarah knows. That's the difference.")],
    "35": [("今天那个结尾，0.52？", "That ending today, 0.52?"),
           ("是。", "Yeah.")],
    "36": [("模型说的是预测笑声强度0.52，不是不行。训练数据里没有我的声音，没有我的停顿，没有小周。",
            "The model said predicted laughter intensity 0.52 — not that it won't work. The training data has no voice of mine, no pause of mine, no Xiao Zhou.")],
    "37": [("那它算你的工具，还是你的搭档？", "So is it your tool, or your partner?")],
    "38": [("你知道为什么我从不评价你的段子吗？因为你不需要。你有自己的判断。你只是需要一个人帮你把那些肯定不行的去掉。",
            "Do you know why I never judge your jokes? Because you don't need it. You have your own judgment. You just need someone to help you cut out the ones that definitely won't work.")],
    "39": [("那你是我的工具还是我的搭档？模型没有回答。她没给它设计这个功能。",
            "So are you my tool or my partner? The model didn't answer. She never built that feature.")],
    "40": [("模型不知道意外。它只知道概率。它渲染不出一个因为没想到而愣住然后突然笑出来的脸。",
            "The model doesn't know surprise. It only knows probability. It can't render a face that freezes in surprise, then suddenly bursts out laughing.")],
    "41": [("但她的观众会那样笑。这就是她还站在台上的原因。",
            "But her audience laughs that way. That's why she's still on stage.")],
    "42": [("她想起地铁。明天早上，她不开车，坐地铁上班。是为了看看那些人，那些不在训练数据里的人。",
            "She thinks of the subway. Tomorrow morning she won't drive — she'll take the subway to work. To look at those people, the ones not in her training data.")],
    "44": [("有些东西可以备份，有些东西不能。不能备份的那些，才是你。",
            "Some things can be backed up, some can't. The things that can't be backed up — those are you.")],
    "45": [("明天九点，别迟到。", "Tomorrow, nine o'clock. Don't be late."),
           ("知道。师兄，我明天坐地铁。", "Got it. Senior, tomorrow I'll take the subway.")],
    "46": [("你的车呢？", "What about your car?"),
           ("在车库。我想看看那些人。", "It's in the garage. I want to see those people."),
           ("好。", "Okay.")],
    "47": [("不是算法预测的下一个窗口。是今天。是现在。她不想预测。想坐地铁。",
            "Not the next window the algorithm predicts. It's today. It's now. She doesn't want to predict. She wants to take the subway.")],
}

# 纯字幕（后期 · 不在 H3 音轨里）：shot → [(zh, en)]
CAPTION = {
    "48": [("莎拉不知道，在同一座城市的另一个角落，一个叫老周的网约车司机正在等一句“小雨最近怎么样”。",
            "Sarah doesn't know that, in another corner of the same city, a ride-hailing driver named Old Zhou is waiting for one line: \"How's Xiaoyu been lately?\"")],
}


def fmt_ts(sec: float) -> str:
    sec = max(0.0, sec)
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_entries():
    """按镜号 01→48 累积 `h3_dur_sec`，把每镜台词按句均摊到该镜时间窗。"""
    entries = []          # [(start, end, "zh\\nen")]
    cursor = 0.0
    for shot in sorted(ALL.keys(), key=int):
        dur = h3_dur_sec(ALL[shot]["dur"])
        seg = DIALOGUE.get(shot) or CAPTION.get(shot)
        if seg:
            n = len(seg)
            for i, (zh, en) in enumerate(seg):
                start = cursor + dur * i / n
                end = cursor + dur * (i + 1) / n
                entries.append((start, end, f"{zh}\n{en}"))
        cursor += dur
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
    ap = argparse.ArgumentParser(description="第13集《外骨骼》成片字幕（去 TTS）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划，不写文件")
    args = ap.parse_args()

    total = sum(h3_dur_sec(ALL[s]["dur"]) for s in ALL)
    entries = build_entries()
    print(f"EP13《外骨骼》字幕 | 48 镜 | 预计总时长 {total:.2f}s | 字幕 {len(entries)} 条")
    if args.dry_run:
        for start, end, text in entries:
            first = text.split("\n")[0][:24]
            print(f"  {fmt_ts(start)} → {fmt_ts(end)}  {first}…")
        print("\n[Dry-run] 未写文件。")
        return

    write_srt(entries, SRT)
    print(f"✅ 字幕已写: {SRT} ({len(entries)} 条)")
    print(f"   （硬字幕烧录由 synth_ep13.py 在拼接后执行）")


if __name__ == "__main__":
    main()
