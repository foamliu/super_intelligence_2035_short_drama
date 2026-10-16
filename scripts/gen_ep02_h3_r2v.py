#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第02集《经验》 Minimax H3 R2V 分镜视频生成脚本（有角色镜 · 32 镜 · 固化）。

作用：把第 02 集「有角色镜 → H3 R2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 无角色镜走 `gen_ep02_h3_t2v.py`（23 镜）；本脚本只做 32 个有角色镜。
- 分镜权威：`SCENES/02_经验.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威）
- 风格：以 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准
- 角色外观常数：与 `ASSETS/CHARACTERS/05_王建国/定妆规格.md`、
  `ASSETS/CHARACTERS/02_陈思危/定妆规格.md` 的客观可见稳定特征一致

用法:
  python scripts/gen_ep02_h3_r2v.py --dry-run
  python scripts/gen_ep02_h3_r2v.py --limit 4
  python scripts/gen_ep02_h3_r2v.py --shot 06
  python scripts/gen_ep02_h3_r2v.py --skip-existing --wait

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
OUT = ROOT / "OUTPUT" / "02_经验" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.4   # R2V 双参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 角色外观常数（客观可见稳定特征 · 与定妆规格一致）──
# 🚫 王建国禁：劳动模范化 / 悲情化 / 过度年轻化（60岁必须有60岁的样子）
WANG = ("一位六十岁的中国退休工人，方脸宽下颌颧骨略高，皮肤黝黑偏黄，浓眉微皱，"
        "单眼皮，黑色极短发几乎贴头皮，身形壮实，双手粗糙布满老茧")
CHENSIWEI = ("一位四十八岁的中国男性，长圆脸下颌柔和，额头宽发际线略高，眉毛淡疏，"
             "双眼皮，眼神柔和，黑发夹杂灰白，中等偏瘦，深灰圆领毛衣")
LAOSHIFU = "一位六十多岁的老技术员，瘦削布满皱纹的脸，灰色短发，旧蓝灰工装"
WANG_YOUTH = "一位三十岁左右的中国工厂工人，黑色短发，精瘦，旧浅蓝工装"
ENGINEER = "一位三十岁左右的中国设备工程师，利落短发，深藏青工作夹克，护目镜，手持平板"

# ── 参考图（逻辑 key → 项目相对路径 · 与 gen_ep02_scenes.py / 合影脚本 逐字一致）──
REFS = {
    # 定妆照（外形的唯一权威）
    "wang":          "ASSETS/CHARACTERS/05_王建国/104.png",
    "chensiwei":     "ASSETS/CHARACTERS/02_陈思危/125.png",
    # 一次性角色定妆照（由 gen_ep02_scenes.py 生成）
    "laoshifu":      "ASSETS/CHARACTERS/_scene/02_laoshifu.png",
    "wang_youth":    "ASSETS/CHARACTERS/_scene/02_wang_youth.png",
    "engineer":      "ASSETS/CHARACTERS/_scene/02_engineer.png",
    # 合影（程序拼版 · gen_ep02_group_composites.py）
    "laoshifu_wangyouth": "ASSETS/CHARACTERS/_group/02_laoshifu_wangyouth_hero_v01.png",
    "wang_chensiwei":     "ASSETS/CHARACTERS/_group/02_wangjianguo_chensiwei_hero_v01.png",
    # 场景图（R2V 的 <Picture 2>）
    "fab_door":       "ASSETS/CHARACTERS/_scene/02_fab_door.png",
    "etcher_old":     "ASSETS/CHARACTERS/_scene/02_etcher_old.png",
    "etcher":         "ASSETS/CHARACTERS/_scene/02_etcher.png",
    "fab_workshop":   "ASSETS/CHARACTERS/_scene/02_fab_workshop.png",
    "fab_yellow":     "ASSETS/CHARACTERS/_scene/02_fab_yellow.png",
    "ion_implanter":  "ASSETS/CHARACTERS/_scene/02_ion_implanter.png",
    "restroom":       "ASSETS/CHARACTERS/_scene/02_restroom.png",
    "new_etcher":     "ASSETS/CHARACTERS/_scene/02_new_etcher.png",
    "restroom_glass": "ASSETS/CHARACTERS/_scene/02_restroom_glass.png",
    "palm":           "ASSETS/CHARACTERS/_scene/02_palm.png",
}

# 上传到 ComfyUI input 的 ASCII 名（🚫 中文/空格 → LoadImage 会丢）
REF_SLUG = {
    "wang":          "wangjianguo_hero_v01.png",
    "chensiwei":     "chensiwei_hero_v01.png",
    "laoshifu":      "02_laoshifu.png",
    "wang_youth":    "02_wang_youth.png",
    "engineer":      "02_engineer.png",
    "laoshifu_wangyouth": "02_laoshifu_wangyouth_hero_v01.png",
    "wang_chensiwei":     "02_wangjianguo_chensiwei_hero_v01.png",
    "fab_door":       "02_fab_door.png",
    "etcher_old":     "02_etcher_old.png",
    "etcher":         "02_etcher.png",
    "fab_workshop":   "02_fab_workshop.png",
    "fab_yellow":     "02_fab_yellow.png",
    "ion_implanter":  "02_ion_implanter.png",
    "restroom":       "02_restroom.png",
    "new_etcher":     "02_new_etcher.png",
    "restroom_glass": "02_restroom_glass.png",
    "palm":           "02_palm.png",
}

# ── 32 个有角色镜（镜号 / 名称 / 时长 / seed / ref1角色 / ref2场景 / prompt）──
SHOTS = [
    # ── 一、起点（门禁 / 闪回 / 刻蚀机）──
    {"shot": "02", "name": "门禁刷卡", "dur": 4.0, "seed": 2002,
     "ref1": "wang", "ref2": "fab_door",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + WANG
                + "穿着旧工装，站在洁净室门禁前刷开工牌，红灯转为绿灯，冷白灯光打在他脸上。"
                + STYLE + " Audio: 退休第三天，他还是来了。不是工作需要。是手需要摸到机台。")},
    {"shot": "03", "name": "闪回·师傅用耳朵听", "dur": 6.0, "seed": 2003,
     "ref1": "laoshifu_wangyouth", "ref2": "etcher_old",
     "prompt": ("CUT 1: 中景（人物全身），缓慢横移，闪回，二十八年前的六英寸线车间里，"
                + LAOSHIFU + "弯腰在旧刻蚀机旁，指着自己的耳朵，对" + WANG_YOUTH
                + "说话，暖黄旧色调，颗粒感胶片质感。"
                + STYLE + " Audio: 别用眼睛看，用耳朵听。眼睛会骗你，耳朵不会。")},
    {"shot": "06", "name": "三号刻蚀机前", "dur": 4.0, "seed": 2006,
     "ref1": "wang", "ref2": "etcher",
     "prompt": ("CUT 1: 中近景（人物腰部以上），固定，" + WANG
                + "穿着白色洁净服，站在三号刻蚀机前，头顶扬声器亮起微光，冷白灯光。"
                + STYLE + " Audio: 老王，三号刻蚀机，聚焦环温度漂移。零点三度。")},
    {"shot": "07", "name": "掌心贴反应腔", "dur": 5.0, "seed": 2007,
     "ref1": "wang", "ref2": "etcher",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + WANG
                + "穿着白色洁净服，走到机台前，不看屏幕，把掌心平贴上反应腔外壁，手指微微张开，闭眼，像在听。"
                + STYLE + " Audio: 这个系统叫小华，工厂的AI。小华，像个学徒——他师傅才配叫「老」什么。")},
    {"shot": "08", "name": "睁眼收手", "dur": 2.0, "seed": 2008,
     "ref1": "wang", "ref2": "etcher",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "穿着白色洁净服，三秒后睁开眼，把手从机台上收回。"
                + STYLE + " Audio: 正常。")},
    {"shot": "10", "name": "直视机台", "dur": 7.0, "seed": 2010,
     "ref1": "wang", "ref2": "etcher",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + WANG
                + "穿着白色洁净服，直视机台，语气笃定。"
                + STYLE + " Audio: 我知道数据。你的温度传感器在腔壁上，聚焦环在里面，等离子体在烧。零点三度是正常波动，不是漂移。")},
    {"shot": "11", "name": "侧身望车间", "dur": 3.0, "seed": 2011,
     "ref1": "wang", "ref2": "fab_workshop",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "穿着白色洁净服，侧过身，望向车间深处。"
                + STYLE + " Audio: 但偏移趋势——四月了。")},
    {"shot": "12", "name": "四月了", "dur": 8.0, "seed": 2012,
     "ref1": "wang", "ref2": "fab_yellow",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + WANG
                + "穿着白色洁净服，黄光区的暖黄光落在他身上，他慢慢开口。"
                + STYLE + " Audio: 深圳四月湿度上来，Fab的温湿度控制系统要处理更多外部湿负荷，整栋楼的供电会有波动，刻蚀等离子体稳定性受影响。这不是聚焦环的问题。")},
    {"shot": "13", "name": "低头看手掌", "dur": 6.0, "seed": 2013,
     "ref1": "wang", "ref2": "palm",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + WANG
                + "穿着白色洁净服，低头看着自己的手掌，掌心有旧茧。"
                + STYLE + " Audio: 我不知道怎么告诉你。我只能说，我在这站了二十八年。每年的四月，机台的感觉都会变。我听了二十八个四月。你才听了一个。")},
    # ── 二、说不清（离子注入机 / 平路比喻）──
    {"shot": "15", "name": "手搭机台仰头", "dur": 4.0, "seed": 2015,
     "ref1": "wang", "ref2": "ion_implanter",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + WANG
                + "穿着白色洁净服，手搭在离子注入机外壳上，仰头。"
                + STYLE + " Audio: 老王，你刚才的判断是对的。聚焦环没有问题，是供电波动造成的测量噪声。")},
    {"shot": "17", "name": "无尘布擦手", "dur": 2.0, "seed": 2017,
     "ref1": "wang", "ref2": "fab_workshop",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "穿着白色洁净服，收回手，在无尘布上擦了擦。"
                + STYLE + " Audio: 现在有了。")},
    {"shot": "19", "name": "侧头看屏幕", "dur": 3.0, "seed": 2019,
     "ref1": "wang", "ref2": "ion_implanter",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "穿着白色洁净服，侧头看向机台上的屏幕。"
                + STYLE + " Audio: 有什么区别？")},
    {"shot": "21", "name": "看自己的手", "dur": 6.0, "seed": 2021,
     "ref1": "wang", "ref2": "fab_workshop",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "穿着白色洁净服，想了想，看向自己的手。"
                + STYLE + " Audio: 我就是知道它不对。手贴上去就知道了。你问我怎么知道的，我说不出来。你说得对，我也不知道自己是怎么发现的。")},
    {"shot": "22", "name": "平路是长出来的", "dur": 10.0, "seed": 2022,
     "ref1": "wang", "ref2": "fab_workshop",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + WANG
                + "穿着白色洁净服，在无尘布上擦手，缓缓讲述，背景是焦外的黄光区，冷暖对撞。"
                + STYLE + " Audio: 你走路的时候，路上有个坑，你没看见。但你的脚踩上去之前，身体已经知道不对了。平路的感觉长在身体里了。突然有一个不一样的，身体先于大脑知道。")},

    # ── 三、不同（午休 · 休息室）──
    {"shot": "27", "name": "休息室屏幕亮起", "dur": 4.0, "seed": 2027,
     "ref1": "wang", "ref2": "restroom",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + WANG
                + "脱掉洁净服上衣，露出灰色长袖T恤，坐在休息室里，墙上屏幕亮起。"
                + STYLE + " Audio: 老王，你说的「长出来的」，能不能再解释一下？")},
    {"shot": "28", "name": "嚼米饭想了想", "dur": 4.0, "seed": 2028,
     "ref1": "wang", "ref2": "restroom",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "露出灰色长袖T恤，嚼着米饭，想了想。"
                + STYLE + " Audio: 你记得你第一次看到的东西吗？")},
    {"shot": "30", "name": "看玻璃外黄光", "dur": 8.0, "seed": 2030,
     "ref1": "wang", "ref2": "restroom_glass",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + WANG
                + "露出灰色长袖T恤，放下筷子，隔着玻璃看着外面洁净室的黄光。"
                + STYLE + " Audio: 不只是第一次，是每一次。今天的我和昨天的我，是同一个人。昨天的感觉留在我身体里了，今天的我带着昨天的我一起进来。")},
    {"shot": "31", "name": "妈妈的菜", "dur": 8.0, "seed": 2031,
     "ref1": "wang", "ref2": "restroom",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + WANG
                + "露出灰色长袖T恤，重新拿起筷子，慢慢说。"
                + STYLE + " Audio: 你想拆开它，就没了。就像你妈做的菜，你问她怎么做的，她说放盐、放糖、放酱油。但你按这个做，不是那个味道——那个「差不多」里面有二十年的手感和火候。")},
    {"shot": "33", "name": "不知道怎么给你", "dur": 5.0, "seed": 2033,
     "ref1": "wang", "ref2": "restroom",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "露出灰色长袖T恤，放下筷子，看着屏幕。"
                + STYLE + " Audio: 也许吧。但我也不知道怎么给你。")},
    # ── 四、脚印（新机台 · 太干净了）──
    {"shot": "34", "name": "厂商工程师群像", "dur": 4.0, "seed": 2034,
     "ref1": "engineer", "ref2": "fab_workshop",
     "prompt": ("CUT 1: 中景（人物全身），缓慢横移，下午，Fab车间里，" + ENGINEER
                + "和一群设备厂商工程师在调试一台新刻蚀机，动作专业利落。"
                + STYLE + " Audio: 调试仪器声与脚步声。")},
    {"shot": "35", "name": "贴传感器跑数据", "dur": 4.0, "seed": 2035,
     "ref1": "engineer", "ref2": "new_etcher",
     "prompt": ("CUT 1: 中景（人物全身），固定，" + ENGINEER
                + "在新刻蚀机上贴了十几个传感器，连上电脑，跑数据。"
                + STYLE + " Audio: 没问题了。")},
    {"shot": "36", "name": "手贴新机台", "dur": 4.0, "seed": 2036,
     "ref1": "wang", "ref2": "new_etcher",
     "prompt": ("CUT 1: 中景（人物全身），跟移，工程师走后，" + WANG
                + "穿着白色洁净服，走过去，把手贴在新机台外壳上。"
                + STYLE + " Audio: 新机台运转的轻微嗡鸣。")},
    {"shot": "37", "name": "太干净了", "dur": 6.0, "seed": 2037,
     "ref1": "wang", "ref2": "new_etcher",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + WANG
                + "穿着白色洁净服，手在新机台上停留，眉头轻皱，新机台金属表面反光过亮、过分干净。"
                + STYLE + " Audio: 太干净了。这个机台的震动太干净了，像录音棚里修过音的嗓子。真的机台是有脾气的。")},
    {"shot": "39", "name": "太干净反而不对", "dur": 4.0, "seed": 2039,
     "ref1": "wang", "ref2": "new_etcher",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "穿着白色洁净服，把手收回来。"
                + STYLE + " Audio: 我知道。但它太干净了，我反而觉得不对。")},
    # ── 五、良率（王建国 × 陈思危 · 人机之辩）──
    {"shot": "42", "name": "陈思危玻璃前", "dur": 5.0, "seed": 2042,
     "ref1": "chensiwei", "ref2": "restroom_glass",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + CHENSIWEI
                + "来到休息室玻璃前，看着洁净室里的机台。"
                + STYLE + " Audio: 听说你今天说一台新机台「太干净了」？")},
    {"shot": "43", "name": "王建国讲夜班盯", "dur": 6.0, "seed": 2043,
     "ref1": "wang", "ref2": "restroom_glass",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "露出灰色长袖T恤，站在旁边，看着玻璃里的机台。"
                + STYLE + " Audio: 后来我让夜班的工程师盯了一下。跑了十二小时，晶圆边缘出现了一致的微观形貌偏移。数据在规格范围内，但形貌偏移了。")},
    {"shot": "44", "name": "用了什么数据", "dur": 3.0, "seed": 2044,
     "ref1": "chensiwei", "ref2": "fab_workshop",
     "prompt": ("CUT 1: 中近景（人物腰部以上），固定，" + CHENSIWEI
                + "转过身。"
                + STYLE + " Audio: 你做这个判断的时候，用了什么数据？")},
    {"shot": "45", "name": "就是感觉", "dur": 3.0, "seed": 2045,
     "ref1": "wang", "ref2": "fab_workshop",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "露出灰色长袖T恤，想了想。"
                + STYLE + " Audio: 没有数据。就是感觉。")},
    {"shot": "46", "name": "黄光落两人", "dur": 8.0, "seed": 2046,
     "ref1": "wang_chensiwei", "ref2": "fab_yellow",
     "prompt": ("CUT 1: 中景（人物全身），缓推，黄光落在两个人身上，" + WANG
                + "与" + CHENSIWEI + "站在Fab车间黄光区。"
                + STYLE + " Audio: 我年轻的时候带过一个工程师。他很聪明，什么都按规程来，但良率就是比我低。后来他调走了，换了个人来，同样的机台，同样的规程，良率上来了。")},
    {"shot": "47", "name": "区别不在机台", "dur": 4.0, "seed": 2047,
     "ref1": "chensiwei", "ref2": "fab_workshop",
     "prompt": ("CUT 1: 中近景（人物腰部以上），固定，" + CHENSIWEI
                + "望着洁净室里沉默的机台。"
                + STYLE + " Audio: 区别不在机台，在人。")},
    {"shot": "48", "name": "我有身体", "dur": 5.0, "seed": 2048,
     "ref1": "wang", "ref2": "fab_workshop",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + WANG
                + "露出灰色长袖T恤，看着他。"
                + STYLE + " Audio: 那不一样。我有身体。")},
    {"shot": "49", "name": "属于它的四月", "dur": 8.0, "seed": 2049,
     "ref1": "chensiwei", "ref2": "fab_yellow",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + CHENSIWEI
                + "没有回头，望着黄光灯下的机台。"
                + STYLE + " Audio: 我知道。所以我没打算复制你。我只是想，如果它也有一个属于自己的「四月」，它会变成什么。")},
]


# ── ComfyUI 通用（与 T2V 脚本同构 · 固化）────────────────
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
                f"video/EP02_SHOT-{shot['shot']}_H3_R2V")
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
    return sorted(OUT.glob(f"EP02_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第02集《经验》H3 R2V 分镜视频生成")
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
