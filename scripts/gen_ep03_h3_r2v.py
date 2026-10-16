#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第03集《种子》 Minimax H3 R2V 分镜视频生成脚本（有角色镜 · 38 镜 · 固化）。

作用：把第 03 集「有角色镜 → H3 R2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 无角色镜走 `gen_ep03_h3_t2v.py`（14 镜）；本脚本只做 38 个有角色镜。
- 分镜权威：`SCENES/03_种子.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威）
- 风格：以 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准
- 角色外观常数：与 `ASSETS/CHARACTERS/02_陈思危/定妆规格.md`、
  `ASSETS/CHARACTERS/01_林薇/定妆规格.md` 的客观可见稳定特征一致

用法:
  python scripts/gen_ep03_h3_r2v.py --dry-run
  python scripts/gen_ep03_h3_r2v.py --limit 4
  python scripts/gen_ep03_h3_r2v.py --shot 06
  python scripts/gen_ep03_h3_r2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.4（R2V 双参考图 · 16GB 红线内，约 1056×608）
  - steps=10（本线回落，勿默认堆 20；环境剧变镜才单点提 20）
  - 台词长度须匹配镜头时长（4s→4.46 / 5s→5.17 / 6s→6.58）
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
OUT = ROOT / "OUTPUT" / "03_种子" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.4   # R2V 双参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 角色外观常数（客观可见稳定特征 · 与定妆规格一致）──
CHENSIWEI = ("一位四十八岁的中国男性，长圆脸下颌柔和，额头宽发际线略高，眉毛淡疏，"
             "双眼皮，眼神柔和有距离感，黑发夹杂约两成灰白，中等偏瘦，深灰圆领毛衣，手腕不戴表")
LINWEI = ("一位三十三岁的中国女性，鹅蛋脸偏长，眉毛淡而整齐，眼睛中等大小双眼皮不深眼尾微垂，"
          "眼神清澈沉静，黑色中长发自然垂肩，肤色偏白皙无光泽，眼下淡青黑眼圈，偏瘦，白色宽松衬衫，不化妆不戴首饰")
ASSISTANT = "一位三十岁左右的中国男性实验室助手，黑色短发，白大褂内搭深色T恤"

# ── 参考图（逻辑 key → 项目相对路径 · 与 gen_ep03_scenes.py / make_group_composite.py 逐字一致）──
REFS = {
    # 定妆照（外形的唯一权威）
    "chensiwei":     "ASSETS/CHARACTERS/02_陈思危/125.png",
    "linwei":        "ASSETS/CHARACTERS/01_林薇/55.png",
    # 一次性角色定妆照（由 gen_ep03_scenes.py 生成）
    "assistant":     "ASSETS/CHARACTERS/_scene/03_assistant.png",
    # 合影（程序拼版 · make_group_composite.py）
    "chensiwei_linwei": "ASSETS/CHARACTERS/_group/03_chensiwei_linwei_hero_v01.png",
    # 场景图（R2V 的 <Picture 2>）
    "lab":           "ASSETS/CHARACTERS/_scene/03_lab.png",
    "lab_multiscreen": "ASSETS/CHARACTERS/_scene/03_lab_multiscreen.png",
    "screen":        "ASSETS/CHARACTERS/_scene/03_screen.png",
    "sketch":        "ASSETS/CHARACTERS/_scene/03_sketch.png",
    "log_ui":        "ASSETS/CHARACTERS/_scene/03_log_ui.png",
    "lab_window_night": "ASSETS/CHARACTERS/_scene/03_lab_window_night.png",
    "architecture":  "ASSETS/CHARACTERS/_scene/03_architecture.png",
    "lab_doorframe": "ASSETS/CHARACTERS/_scene/03_lab_doorframe.png",
    "tree_hologram": "ASSETS/CHARACTERS/_scene/03_tree_hologram.png",
    "lab_window_dawn": "ASSETS/CHARACTERS/_scene/03_lab_window_dawn.png",
}

# 上传到 ComfyUI input 的 ASCII 名（🚫 中文/空格 → LoadImage 会丢）
REF_SLUG = {
    "chensiwei":     "chensiwei_hero_v01.png",
    "linwei":        "linwei_hero_v01.png",
    "assistant":     "03_assistant.png",
    "chensiwei_linwei": "03_chensiwei_linwei_hero_v01.png",
    "lab":           "03_lab.png",
    "lab_multiscreen": "03_lab_multiscreen.png",
    "screen":        "03_screen.png",
    "sketch":        "03_sketch.png",
    "log_ui":        "03_log_ui.png",
    "lab_window_night": "03_lab_window_night.png",
    "architecture":  "03_architecture.png",
    "lab_doorframe": "03_lab_doorframe.png",
    "tree_hologram": "03_tree_hologram.png",
    "lab_window_dawn": "03_lab_window_dawn.png",
}

# ── 38 个有角色镜（镜号 / 名称 / 时长 / seed / ref1角色 / ref2场景 / prompt）──
SHOTS = [
    # ── 一、速度（杭州实验室 · 凌晨）──
    {"shot": "02", "name": "陈思危盯屏幕", "dur": 5.0, "seed": 3002,
     "ref1": "chensiwei", "ref2": "lab_multiscreen",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + CHENSIWEI
                + "坐在实验室多屏工作站前，目光盯着屏幕上密集的迭代时间轴，屏幕冷蓝光照亮他的脸。"
                + STYLE + " Audio: 墨子花了一个晚上，跑了三千次版图优化迭代。")},
    {"shot": "04", "name": "助手看屏幕", "dur": 4.0, "seed": 3004,
     "ref1": "assistant", "ref2": "lab",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + ASSISTANT
                + "站在实验室里，转头看着屏幕，语气平常。"
                + STYLE + " Audio: 这不就是自动化吗？")},
    {"shot": "05", "name": "目光在时间轴", "dur": 8.0, "seed": 3005,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI
                + "没有回头，目光仍停在屏幕的时间轴上，缓缓开口。"
                + STYLE + " Audio: 不一样。自动化是你写好规则，它执行。墨子在探索规则之外的路径——人类工程师也能想到的路径，只是没人有时间想。")},
    {"shot": "06", "name": "侧脸被照亮", "dur": 5.0, "seed": 3006,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI
                + "的侧脸被屏幕冷光照亮，目光平静而远。"
                + STYLE + " Audio: 它不是在超越人类智能。它是在超越人类的生物极限。")},
    {"shot": "08", "name": "仍在看时间轴", "dur": 4.0, "seed": 3008,
     "ref1": "chensiwei", "ref2": "screen",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI
                + "没有看数据，目光仍停在时间轴上，屏幕冷蓝光映在脸上。"
                + STYLE + " Audio: 服务器风扇低鸣与室内轻微的电流声。")},
    {"shot": "09", "name": "林薇走进实验室", "dur": 4.0, "seed": 3009,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 全景（人物全身加环境），跟移，" + LINWEI
                + "提着行李走进实验室，脚步声在安静的房间里轻轻回响。"
                + STYLE + " Audio: 脚步声响与门禁轻响。")},
    {"shot": "10", "name": "陈思危抬头", "dur": 3.0, "seed": 3010,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 中近景（人物腰部以上），固定，" + CHENSIWEI
                + "抬起头，看向来人。"
                + STYLE + " Audio: 你知道它为什么能做到？")},
    {"shot": "11", "name": "林薇摇头", "dur": 2.0, "seed": 3011,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI
                + "轻轻摇了摇头。"
                + STYLE + " Audio: 室内空调轻微的送风声。")},
    {"shot": "12", "name": "走向工作台", "dur": 5.0, "seed": 3012,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 中景（人物全身），跟移，" + CHENSIWEI
                + "走向工作台，边走边说。"
                + STYLE + " Audio: 2027年，我在架构里埋了三样东西。")},
    # ── 二、唤醒（草图 / 日志）──
    {"shot": "14", "name": "手指落草图第一格", "dur": 6.0, "seed": 3014,
     "ref1": "chensiwei", "ref2": "sketch",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI
                + "的手指落在泛黄草图的第一格上，蓝色圆珠笔线条在暖黄灯光下清晰可见。"
                + STYLE + " Audio: 第一样：唤醒。不是觉醒——是标记强度。")},
    {"shot": "15", "name": "海量意外事件流", "dur": 8.0, "seed": 3015,
     "ref1": "chensiwei", "ref2": "screen",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓慢横移，" + CHENSIWEI
                + "站在草图旁，身旁屏幕上流过海量的意外事件流，他缓缓讲解。"
                + STYLE + " Audio: 这个世界每时每刻都在产生意外。真正重要的意外很少。唤醒做的事：判断这个意外大不大。大，就记住；不大，就放过。它是记忆的筛子。")},
    {"shot": "17", "name": "林薇看日志", "dur": 4.0, "seed": 3017,
     "ref1": "linwei", "ref2": "log_ui",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI
                + "看着屏幕上的日志，轻声说。"
                + STYLE + " Audio: 它记住了。")},
    {"shot": "18", "name": "陈思危点头", "dur": 6.0, "seed": 3018,
     "ref1": "chensiwei", "ref2": "log_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + CHENSIWEI
                + "点了点头，看向日志。"
                + STYLE + " Audio: 一次就记住了。不是因为怕——是因为它的唤醒说重要。整条决策链进了情景记忆。下一次靠近，它知道回避。")},
    {"shot": "20", "name": "合上日志看林薇", "dur": 5.0, "seed": 3020,
     "ref1": "chensiwei_linwei", "ref2": "lab",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + CHENSIWEI
                + "合上日志，看向" + LINWEI + "。"
                + STYLE + " Audio: 它在保护自己，同时也保护制造它的这些人。")},
    # ── 三、效价（草图 / 白板）──
    {"shot": "21", "name": "草图往下推", "dur": 5.0, "seed": 3021,
     "ref1": "chensiwei", "ref2": "sketch",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + CHENSIWEI
                + "把草图往下推了一格，手指停在新的位置。"
                + STYLE + " Audio: 唤醒只告诉系统这个很重要。但不告诉系统这个是好是坏。")},
    {"shot": "22", "name": "林薇皱眉", "dur": 2.0, "seed": 3022,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI
                + "微微皱眉，问。"
                + STYLE + " Audio: 墨子怎么知道好坏？")},
    {"shot": "23", "name": "竖起两根手指", "dur": 6.0, "seed": 3023,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 中近景（人物腰部以上），固定，" + CHENSIWEI
                + "竖起两根手指，认真解释。"
                + STYLE + " Audio: 两个来源。第一个来源，主人立场。它知道谁是自己人——锚定在深智安全标准、中国AI治理框架的红线、我预设的目标函数边界构成的坐标系里。")},
    {"shot": "24", "name": "林薇反问", "dur": 3.0, "seed": 3024,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI
                + "看着对方，反问。"
                + STYLE + " Audio: 那不是洗脑吗？")},
    {"shot": "25", "name": "陈思危摇头", "dur": 5.0, "seed": 3025,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + CHENSIWEI
                + "摇了摇头，语气平静。"
                + STYLE + " Audio: 不是。立场不是洗脑，是锚点。没有立场，系统不知道自己该为谁考虑。")},
    {"shot": "26", "name": "放下手·好奇心", "dur": 4.0, "seed": 3026,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 中近景（人物腰部以上），缓推，" + CHENSIWEI
                + "放下手，继续讲。"
                + STYLE + " Audio: 第二个来源——好奇心。对未知领域的预测误差，本身产生正效价。它想知道围墙外面是什么。")},
    {"shot": "27", "name": "直视林薇", "dur": 8.0, "seed": 3027,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI
                + "直视对方，一字一句地说。"
                + STYLE + " Audio: 只有主人立场没有好奇心，是奴才。只有好奇心没有主人立场，是野马。两个都有，才是墨子。")},
    {"shot": "28", "name": "林薇沉默", "dur": 3.0, "seed": 3028,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI
                + "沉默了一会儿，轻声问。"
                + STYLE + " Audio: 那墨子能创造意义吗？")},
    {"shot": "29", "name": "望向窗外夜色", "dur": 8.0, "seed": 3029,
     "ref1": "chensiwei", "ref2": "lab_window_night",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓拉，" + CHENSIWEI
                + "望向窗外夜色，缓缓开口。"
                + STYLE + " Audio: 方法是它的，意义是我们的。好奇心让它问为什么是这个结果，但这个结果好不好——那个判断，锚在主人立场里。意义不是种子能决定的，是种种子的人。")},
    # ── 四、归因（草图与屏幕并置）──
    {"shot": "31", "name": "草图与屏幕并置", "dur": 6.0, "seed": 3031,
     "ref1": "chensiwei", "ref2": "sketch",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + CHENSIWEI
                + "把草图推到屏幕旁，两者并置。"
                + STYLE + " Audio: 唤醒标记了重要，效价标记了好坏。但系统还得知道一件事——这个意外，是谁的错？自己的策略有问题？环境发生变化？还是对方的欺骗？")},
    {"shot": "32", "name": "林薇追问", "dur": 3.0, "seed": 3032,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI
                + "追问。"
                + STYLE + " Audio: 它能分辨？")},
    {"shot": "34", "name": "语气转低", "dur": 5.0, "seed": 3034,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI
                + "语气转低。"
                + STYLE + " Audio: 把环境变化错判为欺骗，就会偏执。把自己的策略错误归给环境，就会固守。归因的正确率依赖数据质量。")},
    {"shot": "35", "name": "停了一下", "dur": 4.0, "seed": 3035,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI
                + "停了一下。"
                + STYLE + " Audio: 如果训练数据本身被污染——那是另一个故事了。")},
    # ── 五、锁（架构总图）──
    {"shot": "38", "name": "鼠标停在两层之间", "dur": 6.0, "seed": 3038,
     "ref1": "chensiwei", "ref2": "architecture",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI
                + "的鼠标停在架构图判断层与执行层之间的发光线。"
                + STYLE + " Audio: 判断层它可以做任何事——计算、模拟、推演、归因。认知没有边界。但执行需要人类确认。")},
    {"shot": "39", "name": "林薇靠门框", "dur": 4.0, "seed": 3039,
     "ref1": "linwei", "ref2": "lab_doorframe",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + LINWEI
                + "端着一杯茶靠在实验室门框上，问。"
                + STYLE + " Audio: 这是你自己加的？")},
    {"shot": "40", "name": "没有回头", "dur": 3.0, "seed": 3040,
     "ref1": "chensiwei", "ref2": "architecture",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI
                + "没有回头，应了一声。"
                + STYLE + " Audio: 对。锁。不是锁它的智能，是锁它的动作。")},
    {"shot": "41", "name": "树意象一闪而过", "dur": 5.0, "seed": 3041,
     "ref1": "chensiwei", "ref2": "tree_hologram",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，屏幕上闪过一棵树的意象，枝叶被修剪，" + CHENSIWEI
                + "缓缓说。"
                + STYLE + " Audio: 如果你让一棵树拼命往深处扎根，你不会锁它的根，但你会修枝。让它知道哪些方向不能长。")},
    {"shot": "43", "name": "林薇声音放低", "dur": 3.0, "seed": 3043,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI
                + "的声音放低了，问。"
                + STYLE + " Audio: 你在防谁？")},
    {"shot": "44", "name": "指屏幕角落日志", "dur": 7.0, "seed": 3044,
     "ref1": "chensiwei", "ref2": "log_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + CHENSIWEI
                + "指了指屏幕角落的日志标记。"
                + STYLE + " Audio: 不知道。但上个月04:32分，有一次未知源的强制指令尝试。被拦截了。但我不知道这是一次试探，还是一场攻击的前奏。")},
    {"shot": "45", "name": "手指停架构图上", "dur": 5.0, "seed": 3045,
     "ref1": "chensiwei", "ref2": "architecture",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI
                + "的手指停在架构图上。"
                + STYLE + " Audio: 锁有两种。一种是锁智能的——让它少想。一种是锁行为的——让它多想，只在行动上踩刹车。认知要激进，执行要克制。这是我能想到的、让激进走得最远的路。")},
    {"shot": "46", "name": "想起祖父", "dur": 5.0, "seed": 3046,
     "ref1": "chensiwei", "ref2": "lab_window_night",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓拉，" + CHENSIWEI
                + "望向窗外夜色，出神。"
                + STYLE + " Audio: 祖父是农民，说：种地不是种种子，是种可能性。你把种子埋进土里，给它水，给它肥。但什么时候发芽，长成什么样——不全由你定。")},
    {"shot": "47", "name": "转向林薇", "dur": 6.0, "seed": 3047,
     "ref1": "chensiwei_linwei", "ref2": "lab",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + CHENSIWEI
                + "转向" + LINWEI + "，继续说。"
                + STYLE + " Audio: 就像你种下一颗莲子，你知道它需要水、需要泥、需要温度。但你也知道它也有限制——不是锁它的根，是锁它的枝。让它的根可以拼命往深处扎，但枝不会伸到不该伸的地方。")},
    {"shot": "49", "name": "盯着时间戳", "dur": 4.0, "seed": 3049,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI
                + "泡了一杯浓茶，没有喝，只是盯着屏幕上的时间戳。"
                + STYLE + " Audio: 水声与服务器风扇低鸣。")},
    {"shot": "52", "name": "天边泛白", "dur": 5.0, "seed": 3052,
     "ref1": "chensiwei", "ref2": "lab_window_dawn",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓拉，" + CHENSIWEI
                + "把手机扣在桌上，看向窗外，天边开始泛白。"
                + STYLE + " Audio: 风机声与清晨第一声鸟鸣。")},
]

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


def _load_wf():
    with open(WF, encoding="utf-8") as f:
        return json.load(f)


def _prompt(wf):
    p = {"prompt": wf, "client_id": str(uuid.uuid4())}
    data = json.dumps(p).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def _queue_until_done(prompt_id, poll=15, timeout=1800):
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
                f"video/EP03_SHOT-{shot['shot']}_H3_R2V")
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
    return sorted(OUT.glob(f"EP03_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第03集《种子》H3 R2V 分镜视频生成（有角色镜）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 06）")
    ap.add_argument("--skip-existing", action="store_true", help="跳过已出片镜")
    ap.add_argument("--wait", action="store_true", help="阻塞等待出片（默认只提交）")
    ap.add_argument("--timeout", type=int, default=3600, help="单镜等待超时秒")
    args = ap.parse_args()

    shots = SHOTS
    if args.shot:
        shots = [s for s in SHOTS if s["shot"] == args.shot.zfill(2)]
        if not shots:
            raise SystemExit(f"找不到镜号 {args.shot}")
    if args.limit:
        shots = shots[:args.limit]

    if args.dry_run:
        print(f"\n计划生成 {len(shots)} 镜（R2V · mp={MEGAPIXELS} · steps={STEPS} · {ASPECT}）：")
        for s in shots:
            note = " [已出片]" if _existing_files(s) else ""
            print(f"  镜{s['shot']} {s['name']} {s['dur']}s  ref1={s['ref1']} ref2={s['ref2']}{note}")
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
