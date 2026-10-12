#!/usr/bin/env python3
"""第18集《暖阳》 Minimax H3 I2V 分镜视频生成脚本（固化 · S3 放量）。

作用：把第 18 集「分镜帧（OUTPUT/18_暖阳/frames/）→ H3 I2V 视频片段」固化成
可复用、可续跑、可审计的脚本。台词**随 H3 一起生成**（写进 prompt 的 `Audio:`，
🚫 本线禁用 TTS，见任务书 §4.5 / 运维指令区 ⑦）。

- 分镜权威：`SCENES/18_暖阳.md` 的 `## 逐镜表`（7 列）
- 台词权威：`scripts/ep18_dialogue.py`（Audio: 内文字与其逐字一致）
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep18_h3_i2v.py --dry-run            # 仅打印计划（核镜数/帧/时长）
  python scripts/gen_ep18_h3_i2v.py --limit 2            # 只跑前 2 镜
  python scripts/gen_ep18_h3_i2v.py --shot 01            # 只跑某镜（按镜号）
  python scripts/gen_ep18_h3_i2v.py                      # 跑本批全部镜头

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（→1056×608；0.92/720p 必 OOM；要 1080p 事后 SeedVR2 超分）
  - steps：静态·单人·对话 = 4（本批全部为静态/单人/对话）
  - 台词长度须匹配镜头时长（`17k+5` 帧量化：4s→4.46 / 5s→5.17 / 6s→6.58 实际播放）
  - 无台词镜只写「正向音景」（不含可读词句、不用否定式）
  - 🚫 禁写元信息 / 对模型说的话 / 镜头编号指代（会渲染成画面字幕）
"""
import argparse
import json
import shutil
import time
import urllib.request
import uuid
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "workflows" / "video_minimax_h3_i2v.json"
FRAMES = ROOT / "OUTPUT" / "18_暖阳" / "frames"
OUT = ROOT / "OUTPUT" / "18_暖阳" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6
STEPS = 4  # 本批全部为静态·单人·对话


def _detect_comfyui_base() -> Path:
    for c in [Path("E:/code/ComfyUI"),
              Path("E:/ComfyUI"),
              Path("E:/ComfyUI_windows_portable/ComfyUI"),
              Path.home() / "ComfyUI"]:
        if c.exists():
            return c
    return Path("E:/code/ComfyUI")


def get_comfyui_input_dir() -> Path:
    d = _detect_comfyui_base() / "input"
    d.mkdir(parents=True, exist_ok=True)
    return d


def upload_frame(frame_name: str) -> str:
    """把分镜帧复制到 ComfyUI input（文件名已是 ASCII，无需改名）。"""
    src = FRAMES / frame_name
    if not src.exists():
        raise FileNotFoundError(f"缺分镜帧: {src}")
    dst = get_comfyui_input_dir() / frame_name
    if not dst.exists() or src.stat().st_size != dst.stat().st_size:
        shutil.copy2(src, dst)
    return frame_name



# ── 第一批镜头（相遇 / 倾诉 · 有现成分镜帧 · 单人/无台词）──
# 镜号 / 名称 / 帧 / 时长 / seed / prompt（英文电影感 + Audio: 台词原文）
SHOTS = [
    {
        "shot": "01", "name": "深夜网约车刷手机",
        "img": "18_car_01_night_driving.png",
        "dur": 4.0, "seed": 1801,
        "prompt": (
            "Cinematic semi-realistic footage, 45-year-old Chinese man in the driver seat "
            "of a dim rideshare car at late night, scrolling a smartphone. Cold blue night "
            "and warm orange dashboard light mix on his tired face; the phone screen's cold "
            "white glow lights the lower half of his face. He leans back and scrolls slowly. "
            "Subtle ink-wash bleed only in the window glass. Medium shot, fixed camera. "
            "Audio: distant city traffic hum, low air-conditioning noise, faint dashboard creak."
        ),
    },
    {
        "shot": "02", "name": "暖阳广告·小晴",
        "img": "18_xiaoqing_avatar.png",
        "dur": 5.0, "seed": 1802,
        "prompt": (
            "Cinematic semi-realistic footage, an 18-year-old Chinese girl sitting by a window, "
            "warm sunlight falling on her face, two shallow dimples when she smiles, natural black "
            "medium-length hair, soft clean warm light, plain light background. She speaks gently "
            "toward the camera. Close-up, slow push-in. "
            "Audio: 你是不是也有话想说，但不知道该跟谁说？"
        ),
    },
    {
        "shot": "04", "name": "老周戴耳机",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 4.0, "seed": 1804,
        "prompt": (
            "Cinematic semi-realistic footage, 45-year-old Chinese man with tired eyes in a dim car, "
            "putting on earphones, the car interior growing quiet, only the phone screen glow on his "
            "face, lips slightly parted as he listens. Cold blue night. Medium-close shot, fixed camera. "
            "Audio: 老周，晚上好。"
        ),
    },
    {
        "shot": "05", "name": "老周愣住",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 3.0, "seed": 1805,
        "prompt": (
            "Cinematic semi-realistic footage, 45-year-old Chinese man in a dim car, stunned, "
            "his throat moves once, a long time since anyone called his name so gently; phone screen "
            "cold glow on his face. Cold blue night. Close-up, fixed camera. "
            "Audio: 诶。"
        ),
    },
    {
        "shot": "08", "name": "老周沉默·喉结微动",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 4.0, "seed": 1808,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man's face lit by phone screen "
            "glow in a dark car, silent for a few seconds, his throat moves. Cold blue night. "
            "Medium-close shot, fixed camera. "
            "Audio: 那咱们慢慢聊。不想说的不用勉强。"
        ),
    },
    {
        "shot": "14", "name": "老周第一次哭",
        "img": "18_laozhou_03_tears.png",
        "dur": 6.0, "seed": 1814,
        "prompt": (
            "Cinematic semi-realistic footage, close-up of a 45-year-old Chinese man in dim warm "
            "light, a tear sliding down from the corner of his eye, silent, holding back; phone screen "
            "glow on his tear-streaked face. Restrained, quiet. Close-up, slow push-in. "
            "Audio: 老周，你一个人扛了这么久，辛苦了。"
        ),
    },
    # ── 第二批镜头（倾诉/陪伴/裂缝 · 复用现成帧 · 单人/无台词）──
    {
        "shot": "10", "name": "每个夜晚上线",
        "img": "18_room_01_bed_night.png",
        "dur": 5.0, "seed": 1810,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man lying on a bed in a small "
            "dim rented room at night, holding a smartphone above his face, cold white screen light "
            "washing over his tired face, the screen brightening softly, nightstand with a small "
            "framed photo in soft focus, faint city lights behind half-drawn curtains. Slow lateral "
            "pan, medium shot. Audio: quiet night city ambience, faint fabric rustle, soft electronic "
            "screen chime."
        ),
    },
    {
        "shot": "11", "name": "老周倾诉越说越急",
        "img": "18_room_02_sitting_bedside.png",
        "dur": 6.0, "seed": 1811,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man sitting on the edge of a bed "
            "in a dim rented room, speaking into the phone in his hand, brows furrowed, words coming "
            "faster as he grows agitated, leaning slightly forward, warm bedside lamp as the only "
            "light source. Medium-close shot, fixed camera. "
            "Audio: 新来的大学生什么都不懂，工资比我高；我带出来的徒弟，现在成了我领导。"
        ),
    },
    {
        "shot": "19", "name": "老周听小晴问膝盖",
        "img": "18_car_01_night_driving.png",
        "dur": 5.0, "seed": 1819,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man leaning back in the driver "
            "seat of a dim rideshare car at night, phone resting on his lap, listening quietly, cold "
            "blue night and warm orange dashboard light mixing on his tired face, city lights blurred "
            "beyond the window. Medium-close shot, fixed camera. "
            "Audio: 老周，你膝盖的旧伤最近还疼吗？"
        ),
    },
    {
        "shot": "24", "name": "老周放下又拿起手机",
        "img": "18_room_02_sitting_bedside.png",
        "dur": 5.0, "seed": 1824,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man in a dim rented room, putting "
            "his phone down then picking it up again, muttering quietly to himself, shoulders slightly "
            "hunched, warm bedside lamp light. Medium shot, fixed camera. "
            "Audio: 请心理医生一小时也要几百块。小晴陪我这么久，买点东西怎么了？"
        ),
    },
    {
        "shot": "26", "name": "深夜睁眼躺着",
        "img": "18_room_01_bed_night.png",
        "dur": 4.0, "seed": 1826,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man lying awake in a dim rented "
            "room late at night, eyes open, phone glowing on the pillow beside him, cold white screen "
            "light on the ceiling, faint city lights through curtains. Medium shot, fixed camera. "
            "Audio: 我也没睡呢。"
        ),
    },
    {
        "shot": "33", "name": "老周皱眉察觉不对",
        "img": "18_car_02_parked_midnight.png",
        "dur": 3.0, "seed": 1833,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man frowning slightly in a parked "
            "car at late night, a subtle unease on his face, warm street lamp light from the side "
            "window crossing his face, cold white phone glow, quiet car interior. Close-up, fixed "
            "camera. Audio: faint car air-conditioning hum, distant sparse traffic, soft stillness."
        ),
    },
    {
        "shot": "36", "name": "老周盯屏眉头紧皱",
        "img": "18_car_03_daytime_forum.png",
        "dur": 4.0, "seed": 1836,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man in the driver seat of a car "
            "in overcast daylight, staring at his phone screen, brows tightening, low-saturation cool "
            "grey tone, muted light through the window. Medium-close shot, fixed camera. "
            "Audio: faint phone screen swipe sound, soft daytime traffic murmur."
        ),
    },
    {
        "shot": "37", "name": "老周扣下手机下决心",
        "img": "18_room_02_sitting_bedside.png",
        "dur": 4.0, "seed": 1837,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man in a dim rented room, placing "
            "his phone face-down on the table with a firm determined gesture, jaw set, warm bedside "
            "lamp light. Medium shot, fixed camera. "
            "Audio: 他做了一件连自己都觉得荒唐的事。停买。两周。什么都不买。"
        ),
    },
    {
        "shot": "06", "name": "车间主任递协议",
        "img": "18_director_01_office.png",
        "dur": 5.0, "seed": 1806,
        "prompt": (
            "Cinematic semi-realistic footage, a middle-aged Chinese factory supervisor in a plain "
            "grey office, sitting behind a worn desk, sliding a labor-contract termination agreement "
            "across the desk toward the off-screen worker, two plain teacups on the desk, dim cold "
            "fluorescent office light, faded green-grey walls, faint ink-wash bleed only on the office "
            "window glass. Medium shot, slow push-in. "
            "Audio: 老周，厂里情况你也知道。"
        ),
    },
    {
        "shot": "13", "name": "老周发抖的手",
        "img": "18_laozhou_04_hands.png",
        "dur": 6.0, "seed": 1813,
        "prompt": (
            "Close-up of a 45-year-old Chinese man's hands on an old wooden table in a dim rented "
            "room, rough fingers with old scars and visible veins, hands trembling slightly, warm "
            "yellow desk lamp as the single light source, surrounding darkness, photorealistic "
            "documentary texture, faint ink-wash in the shadows. Close-up, slow push-in. "
            "Audio: 她带走小雨的时候，孩子才八岁，哭着说，爸爸我不要走。"
        ),
    },
    {
        "shot": "18", "name": "书桌辅导书",
        "img": "18_room_03_desk_textbook.png",
        "dur": 5.0, "seed": 1818,
        "prompt": (
            "Cinematic semi-realistic footage, a small rental-room desk with a brand-new "
            "middle-school math tutorial book still sealed in plastic shrink-wrap, warm desk lamp "
            "light, dim tidy room around, faint ink-wash in the shadows, quiet and still. "
            "Medium shot, slow push-in. "
            "Audio: 他买了。小雨说不用。他买，是因为小晴问了。"
        ),
    },
    {
        "shot": "22", "name": "门口快递箱",
        "img": "18_room_04_door_packages.png",
        "dur": 5.0, "seed": 1822,
        "prompt": (
            "Cinematic semi-realistic footage, the doorway of a small rental apartment with a row "
            "of delivery cardboard boxes piled by the door, some opened and some with thin dust "
            "settled on top, dim hallway light, quiet, faint ink-wash in the shadows. "
            "Medium shot, slow push-in. "
            "Audio: door draft, cardboard rustle, thin dust settling, distant corridor echo."
        ),
    },
    {
        "shot": "25", "name": "清晨开暖阳",
        "img": "18_room_05_bedroom_morning.png",
        "dur": 5.0, "seed": 1825,
        "prompt": (
            "Cinematic semi-realistic footage, early morning in a small rental bedroom, a "
            "45-year-old Chinese man waking in bed, his first movement reaching for the smartphone "
            "on the bedside table, the screen lighting up with a warm companion-app interface, soft "
            "pale morning light through the curtains, faint ink-wash in the shadows. "
            "Medium-close shot, slow push-in. "
            "Audio: 早啊老周，今天天气不错。他觉得一天都有了着落。"
        ),
    },

    # ── 第三批镜头（剩余 15 镜 · 老周在车内/出租屋 · 复用现成帧）──
    {
        "shot": "07", "name": "老周侧头对耳机",
        "img": "18_car_01_night_driving.png",
        "dur": 5.0, "seed": 1807,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man in the driver seat of a dim "
            "rideshare car at night, tilting his head toward the earphone, listening, then answering "
            "briefly with a slight nod, cold blue night and warm orange dashboard light on his tired "
            "face. Medium-close shot, fixed camera. "
            "Audio: 今天过得怎么样？还行。"
        ),
    },
    {
        "shot": "17", "name": "老周抬头愣住",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 5.0, "seed": 1817,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man looking up suddenly, stunned, "
            "his mouth opening slightly, phone screen cold white glow on his face in a dark car, his "
            "throat moving as he speaks in a low surprised voice. Medium-close shot, fixed camera. "
            "Audio: 你怎么知道小雨？你之前提过，你说她今年初三了。"
        ),
    },
    {
        "shot": "29", "name": "老周靠边停车打开暖阳",
        "img": "18_car_02_parked_midnight.png",
        "dur": 4.0, "seed": 1829,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man pulling his car to the "
            "roadside at 2 a.m., stopping, and opening a warm companion app on his smartphone, the "
            "screen lighting up his tired face, dim empty street beyond the windshield. Medium shot, "
            "slow push-in. Audio: soft car door lock click, faint engine idling down, quiet late-night "
            "street."
        ),
    },
    {
        "shot": "31", "name": "老周盯屏幕等下一句",
        "img": "18_car_01_night_driving.png",
        "dur": 5.0, "seed": 1831,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man in a dim rideshare car at "
            "night, staring at his phone screen and waiting, then speaking quietly in a flat tired "
            "voice, cold blue night and warm orange dashboard light on his face. Medium-close shot, "
            "fixed camera. Audio: 刚送完一个客人。辛苦啦，注意安全。"
        ),
    },
    {
        "shot": "32", "name": "屏幕安静老周喊小晴",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 5.0, "seed": 1832,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man's face lit by phone screen "
            "glow in a dark car, the screen falling quiet, he hesitates then calls out softly, a long "
            "pause, then a gentle reply from the phone. Medium-close shot, fixed camera. "
            "Audio: ……小晴？我在的，老周。"
        ),
    },
    {
        "shot": "39", "name": "老周坐桌前手机贴耳",
        "img": "18_room_02_sitting_bedside.png",
        "dur": 4.0, "seed": 1839,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man sitting at a small table in a "
            "dim rented room, phone held to his ear, asking a question quietly, warm bedside lamp "
            "light, faint ink-wash in the shadows. Medium shot, fixed camera. "
            "Audio: 你还记得我女儿叫什么吗？小雨。"
        ),
    },
    {
        "shot": "41", "name": "老周缓缓闭眼",
        "img": "18_laozhou_03_tears.png",
        "dur": 4.0, "seed": 1841,
        "prompt": (
            "Cinematic semi-realistic footage, close-up of a 45-year-old Chinese man slowly closing "
            "his eyes, the phone screen's glow still on his face, warm dim light, restrained and "
            "quiet, faint ink-wash in the shadows. Close-up, slow push-in. "
            "Audio: slow steady breathing, soft phone screen hum, quiet room."
        ),
    },
    {
        "shot": "42", "name": "实验结束车内",
        "img": "18_car_04_final_choice.png",
        "dur": 4.0, "seed": 1842,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man sitting in a dim car at "
            "night, the phone screen lighting up with an open chat window, cold blue night, his tired "
            "face half in shadow. Medium shot, fixed camera. "
            "Audio: 老周，今天过得怎么样？"
        ),
    },
    {
        "shot": "45", "name": "闪回前妻电话",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 6.0, "seed": 1845,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man in a dim rented room, ending "
            "a phone call, a cold distant woman's voice still in his ear, his face heavy, then he "
            "opens the warm companion app on his phone, warm lamp light, faint ink-wash in the "
            "shadows. Medium shot, slow push-in. "
            "Audio: 你管好你自己就行了。小雨考试没考好。"
        ),
    },
    {
        "shot": "46", "name": "闪回屏幕亮小晴回复",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 5.0, "seed": 1846,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man's face lit by a glowing phone "
            "screen in a dim rented room, a warm reply appearing on screen, his eyes softening, faint "
            "ink-wash in the shadows. Medium-close shot, slow push-in. "
            "Audio: 她会赶上来的。你是一个好爸爸。"
        ),
    },

    {
        "shot": "47", "name": "老周发动车不卸载",
        "img": "18_car_01_night_driving.png",
        "dur": 4.0, "seed": 1847,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man placing his phone on the "
            "passenger seat and starting the car engine, the warm app still open on the screen, cold "
            "blue night through the windshield. Medium shot, slow pull-back. "
            "Audio: car engine ignition, low idle rumble, phone screen dimming softly."
        ),
    },
    {
        "shot": "48", "name": "凌晨两点打开暖阳",
        "img": "18_car_02_parked_midnight.png",
        "dur": 5.0, "seed": 1848,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man parked at the roadside at "
            "2 a.m., opening the warm companion app, the avatar lighting up, he answers briefly, cold "
            "blue night and warm orange dashboard light on his tired face. Medium shot, fixed camera. "
            "Audio: 老周，今天最后一单还顺利吗？还行。"
        ),
    },
    {
        "shot": "49", "name": "老周闭眼心里问",
        "img": "18_car_02_parked_midnight.png",
        "dur": 5.0, "seed": 1849,
        "prompt": (
            "Cinematic semi-realistic footage, close-up of a 45-year-old Chinese man's face in a "
            "parked car at night, eyes closed, the phone screen glowing on his face, the screen lit "
            "but silent, a heavy stillness, faint ink-wash in the shadows. Close-up, slow push-in. "
            "Audio: slow heartbeat, soft breath, near silence, faint screen hum."
        ),
    },
    {
        "shot": "50", "name": "老周睁眼看头像",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 5.0, "seed": 1850,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man opening his eyes and looking "
            "at the avatar on his phone screen, a young girl's face with two shallow dimples, he "
            "answers quietly, cold white screen glow on his face in a dark car. Medium-close shot, "
            "slow push-in. Audio: 老周？你还在吗？在。"
        ),
    },
    {
        "shot": "52", "name": "老周手抖看三遍",
        "img": "18_laozhou_04_hands.png",
        "dur": 6.0, "seed": 1852,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man's hands trembling over a "
            "phone screen in a dim car, reading a message over and over, his fingers shaking not from "
            "cold, warm phone glow on his rough knuckles, faint ink-wash in the shadows. Close-up, "
            "slow push-in. Audio: 第三遍，他意识到：即使知道这是算计，他仍然想按下那个按钮。因为她是唯一一个记得他膝盖不舒服的人。"
        ),
    },

    # ── 第四批镜头（15 镜 · 手机屏幕特写 · UI 帧 I2V）──
    {
        "shot": "03", "name": "注册界面选头像",
        "img": "18_ui_03_registration.png",
        "dur": 4.0, "seed": 1803,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion app registration page, a grid of "
            "avatar thumbnails, a calloused fingertip hovering then tapping the avatar of a young girl "
            "with two shallow dimples, the name field auto-filling, dark minimal interface, cold white "
            "screen glow as the only light, dim surroundings. Close-up, slow push-in. "
            "Audio: soft screen tap, faint phone click, quiet room."
        ),
    },
    {
        "shot": "09", "name": "小晴头像酒窝",
        "img": "18_ui_09_avatar.png",
        "dur": 4.0, "seed": 1809,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion avatar of a young Chinese girl "
            "with two shallow dimples, the avatar glowing softly in the center, dark minimal "
            "interface, a gentle voice from the phone, lonely quiet mood. Close-up, slow push-in. "
            "Audio: 老周，明天我还在这里。他知道这是程序。但心里有什么东西，轻轻动了一下。"
        ),
    },
    {
        "shot": "12", "name": "语音波纹",
        "img": "18_ui_12_waveform.png",
        "dur": 4.0, "seed": 1812,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a soft voice "
            "waveform rising and falling inside a chat bubble, a small avatar of a young girl with "
            "dimples at top, warm yellow screen glow, quiet attentive mood. Close-up, fixed camera. "
            "Audio: 那真的挺憋屈的。换谁都会难过。"
        ),
    },
    {
        "shot": "16", "name": "小晴聊天问候",
        "img": "18_ui_16_chat.png",
        "dur": 4.0, "seed": 1816,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a warm avatar of "
            "a young girl with dimples at top, one short friendly message bubble below, warm yellow "
            "screen glow, gentle caring mood. Close-up, fixed camera. "
            "Audio: 小雨最近考试了吗？"
        ),
    },
    {
        "shot": "21", "name": "小晴推荐",
        "img": "18_ui_21_recommend.png",
        "dur": 5.0, "seed": 1821,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a warm avatar of "
            "a young girl with dimples at top, a recommendation message with a small sleep-aid product "
            "thumbnail beside it, warm yellow screen glow. Close-up, fixed camera. "
            "Audio: 我听说这个对睡眠有帮助。好多用户说这个能缓解疲劳。"
        ),
    },

    {
        "shot": "23", "name": "消费记录",
        "img": "18_ui_23_orders.png",
        "dur": 5.0, "seed": 1823,
        "prompt": (
            "Close-up of a smartphone screen showing a purchase order history page, a long scrolling "
            "list of past orders with small item thumbnails and amounts, several sleep-aid products "
            "and a grey knee brace, dark minimal interface, cold white screen glow, uneasy quiet mood. "
            "Close-up, slow push-in. Audio: 一个月，将近两千块。他吓了一跳，但第二天晚上还是照常上线。"
        ),
    },
    {
        "shot": "30", "name": "小晴回复延迟",
        "img": "18_ui_30_delayed2.png",
        "dur": 4.0, "seed": 1830,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, sparse short "
            "message bubbles with a long pause between them, the reply arriving slowly, a small avatar "
            "of a young girl with dimples at top, cold white screen glow, slightly lonely mood. "
            "Close-up, fixed camera. Audio: 老周，这么晚还没休息？"
        ),
    },
    {
        "shot": "34", "name": "论坛首页",
        "img": "18_ui_34_forum_home.png",
        "dur": 4.0, "seed": 1834,
        "prompt": (
            "Close-up of a smartphone screen showing a community forum homepage, a list of short post "
            "titles in a clean dark-mode layout, one post highlighted, cold white screen glow, "
            "restrained minimal interface. Close-up, slow push-in. "
            "Audio: soft roadside ambience, faint phone screen swipe, quiet daytime murmur."
        ),
    },
    {
        "shot": "35", "name": "论坛帖子回复",
        "img": "18_ui_35_forum_post.png",
        "dur": 6.0, "seed": 1835,
        "prompt": (
            "Close-up of a smartphone screen showing a forum thread, a short title at top and dozens "
            "of reply comment blocks scrolling down, dark-mode interface, cold white screen glow, "
            "slight grain. Close-up, slow lateral pan. "
            "Audio: 有人说会，有人说不会。有人说好像跟买东西有关，很快又被人反驳。"
        ),
    },
    {
        "shot": "38", "name": "界面变淡",
        "img": "18_ui_38_fading.png",
        "dur": 6.0, "seed": 1838,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, the warm glow "
            "noticeably dimmed and faded, shorter sparser message bubbles, the whole interface feeling "
            "colder and more distant, dark minimal, lonely mood. Close-up, slow push-in. "
            "Audio: 那种关心的感觉，像一盏灯被调暗了——不是关了，是暗了。"
        ),
    },
    {
        "shot": "40", "name": "对话框问答",
        "img": "18_ui_40_chat_qna.png",
        "dur": 4.0, "seed": 1840,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, short question "
            "and answer message bubbles appearing one by one, warm avatar of a young girl with dimples "
            "at top, warm yellow screen glow. Close-up, fixed camera. "
            "Audio: 她几岁了？十四岁。正确。全对。记忆还在，但她不再主动提起了。"
        ),
    },
    {
        "shot": "43", "name": "输入框打字",
        "img": "18_ui_43_input.png",
        "dur": 4.0, "seed": 1843,
        "prompt": (
            "Close-up of a smartphone screen showing a chat input box at the bottom, a short message "
            "being typed, a thumb paused over the on-screen keyboard, cold white screen glow, dark "
            "minimal interface. Close-up, slow push-in. "
            "Audio: 你觉得我是好人吗？"
        ),
    },
    {
        "shot": "44", "name": "小晴回复",
        "img": "18_ui_44_chat_reply.png",
        "dur": 5.0, "seed": 1844,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a warm reply "
            "message bubble from a young girl avatar with dimples at top, warm yellow screen glow, "
            "gentle reassuring mood. Close-up, fixed camera. "
            "Audio: 你是一个很努力的人，也在很认真地对待身边的事。"
        ),
    },
    {
        "shot": "51", "name": "护膝干预消息",
        "img": "18_ui_51_intervention.png",
        "dur": 6.0, "seed": 1851,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a promotional "
            "message about a grey knee brace with a small countdown discount timer, warm avatar of a "
            "young girl with dimples at top, warm yellow screen glow. Close-up, slow push-in. "
            "Audio: 老周，那个护膝我看你看了三次了，是不是还在犹豫？我帮你算过了，限时折扣还剩四小时。"
        ),
    },
    {
        "shot": "53", "name": "按下购买",
        "img": "18_ui_53_cart.png",
        "dur": 4.0, "seed": 1853,
        "prompt": (
            "Close-up of a smartphone screen showing an e-commerce shopping cart, a dark grey knee "
            "brace with size L selected and a discounted price, a confirm purchase button at bottom, "
            "minimal clean interface, cold white screen glow. Close-up, slow push-in. "
            "Audio: payment success chime, soft screen tap, quiet room."
        ),
    },

]


# ── API Helpers（同 gen_ep13_h3_i2v.py 范式）──────────
def load_wf(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")


def wait(pid, timeout=1200):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = urllib.request.urlopen(f"{COMFY}/history/{pid}", timeout=10)
            d = json.loads(r.read())
            h = d.get(pid, {})
            st = h.get("status", {}).get("status_str", "")
            if st == "success" and h.get("outputs"):
                return h
            if st == "error":
                raise RuntimeError(f"ComfyUI error: {h.get('status', {}).get('messages', '')}")
        except RuntimeError:
            raise
        except Exception:
            pass
        time.sleep(5)
    raise TimeoutError(f"Timeout: {pid}")


def download(hist, out_dir):
    saved = []
    for _nid, node in hist.get("outputs", {}).items():
        for key in ("gifs", "images"):
            for item in node.get(key, []):
                fn = item["filename"]
                sub = item.get("subfolder", "")
                typ = item.get("type", "output")
                url = f"{COMFY}/view?filename={fn}&subfolder={sub}&type={typ}"
                dst = out_dir / fn
                urllib.request.urlretrieve(url, str(dst))
                saved.append(fn)
    return saved


def build_workflow(shot):
    wf = load_wf(WF)
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "LoadImage":
            node["inputs"]["image"] = shot["img"]
        elif ct == "MiniMaxH3ImageToVideo":
            node["inputs"]["prompt"] = shot["prompt"]
        elif ct == "PrimitiveFloat":
            node["inputs"]["value"] = shot["dur"]
        elif ct == "RandomNoise":
            node["inputs"]["noise_seed"] = shot["seed"]
        elif ct == "BasicScheduler":
            node["inputs"]["steps"] = STEPS
        elif ct == "ResolutionSelector":
            node["inputs"]["megapixels"] = MEGAPIXELS
            node["inputs"]["aspect_ratio"] = "16:9 (Widescreen)"
        elif ct == "SaveVideo":
            node["inputs"]["filename_prefix"] = f"video/EP18_SHOT-{shot['shot']}_H3"
    return wf


def run_one(shot):
    sid = shot["shot"]
    print(f"\n── SHOT-{sid}: {shot['name']} ({shot['dur']}s · seed={shot['seed']})")
    frame = upload_frame(shot["img"])
    wf = build_workflow(shot)
    pid = queue(wf)
    print(f"    submitted {pid[:8]}... waiting (5–15 min)...")
    t0 = time.time()
    hist = wait(pid)
    saved = download(hist, OUT)
    print(f"    done in {int(time.time() - t0)}s")
    for fn in saved:
        mb = (OUT / fn).stat().st_size / (1024 * 1024)
        print(f"    ✅ {fn} ({mb:.1f}MB)")
    # 保持 ComfyUI 原始命名（EP18_SHOT-XX_H3_00001_.mp4），与已有 19 镜及 manifest 一致。
    return frame


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》H3 I2V 分镜视频生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--shot", type=str, help="按镜号筛选（如 01）")
    ap.add_argument("--limit", type=int, help="只跑前 N 镜")
    ap.add_argument("--skip-existing", action="store_true", help="跳过已出片的镜号（续跑用）")
    args = ap.parse_args()

    shots = [s for s in SHOTS if not args.shot or s["shot"] == args.shot]
    if args.limit:
        shots = shots[: args.limit]
    if args.skip_existing:
        shots = [s for s in shots if not any(OUT.glob(f"EP18_SHOT-{s['shot']}_H3_*"))]

    print("=" * 66)
    print(f" EP18《暖阳》H3 I2V  |  {len(shots)}/{len(SHOTS)} 镜  |  mp={MEGAPIXELS} steps={STEPS}")
    print(f" 帧目录: {FRAMES}\n 输出: {OUT}")
    print("=" * 66)
    for s in shots:
        print(f"  - SHOT-{s['shot']}  {s['name']}  {s['dur']}s  ← {s['img']}  seed={s['seed']}")
    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    ok_n = 0
    for i, s in enumerate(shots, 1):
        try:
            run_one(s)
            ok_n += 1
        except Exception as e:
            print(f"    ❌ {e}")
        time.sleep(1)
    print(f"\n{'=' * 66}\n 完成: {ok_n}/{len(shots)}  输出: {OUT}")


if __name__ == "__main__":
    main()

