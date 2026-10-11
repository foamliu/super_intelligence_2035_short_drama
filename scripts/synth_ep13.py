#!/usr/bin/env python3
"""EP13 成片合成：拼接 11 镜 + 混音（BGM + TTS）+ 字幕 -> 成片 mp4。"""
import subprocess, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # 项目根（原 E:/code/... 已迁至 D:\...，改为脚本相对定位）
EP = ROOT / "OUTPUT" / "13_外骨骼"
UP = EP / "upscaled"
AUD = EP / "audio"
UP.mkdir(parents=True, exist_ok=True)

# 镜头顺序（叙事序）
ORDER = [
    "EP13_SHOT-01_H3_720p_sarah_desk_explaining.mp4",  # 工位解释外骨骼
    "EP13_SHOT-02_office_exoskeleton_ui_push.mp4",      # 外骨骼UI
    "EP13_SHOT-03_H3_720p_shixiong_coffee_legal.mp4",   # 师兄"合法吗"
    "EP13_SHOT-04_lab_2017_night_coffee_steam.mp4",     # 2017实验室闪回
    "EP13_SHOT-05_subway_rush_hour_commute.mp4",        # 地铁群像
    "EP13_SHOT-06_H3_720p_sarah_subway_observing.mp4",  # 莎拉地铁观察
    "EP13_SHOT-07_virtual_face_082_laughing.mp4",       # 虚拟观众脸
    "EP13_SHOT-08_render_vs_real_fade.mp4",             # 渲染vs真实
    "EP13_SHOT-09_notebook_label_push.mp4",             # 笔记本
    "EP13_SHOT-10_wechat_typing_hao.mp4",               # 微信"好"
    "EP13_SHOT-11_H3_sarah_bar_052.mp4",                # 吧台散场
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r

def probe_dur(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)])
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0

# 台词与镜头的对应（start 为在成片中的起始秒，允许声音溢出到后续镜头）
TTS_CUES = [
    # (音频文件, 起始秒)
    ("13_tts_sarah_02_desk.flac", 0.00),       # 工位解释外骨骼
    ("13_tts_shixiong_01_hefa.flac", 18.19),   # 师兄"合法吗"
    ("13_tts_shixiong_02_code.flac", 19.87),
    ("13_tts_shixiong_03_bracket.flac", 22.99),
    ("13_tts_sarah_05_hao.flac", 70.79),       # 微信"好"
    ("13_tts_sarah_04_bar.flac", 80.85),       # 吧台散场
]

def main():
    # 1. 拼接视频轨（concat demuxer，绝对路径 + UTF-8）
    concat_txt = UP / "concat_list.txt"
    lines = [f"file '{UP / f}'" for f in ORDER]
    concat_txt.write_text("\n".join(lines), encoding="utf-8")

    video_track = UP / "video_track.mp4"
    print("=== 1. 拼接视频轨 ===")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", str(concat_txt),
         "-c:v", "libx264", "-crf", "18", "-preset", "fast",
         "-an", str(video_track)])
    if not video_track.exists():
        print("拼接失败")
        return
    total = probe_dur(video_track)
    print(f"视频轨完成: {total:.1f}s")

    # 2. 构建混音：TTS 台词 + BGM
    print("=== 2. 混音 (TTS + BGM) ===")
    bgm_src = AUD / "13_bgm_04_bar_aftermath.mp3"

    inputs = ["-i", str(video_track), "-i", str(bgm_src)]
    fc_parts = []
    amix_inputs = []
    # TTS 输入（从 index 2 开始）
    for i, (tts_file, start_s) in enumerate(TTS_CUES):
        p = AUD / tts_file
        if not p.exists():
            continue
        idx = 2 + i
        inputs += ["-i", str(p)]
        delay_ms = int(start_s * 1000)
        fc_parts.append(f"[{idx}:a]aresample=48000,adelay={delay_ms}|{delay_ms},"
                        f"volume=1.0[t{i}]")
        amix_inputs.append(f"[t{i}]")

    # BGM 循环 + 低音量
    fc_parts.append(f"[1:a]aresample=48000,volume=0.22[bgm]")
    amix_inputs.append("[bgm]")

    # 混合所有音频
    n = len(amix_inputs)
    amix = "".join(amix_inputs) + f"amix=inputs={n}:duration=longest:normalize=0[outa]"
    fc_parts.append(amix)

    filter_complex = ";".join(fc_parts)

    final = EP / "EP13_外骨骼_成片_v2.mp4"
    print("=== 3. 合成成片 ===")
    r = run(["ffmpeg", "-y", *inputs,
             "-filter_complex", filter_complex,
             "-map", "0:v", "-map", "[outa]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
             "-shortest", str(final)])
    if final.exists():
        print(f"OK 成片: {final.name} ({probe_dur(final):.1f}s, "
              f"{(final.stat().st_size/1024/1024):.1f}MB)")
    else:
        print("合成失败:", r.stderr[-1200:])

if __name__ == "__main__":
    main()
