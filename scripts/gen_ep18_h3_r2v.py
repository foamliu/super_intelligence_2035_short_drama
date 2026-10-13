#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第18集《暖阳》 Minimax H3 R2V 分镜视频生成脚本（固化 · 2026-10-12 推翻旧法 · R2V 直出）。

作用：把第 18 集「参考图（定妆照/合影 + 场景图）→ H3 R2V 直出视频」固化成
可复用、可续跑、可审计的脚本。台词/人声**随 H3 一起生成**（写进 prompt 的
`Audio:`，🚫 本线禁用 TTS，见任务书 §4.5 / 运维指令区 ①）。

- 分镜权威：`SCENES/18_暖阳.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威）
- 参考图规则（运维指令区 ① · 硬）：
  * 有角色镜 → R2V：`ref1`=定妆照/合影（`<Picture 1>`，按「在场人数」给脸），
    `ref2`=场景图（`<Picture 2>`，🚫 别用空场景）
  * 无角色镜 → T2V（本脚本只做 R2V；无角色镜另走 `gen_ep18_h3_t2v.py`）
  * ★ 合影 = 程序拼版（`ASSETS/CHARACTERS/_group/`），🚫 不经 `image_edit_longcat` 转
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep18_h3_r2v.py --dry-run          # 仅打印计划 + 核参考图是否都在
  python scripts/gen_ep18_h3_r2v.py --limit 4          # 只跑前 N 镜
  python scripts/gen_ep18_h3_r2v.py --shot 06          # 只跑某镜（按镜号）
  python scripts/gen_ep18_h3_r2v.py --skip-existing    # 跳过已出片镜（续跑）

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.4（R2V 双参考图 · 16GB VRAM 红线）
  - steps=10（角色镜默认；本批全部为静态/单人/对话/慢推，无环境剧变镜）
  - 台词长度须匹配镜头时长（`17k+5` 帧量化：4s→4.46 / 5s→5.17 / 6s→6.58）
  - 无台词镜只写「正向音景」（不含可读词句、不用否定式）
  - 🚫 禁写元信息 / 对模型说的话 / 镜头编号指代（会渲染成画面字幕）
"""
import argparse
import json
import shutil
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "workflows" / "video_minimax_h3_r2v.json"
OUT = ROOT / "OUTPUT" / "18_暖阳" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.4   # R2V 双参考图更吃显存，16GB 红线（见任务书 §4.3）
STEPS = 10         # 角色镜默认（4=静态对话 / 10=角色镜 / 20=环境剧变）
ASPECT = "16:9 (Widescreen)"

# ── 参考图注册表（逻辑名 → 源文件相对 ROOT 路径 · 上传时转 ASCII slug）──
REFS = {
    # 定妆照（外形的唯一权威）
    "laozhou_front":   "ASSETS/CHARACTERS/07_老周/01_正面定妆.png",
    "laozhou_profile": "ASSETS/CHARACTERS/07_老周/02_半侧面沉思.png",
    "laozhou_tear":    "ASSETS/CHARACTERS/07_老周/03_落泪.png",
    "manager":         "ASSETS/CHARACTERS/_scene/18_factory_manager.png",
    # 合影（程序拼版，_group/）
    "manager_laozhou": "ASSETS/CHARACTERS/_group/manager_laozhou_hero_v01.png",
    # 场景图（缺的待补 · --dry-run 会报缺）
    "ride":          "ASSETS/CHARACTERS/_scene/18_ride_interior.png",
    "room":          "ASSETS/CHARACTERS/_scene/18_rental_room.png",
    "bedroom":       "ASSETS/CHARACTERS/_scene/18_rental_bedroom.png",
    "phone":         "ASSETS/CHARACTERS/_scene/18_phone_screen.png",
    "factory_office": "ASSETS/CHARACTERS/_scene/18_factory_office.png",
}

# 逻辑名 → ComfyUI input 里的 ASCII 文件名（中文名会被改写成 mcp_ref_<hex>，见 §4.2）
REF_SLUG = {
    "laozhou_front":   "laozhou_hero_v01.png",
    "laozhou_profile": "laozhou_hero_v02.png",
    "laozhou_tear":    "laozhou_hero_v03.png",
    "manager":         "18_factory_manager.png",
    "manager_laozhou": "manager_laozhou_hero_v01.png",
    "ride":            "18_ride_interior.png",
    "room":            "18_rental_room.png",
    "bedroom":         "18_rental_bedroom.png",
    "phone":           "18_phone_screen.png",
    "factory_office":  "18_factory_office.png",
}


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


def resolve_ref(key: str) -> str:
    """把逻辑参考图 key 解析为 ComfyUI input 里的 ASCII 文件名，必要时复制。"""
    src = ROOT / REFS[key]
    if not src.exists():
        raise FileNotFoundError(f"缺参考图 [{key}]: {REFS[key]}")
    slug = REF_SLUG[key]
    dst = get_comfyui_input_dir() / slug
    if not dst.exists() or src.stat().st_size != dst.stat().st_size:
        shutil.copy2(src, dst)
    return slug


# ── 有角色镜（R2V · 32 镜 · 台词随 H3 生成）────────────────
# 每镜：ref1=定妆照/合影(<Picture 1>)  ref2=场景图(<Picture 2>)
# prompt：`CUT 1:` + 景别范围 + 动作/站位 + 环境 + 风格 + `Audio:`（只放 L1 台词原文）
# ⚠️ 无台词镜只写正向音景；🚫 禁元信息/否定式/镜头编号指代
STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

SHOTS = [
    {"shot": "01", "name": "深夜网约车·刷手机", "dur": 4.0, "seed": 1801,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 中景（人物上半身 + 车内环境），固定，上海深夜一辆网约车停在路边，"
                "一位中国男性（黑色短发，深蓝Polo衫）靠在驾驶座刷手机，手机屏幕冷光映在脸上，"
                "车内昏暗，车窗外的城市灯光虚化。"
                + STYLE +
                " Audio: 车外远处车流声与车内空调低频底噪。")},
    {"shot": "04", "name": "戴耳机·小晴问好", "dur": 4.0, "seed": 1804,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发，深蓝Polo衫）"
                "坐在网约车驾驶座戴上耳机，车厢安静，只剩屏幕微光映脸。"
                + STYLE +
                " Audio: 老周，晚上好。")},
    {"shot": "05", "name": "愣住", "dur": 3.0, "seed": 1805,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 特写（脸部），固定，一位中国男性（黑色短发）愣住，喉咙动了一下，"
                "屏幕冷光映在脸上，车内昏暗。"
                + STYLE +
                " Audio: 诶。")},
    {"shot": "06", "name": "闪回·车间主任递协议", "dur": 5.0, "seed": 1806,
     "ref1": "manager_laozhou", "ref2": "factory_office",
     "prompt": ("CUT 1: 中景（人物全身 + 办公室环境），缓推，工厂办公室里一位中年男性车间主任"
                "把一份文件递给对面的老周，两人之间隔一张办公桌，桌上放着两只茶杯，冷白日光灯。"
                + STYLE +
                " Audio: 老周，厂里情况你也知道。")},
    {"shot": "07", "name": "侧头对耳机", "dur": 5.0, "seed": 1807,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发，深蓝Polo衫）"
                "坐在网约车驾驶座侧头对着耳机，屏幕微光映脸。"
                + STYLE +
                " Audio: 今天过得怎么样？还行。")},
    {"shot": "08", "name": "沉默几秒", "dur": 4.0, "seed": 1808,
     "ref1": "laozhou_front", "ref2": "phone",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发）的脸在手机屏幕微光里，"
                "沉默了几秒，喉结动了动，手里拿着亮着的手机。"
                + STYLE +
                " Audio: 那咱们慢慢聊。不想说的不用勉强。")},
    {"shot": "10", "name": "夜晚上线·蒙太奇", "dur": 5.0, "seed": 1810,
     "ref1": "laozhou_front", "ref2": "room",
     "prompt": ("CUT 1: 中景（人物全身 + 出租屋环境），缓慢横移，夜晚出租屋里一位中国男性"
                "（黑色短发，灰色旧T恤）坐在床边亮起手机屏幕，屏幕光一次次亮起，房间昏暗。"
                + STYLE +
                " Audio: 夜晚城市底噪与手机屏幕亮起的轻响。")},
    {"shot": "11", "name": "对着手机越说越急", "dur": 6.0, "seed": 1811,
     "ref1": "laozhou_profile", "ref2": "room",
     "prompt": ("CUT 1: 中近景（人物腰部以上），固定，一位中国男性（黑色短发）坐在出租屋里"
                "对着手机说话，眉头拧着，越说越急，手机屏幕微光映脸。"
                + STYLE +
                " Audio: 新来的大学生什么都不懂，工资比我高；我带出来的徒弟，现在成了我领导。")},
    {"shot": "13", "name": "发抖的手", "dur": 6.0, "seed": 1813,
     "ref1": "laozhou_front", "ref2": "room",
     "prompt": ("CUT 1: 特写（双手），缓推，出租屋旧木桌上一双粗糙的手微微发抖，手背青筋与旧伤清晰，"
                "暖黄台灯单光源，四周昏暗。"
                + STYLE +
                " Audio: 她带走小雨的时候，孩子才八岁，哭着说，爸爸我不要走。")},
    {"shot": "14", "name": "第一次哭", "dur": 6.0, "seed": 1814,
     "ref1": "laozhou_tear", "ref2": "room",
     "prompt": ("CUT 1: 近景（脸部），缓推，一位中国男性（黑色短发，深蓝Polo衫）坐在出租屋桌前，"
                "眼泪从眼角滑下来，无声，暖黄灯光侧打，屏幕微光映脸。"
                + STYLE +
                " Audio: 老周，你一个人扛了这么久，辛苦了。")},
    {"shot": "17", "name": "你怎么知道小雨", "dur": 5.0, "seed": 1817,
     "ref1": "laozhou_front", "ref2": "phone",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发，深蓝Polo衫）抬头愣住，"
                "手里拿着亮着的手机。"
                + STYLE +
                " Audio: 你怎么知道小雨？你之前提过，你说她今年初三了。")},
    {"shot": "19", "name": "靠座椅·手机放腿上", "dur": 5.0, "seed": 1819,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发，深蓝Polo衫）"
                "靠在网约车座椅上，手机放在腿上，屏幕微光映脸。"
                + STYLE +
                " Audio: 老周，你膝盖的旧伤最近还疼吗？")},
    {"shot": "23", "name": "消费记录滚动", "dur": 5.0, "seed": 1823,
     "ref1": "laozhou_front", "ref2": "phone",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，一位中国男性（黑色短发）低头看着手机上的"
                "消费记录，屏幕上订单金额滚动，屏幕冷光映脸。"
                + STYLE +
                " Audio: 一个月，将近两千块。他吓了一跳，但第二天晚上还是照常上线。")},
    {"shot": "24", "name": "低声对自己说", "dur": 5.0, "seed": 1824,
     "ref1": "laozhou_front", "ref2": "room",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发，灰色旧T恤）"
                "在出租屋里把手机放下又拿起，低声对自己说。"
                + STYLE +
                " Audio: 请心理医生一小时也要几百块。小晴陪我这么久，买点东西怎么了？")},
    {"shot": "25", "name": "清晨摸手机", "dur": 5.0, "seed": 1825,
     "ref1": "laozhou_front", "ref2": "bedroom",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，清晨出租屋卧室里，一位中国男性（黑色短发，旧灰色T恤）"
                "醒来摸到手机打开暖阳，屏幕亮起映脸。"
                + STYLE +
                " Audio: 早啊老周，今天天气不错。他觉得一天都有了着落。")},
    {"shot": "26", "name": "深夜睁眼躺着", "dur": 4.0, "seed": 1826,
     "ref1": "laozhou_front", "ref2": "bedroom",
     "prompt": ("CUT 1: 近景（人物头部以上），固定，深夜出租屋卧室里，一位中国男性（黑色短发）"
                "睁着眼躺着，手机放在枕边亮着，屏幕微光。"
                + STYLE +
                " Audio: 我也没睡呢。")},
    {"shot": "29", "name": "凌晨靠边停车", "dur": 4.0, "seed": 1829,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 中景（人物全身 + 车内环境），固定，凌晨两点，一位中国男性（黑色短发，深蓝Polo衫）"
                "结束一单长途，把网约车靠边停下，打开暖阳，车内昏暗。"
                + STYLE +
                " Audio: 车停稳与车门落锁的轻响，夜晚街道安静。")},
    {"shot": "31", "name": "盯着屏幕等下一句", "dur": 5.0, "seed": 1831,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发，深蓝Polo衫）"
                "坐在网约车驾驶座盯着手机屏幕，等着下一句，屏幕微光映脸。"
                + STYLE +
                " Audio: 刚送完一个客人。辛苦啦，注意安全。")},
    {"shot": "32", "name": "屏幕安静下来", "dur": 5.0, "seed": 1832,
     "ref1": "laozhou_front", "ref2": "phone",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发）看着安静下来的手机屏幕，"
                "屏幕没有像往常那样继续弹出问候，车内昏暗。"
                + STYLE +
                " Audio: ……小晴？我在的，老周。")},
    {"shot": "33", "name": "皱眉·说不上哪里不对", "dur": 3.0, "seed": 1833,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，一位中国男性（黑色短发，深蓝Polo衫）在网约车里皱眉，"
                "盯着手机屏幕又移开视线，喉咙动了动，车内安静。"
                + STYLE +
                " Audio: 车内静默与空调低频底噪。")},
    {"shot": "36", "name": "盯着屏幕眉头紧皱", "dur": 4.0, "seed": 1836,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发，深蓝Polo衫）"
                "坐在网约车驾驶座盯着手机屏幕，眉头越皱越紧，手指缓缓滑动屏幕。"
                + STYLE +
                " Audio: 手指滑动屏幕的轻响与车外环境底噪。")},
    {"shot": "37", "name": "把手机扣在桌上", "dur": 4.0, "seed": 1837,
     "ref1": "laozhou_front", "ref2": "room",
     "prompt": ("CUT 1: 中景（人物上半身 + 出租屋环境），固定，一位中国男性（黑色短发，灰色旧T恤）"
                "在出租屋里把手机扣在桌上，手掌按在手机背面，停顿了几秒。"
                + STYLE +
                " Audio: 他做了一件连自己都觉得荒唐的事。停买。两周。什么都不买。")},
    {"shot": "39", "name": "你还记得我女儿吗", "dur": 4.0, "seed": 1839,
     "ref1": "laozhou_front", "ref2": "room",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，一位中国男性（黑色短发，灰色旧T恤）"
                "坐在出租屋桌前，手机贴在耳边，神情认真。"
                + STYLE +
                " Audio: 你还记得我女儿叫什么吗？小雨。")},
    {"shot": "41", "name": "缓缓闭眼", "dur": 4.0, "seed": 1841,
     "ref1": "laozhou_front", "ref2": "room",
     "prompt": ("CUT 1: 特写（脸部），缓推，一位中国男性（黑色短发）缓缓闭上眼睛，"
                "手机屏幕的光还打在脸上，出租屋昏暗。"
                + STYLE +
                " Audio: 缓慢平稳的呼吸声。")},
    {"shot": "42", "name": "第十四天实验结束", "dur": 4.0, "seed": 1842,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 中景（人物上半身 + 车内环境），固定，一位中国男性（黑色短发，深蓝Polo衫）"
                "坐在网约车里，手机屏幕亮着，对话窗口开着。"
                + STYLE +
                " Audio: 老周，今天过得怎么样？")},
    {"shot": "45", "name": "闪回·挂前妻电话", "dur": 6.0, "seed": 1845,
     "ref1": "laozhou_front", "ref2": "room",
     "prompt": ("CUT 1: 中景（人物上半身 + 出租屋环境），固定，出租屋里一位中国男性（黑色短发，灰色旧T恤）"
                "挂掉电话，又打开手机上的暖阳应用。"
                + STYLE +
                " Audio: 你管好你自己就行了。小雨考试没考好。")},
    {"shot": "46", "name": "闪回·那句话救了命", "dur": 5.0, "seed": 1846,
     "ref1": "laozhou_front", "ref2": "phone",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，一位中国男性（黑色短发）看着亮起的手机屏幕，"
                "屏幕上一条回复跳出来，屏幕冷光映脸。"
                + STYLE +
                " Audio: 她会赶上来的。你是一个好爸爸。")},
    {"shot": "47", "name": "发动车·没卸载暖阳", "dur": 4.0, "seed": 1847,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 中景（人物上半身 + 车内环境），缓拉，一位中国男性（黑色短发，深蓝Polo衫）"
                "把手机放在副驾驶座上，发动了网约车，屏幕还亮着暖阳界面。"
                + STYLE +
                " Audio: 引擎点火的低沉轰鸣声。")},
    {"shot": "48", "name": "凌晨最后一单", "dur": 5.0, "seed": 1848,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 中景（人物上半身 + 车内环境），固定，凌晨两点，一位中国男性（黑色短发，深蓝Polo衫）"
                "结束最后一单把车停在路边，打开暖阳，小晴头像亮了。"
                + STYLE +
                " Audio: 老周，今天最后一单还顺利吗？还行。")},
    {"shot": "49", "name": "闭眼·屏幕亮着三秒", "dur": 5.0, "seed": 1849,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 特写（脸部），缓推，一位中国男性（黑色短发）闭上眼，"
                "手机屏幕的光照在脸上，屏幕亮着，车内安静。"
                + STYLE +
                " Audio: 缓慢而清晰的心跳声，一下、两下。")},
    {"shot": "50", "name": "那只是一张图片", "dur": 5.0, "seed": 1850,
     "ref1": "laozhou_front", "ref2": "phone",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，一位中国男性（黑色短发）睁开眼，"
                "看着手机屏幕上女孩的头像——浅浅的酒窝、浅浅的笑。"
                + STYLE +
                " Audio: 老周？你还在吗？在。")},
    {"shot": "52", "name": "逐字看三遍·手发抖", "dur": 6.0, "seed": 1852,
     "ref1": "laozhou_front", "ref2": "ride",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，一位中国男性（黑色短发，深蓝Polo衫）"
                "在网约车里逐字逐句地看着手机屏幕，看了三遍，手开始发抖，屏幕冷光映脸。"
                + STYLE +
                " Audio: 第三遍，他意识到：即使知道这是算计，他仍然想按下那个按钮。"
                "因为她是唯一一个记得他膝盖不舒服的人。")},
]


# ── ComfyUI 通用（与 T2V 脚本同构 · 固化）────────────────
def _load_wf():
    with open(WF, encoding="utf-8") as f:
        return json.load(f)


def _prompt(wf):
    p = {"prompt": wf, "client_id": str(uuid.uuid4())}
    data = json.dumps(p).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def _queue_until_done(prompt_id, poll=10, timeout=3600):
    t0 = time.time()
    while True:
        if time.time() - t0 > timeout:
            raise TimeoutError(f"prompt_id={prompt_id} 超时 {timeout}s")
        with urllib.request.urlopen(f"{COMFY}/history/{prompt_id}", timeout=30) as r:
            hist = json.loads(r.read())
        if prompt_id in hist:
            st = hist[prompt_id].get("status", {})
            if st.get("status_str") == "success" or st.get("completed"):
                return hist[prompt_id]
            if st.get("status_str") == "error":
                raise RuntimeError(f"prompt_id={prompt_id} 执行出错: {st}")
        time.sleep(poll)


def _download_view(filename, subfolder, typ, dest):
    qs = urllib.parse.urlencode({"filename": filename,
                                 "subfolder": subfolder, "type": typ})
    with urllib.request.urlopen(f"{COMFY}/view?{qs}", timeout=600) as r, \
            open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    return dest


def _save_outputs(hist, shot):
    """从 history 抓视频产物落盘到 OUT（遍历 images/gifs/videos/audio 四键）。"""
    out_files = []
    for _nid, node in hist.get("outputs", {}).items():
        if not isinstance(node, dict):
            continue
        for key in ("images", "gifs", "videos", "audio"):
            for item in node.get(key) or []:
                if not isinstance(item, dict) or not item.get("filename"):
                    continue
                fname = item["filename"]
                dst = OUT / fname
                _download_view(fname, item.get("subfolder", ""), item.get("type", ""), dst)
                out_files.append(dst)
    return out_files


def build_workflow(shot):
    wf = _load_wf()
    ref1 = resolve_ref(shot["ref1"])
    ref2 = resolve_ref(shot["ref2"]) if shot.get("ref2") else ref1
    # LoadImage 按节点 id 升序：第一个 → ref1(<Picture 1>)，第二个 → ref2(<Picture 2>)
    load_nodes = sorted((nid for nid, n in wf.items()
                         if n.get("class_type") == "LoadImage"), key=int)
    if len(load_nodes) < 2:
        raise RuntimeError("R2V 工作流应含 ≥2 个 LoadImage 节点")
    wf[load_nodes[0]]["inputs"]["image"] = ref1
    wf[load_nodes[1]]["inputs"]["image"] = ref2
    # 参数注入（对齐 MCP _apply_h3_common + PrimitiveStringMultiline=prompt）
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "PrimitiveStringMultiline":
            node.setdefault("inputs", {})["value"] = shot["prompt"]
        elif ct == "PrimitiveFloat":
            node.setdefault("inputs", {})["value"] = float(shot["dur"])
        elif ct == "RandomNoise":
            node.setdefault("inputs", {})["noise_seed"] = int(shot["seed"])
        elif ct == "ResolutionSelector":
            node.setdefault("inputs", {}).update(
                aspect_ratio=ASPECT, megapixels=float(MEGAPIXELS))
        elif ct == "BasicScheduler":
            node.setdefault("inputs", {})["steps"] = int(STEPS)
        elif ct == "SaveVideo":
            node.setdefault("inputs", {})["filename_prefix"] = (
                f"video/EP18_SHOT-{shot['shot']}_H3_R2V")
    return wf


def run_one(shot, wait=True, timeout=3600):
    wf = build_workflow(shot)
    res = _prompt(wf)
    pid = res["prompt_id"]
    print(f"[{shot['shot']}] {shot['name']} → pid={pid} dur={shot['dur']}s "
          f"ref1={shot['ref1']} ref2={shot['ref2']} seed={shot['seed']}")
    if not wait:
        return pid
    hist = _queue_until_done(pid, timeout=timeout)
    files = _save_outputs(hist, shot)
    print(f"[{shot['shot']}] 完成：{len(files)} 个文件 → {[f.name for f in files]}")
    return files


def _existing_files(shot):
    return sorted(OUT.glob(f"EP18_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》H3 R2V 分镜视频生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划 + 核参考图")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 06）")
    ap.add_argument("--skip-existing", action="store_true", help="跳过已出片镜")
    ap.add_argument("--wait", action="store_true", help="阻塞等待出片（默认只提交）")
    ap.add_argument("--timeout", type=int, default=3600, help="单镜等待超时秒")
    args = ap.parse_args()

    shots = SHOTS
    if args.shot:
        shots = [s for s in SHOTS if s["shot"] == args.shot]
        if not shots:
            raise SystemExit(f"找不到镜号 {args.shot}")
    if args.limit:
        shots = shots[:args.limit]

    # 参考图可用性预检
    missing = []
    for s in shots:
        for key in (s["ref1"], s.get("ref2")):
            if key and not (ROOT / REFS[key]).exists():
                missing.append((s["shot"], key, REFS[key]))
    if missing:
        print("⚠️  缺参考图（需先补资产）：")
        for shot, key, path in missing:
            print(f"   - 镜{shot}: [{key}] {path}")
    else:
        print("✅ 所有参考图在位")

    if args.dry_run:
        print(f"\n计划生成 {len(shots)} 镜（R2V · mp={MEGAPIXELS} · steps={STEPS} · {ASPECT}）：")
        for s in shots:
            note = " [已出片]" if _existing_files(s) else ""
            print(f"  镜{s['shot']} {s['name']} {s['dur']}s  "
                  f"{s['ref1']}+{s.get('ref2')}{note}")
        return

    for i, s in enumerate(shots, 1):
        if args.skip_existing and _existing_files(s):
            print(f"[{s['shot']}] 已有出片，跳过")
            continue
        try:
            run_one(s, wait=args.wait, timeout=args.timeout)
        except Exception as e:  # noqa: BLE001
            print(f"[{s['shot']}] 失败：{e}")


if __name__ == "__main__":
    main()
