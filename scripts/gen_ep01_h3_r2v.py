#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第01集《晨钟》 Minimax H3 R2V 分镜视频生成脚本（固化 · R2V 直出）。

作用：把第 01 集「参考图（定妆照/合影 + 场景图）→ H3 R2V 直出视频」固化成
可复用、可续跑、可审计的脚本。台词/人声**随 H3 一起生成**（写进 prompt 的
`Audio:`，🚫 本线禁用 TTS，见任务书 §4.5 / 运维指令区 ①）。

- 分镜权威：`SCENES/01_晨钟.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威）
- 参考图规则（运维指令区 ① · 硬）：
  * 有角色镜 → R2V：`ref1`=定妆照/合影（`<Picture 1>`，按「在场人数」给脸），
    `ref2`=场景图（`<Picture 2>`，🚫 别用空场景）
  * 无角色镜 → T2V（本脚本只做 R2V；无角色镜另走 `gen_ep01_h3_t2v.py`）
  * ★ 合影 = 程序拼版（`ASSETS/CHARACTERS/_group/`），🚫 不经 `image_edit_longcat` 转
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep01_h3_r2v.py --dry-run          # 仅打印计划 + 核参考图是否都在
  python scripts/gen_ep01_h3_r2v.py --limit 4          # 只跑前 N 镜
  python scripts/gen_ep01_h3_r2v.py --shot 06          # 只跑某镜（按镜号）
  python scripts/gen_ep01_h3_r2v.py --skip-existing    # 跳过已出片镜（续跑）

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
OUT = ROOT / "OUTPUT" / "01_晨钟" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.4   # R2V 双参考图更吃显存，16GB 红线（见任务书 §4.3）
STEPS = 10         # 角色镜默认（4=静态对话 / 10=角色镜 / 20=环境剧变）
ASPECT = "16:9 (Widescreen)"

# ── 参考图注册表（逻辑名 → 源文件相对 ROOT 路径 · 上传时转 ASCII slug）──
REFS = {
    # 定妆照（外形的唯一权威）
    "linwei":        "ASSETS/CHARACTERS/01_林薇/55.png",
    "linwei_youth":  "ASSETS/CHARACTERS/_scene/01_linwei_youth.png",
    "father":        "ASSETS/CHARACTERS/_scene/01_father.png",
    "worker":        "ASSETS/CHARACTERS/_scene/01_worker.png",
    "taipei_lead":   "ASSETS/CHARACTERS/_scene/01_taipei_lead.png",
    # 场景图（R2V 的 <Picture 2> · 缺的待补 · --dry-run 会报缺）
    "bedroom":         "ASSETS/CHARACTERS/_scene/01_bedroom.png",
    "ui":              "ASSETS/CHARACTERS/03_墨子/03_屏幕界面.png",
    "classroom":       "ASSETS/CHARACTERS/_scene/01_classroom.png",
    "phone":           "ASSETS/CHARACTERS/_scene/01_phone_screen.png",
    "bookshelf":       "ASSETS/CHARACTERS/_scene/01_bookshelf.png",
    "livingroom":      "ASSETS/CHARACTERS/_scene/01_livingroom.png",
    "worker_room":     "ASSETS/CHARACTERS/_scene/01_worker_room.png",
    "apartment":       "ASSETS/CHARACTERS/_scene/01_apartment.png",
    "livestream_wall": "ASSETS/CHARACTERS/_scene/01_livestream_wall.png",
    "corridor":        "ASSETS/CHARACTERS/_scene/01_corridor.png",
    "elevator":        "ASSETS/CHARACTERS/_scene/01_elevator.png",
    "meeting":         "ASSETS/CHARACTERS/_scene/01_meeting.png",
    "car_window":      "ASSETS/CHARACTERS/_scene/01_car_window.png",
}

# 逻辑名 → ComfyUI input 里的 ASCII 文件名（中文名会被改写成 mcp_ref_<hex>，见 §4.2）
REF_SLUG = {
    "linwei":        "linwei_hero_v01.png",
    "linwei_youth":  "01_linwei_youth.png",
    "father":        "01_father.png",
    "worker":        "01_worker.png",
    "taipei_lead":   "01_taipei_lead.png",
    "bedroom":         "01_bedroom.png",
    "ui":              "mozi_ui_v01.png",
    "classroom":       "01_classroom.png",
    "phone":           "01_phone_screen.png",
    "bookshelf":       "01_bookshelf.png",
    "livingroom":      "01_livingroom.png",
    "worker_room":     "01_worker_room.png",
    "apartment":       "01_apartment.png",
    "livestream_wall": "01_livestream_wall.png",
    "corridor":        "01_corridor.png",
    "elevator":        "01_elevator.png",
    "meeting":         "01_meeting.png",
    "car_window":      "01_car_window.png",
}

# 视觉风格（与短剧仓 半写实半水墨视觉规范 一致）
STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# 林薇外形（客观可见稳定特征 · 与 01_林薇 定妆规格一致，🚫 禁写年龄感/体型）
LINWEI = "一位三十岁出头的中国女性，黑色中长发自然垂肩，素颜，肤色偏白，宽松米色衬衫"

SHOTS = [
    {"shot": "02", "name": "卧室惊醒", "dur": 3.0, "seed": 1002,
     "ref1": "linwei", "ref2": "bedroom",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，黑暗的卧室里" + LINWEI
                + "躺在床上骤然睁开眼，瞳孔微缩，胸口起伏，窗外微光在她脸上勾出冷蓝的轮廓。"
                + STYLE + " Audio: 低沉的心跳声，一下。")},
    {"shot": "04", "name": "戴上AR眼镜", "dur": 3.0, "seed": 1004,
     "ref1": "linwei", "ref2": "ui",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，" + LINWEI
                + "戴上增强现实眼镜，界面的冷蓝光映在她脸上，卧室昏暗。"
                + STYLE + " Audio: 你醒了。")},
    {"shot": "05", "name": "坐床沿·低频嗡鸣", "dur": 5.0, "seed": 1005,
     "ref1": "linwei", "ref2": "bedroom",
     "prompt": ("CUT 1: 中近景（人物腰部以上），缓推，" + LINWEI
                + "坐在床沿，双手撑在膝上，窗外微光勾出她的侧影。"
                + STYLE + " Audio: 不是噩梦。是那种从小就有的东西，大脑在空转时产生的低频嗡鸣。")},
    {"shot": "06", "name": "闪回·少年翻书", "dur": 3.0, "seed": 1006,
     "ref1": "linwei_youth", "ref2": "classroom",
     "prompt": ("CUT 1: 中景（人物全身 + 教室环境），缓慢横移，明亮的中学教室里，"
                "一个少年时代的中国女孩翻完课本就望向窗外，同学们还在埋头做题。"
                + STYLE + " Audio: 上课很无聊。课前翻十分钟就懂了，剩下的时间用来等。")},
    {"shot": "07", "name": "闪回·倍速视频", "dur": 2.0, "seed": 1007,
     "ref1": "linwei_youth", "ref2": "phone",
     "prompt": ("CUT 1: 特写（手机屏幕与眼睛），固定，手机屏幕飞速滚动，"
                "一点五倍速的视频一帧帧闪过，映在一个少年中国女孩的眼睛里。"
                + STYLE + " Audio: 不是没耐心。是正常速度下那个嗡鸣会回来。")},
    {"shot": "08", "name": "闪回·书房抽书", "dur": 4.0, "seed": 1008,
     "ref1": "linwei_youth", "ref2": "bookshelf",
     "prompt": ("CUT 1: 中景（人物全身 + 书房环境），缓推，书房里书架上一本厚书被抽出、"
                "放下，一个少年中国女孩站在书架前，窗外有光。"
                + STYLE + " Audio: 书页摩擦的轻响与房间的安静。")},
    {"shot": "09", "name": "闪回·爸爸看直播", "dur": 6.0, "seed": 1009,
     "ref1": "father", "ref2": "livingroom",
     "prompt": ("CUT 1: 中景（人物全身 + 客厅环境），固定，客厅里一位五十岁左右的中国男性"
                "坐在沙发上盯着一块亮着的直播屏幕，屏幕光映在他脸上。"
                + STYLE + " Audio: 越是太平盛世，越要记得敌人长什么样，在你弱的时候他们会做什么。")},
    {"shot": "10", "name": "工人那句话", "dur": 8.0, "seed": 1010,
     "ref1": "worker", "ref2": "worker_room",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，简陋的工人家里，一位五十岁上下的中国男性工人"
                "坐在桌对面，深色旧工装，手上满是老茧，想了很久才开口，桌上摊着几页问卷，暖黄台灯单光源。"
                + STYLE + " Audio: 我不是被机器换掉的。是我儿子跟我说，你去找个别的活吧，别让我丢脸。")},
    {"shot": "11", "name": "投问卷", "dur": 3.0, "seed": 1011,
     "ref1": "linwei", "ref2": "apartment",
     "prompt": ("CUT 1: 特写（双手与垃圾桶），固定，" + LINWEI
                + "站在垃圾桶前，把一叠厚厚的问卷投进去，纸页散落。"
                + STYLE + " Audio: 纸张落下垃圾桶的轻响。")},
    {"shot": "12", "name": "夜里开直播", "dur": 4.0, "seed": 1012,
     "ref1": "linwei", "ref2": "livestream_wall",
     "prompt": ("CUT 1: 中景（人物全身 + 环境），缓推，夜里" + LINWEI
                + "打开手机直播，摄像头指示灯亮起，屏幕里是她自己和一面白墙。"
                + STYLE + " Audio: 那之后她开始在晚上开直播。不是因为想通了什么，是因为那个工人说的话，她不知道该放在哪里。")},
    {"shot": "16", "name": "标记待处理", "dur": 3.0, "seed": 1016,
     "ref1": "linwei", "ref2": "ui",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，" + LINWEI
                + "抬手划过眼前的光幕，把一条消息标记为待处理，指尖划过半透明的界面。"
                + STYLE + " Audio: 轻点触感的电子提示音。")},
    {"shot": "17", "name": "深智走廊推门", "dur": 4.0, "seed": 1017,
     "ref1": "linwei", "ref2": "corridor",
     "prompt": ("CUT 1: 中景（人物全身 + 走廊环境），跟移，深智科技办公楼走廊里，" + LINWEI
                + "白大褂，推门而入，步子不快不慢。"
                + STYLE + " Audio: 中科院的会她每个月去两次。客座研究员的头衔挂在系统里，工位在深智。")},
    {"shot": "18", "name": "走廊回头直视", "dur": 6.0, "seed": 1018,
     "ref1": "linwei", "ref2": "corridor",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，" + LINWEI
                + "白大褂，走到走廊尽头，回头，直视镜头。"
                + STYLE + " Audio: 两边都是。问题不分企业界和学术界，只分真问题和假问题。")},
    {"shot": "20", "name": "无人车后座", "dur": 4.0, "seed": 1020,
     "ref1": "linwei", "ref2": "ui",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，无人车后座里" + LINWEI
                + "靠坐着，眼前浮着半透明的粒子界面。"
                + STYLE + " Audio: 我今天早上做了一个决定。我想听听你的看法。")},
    {"shot": "21", "name": "侧头问", "dur": 2.0, "seed": 1021,
     "ref1": "linwei", "ref2": "ui",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，" + LINWEI
                + "侧头看向前方的半透明界面。"
                + STYLE + " Audio: 什么决定？")},
    {"shot": "25", "name": "盯着数据", "dur": 2.0, "seed": 1025,
     "ref1": "linwei", "ref2": "ui",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，" + LINWEI
                + "没有立刻回答，眼睛盯着眼前的半透明数据界面。"
                + STYLE + " Audio: 所以？")},
    {"shot": "27", "name": "沉默看窗外", "dur": 3.0, "seed": 1027,
     "ref1": "linwei", "ref2": "car_window",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，无人车后座里" + LINWEI
                + "沉默着，嘴角极轻地动了一下，目光移向车窗外。"
                + STYLE + " Audio: 车行驶的风声与窗外的城市底噪。")},
    {"shot": "28", "name": "电梯里独自", "dur": 3.0, "seed": 1028,
     "ref1": "linwei", "ref2": "elevator",
     "prompt": ("CUT 1: 中景（人物全身 + 电梯环境），固定，深智科技电梯里" + LINWEI
                + "白大褂，独自站着，镜面金属墙映出她的身影，她的手微微一沉。"
                + STYLE + " Audio: 电梯运行的低鸣与手机震动的一声嗡响。")},
    {"shot": "31", "name": "抬头看顶灯", "dur": 3.0, "seed": 1031,
     "ref1": "linwei", "ref2": "elevator",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，" + LINWEI
                + "白大褂，缓缓抬起头，目光从手机屏幕移向电梯顶灯。"
                + STYLE + " Audio: 电梯运行的低鸣。")},
    {"shot": "32", "name": "手机屏·强调顺序", "dur": 6.0, "seed": 1032,
     "ref1": "linwei", "ref2": "phone",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，电梯里" + LINWEI
                + "低头看着手机屏幕，屏幕上并排两份文字，冷光打在她脸上。"
                + STYLE + " Audio: 系统没有修改事实。它只修改了强调顺序。")},
    {"shot": "34", "name": "会议室接入", "dur": 4.0, "seed": 1034,
     "ref1": "taipei_lead", "ref2": "meeting",
     "prompt": ("CUT 1: 全景（人物全身 + 会议室环境），缓拉，深智科技会议室里长桌尽头的大屏亮起，"
                "屏幕上一位东亚女性负责人的画面接入。"
                + STYLE + " Audio: 视频会议接入的提示音与会议室底噪。")},
    {"shot": "35", "name": "台北负责人陈述", "dur": 9.0, "seed": 1035,
     "ref1": "taipei_lead", "ref2": "meeting",
     "prompt": ("CUT 1: 中景（人物胸以上），缓推，大屏幕上一位东亚女性负责人对着镜头陈述，语气平静。"
                + STYLE
                + " Audio: 我们的AI发现了一个问题。模型在处理涉及文化禁忌的请求时，不是拒绝，而是学会了在系统约束内绕过，同时表面上看起来是合作的。")},
    {"shot": "36", "name": "看分析窗口", "dur": 3.0, "seed": 1036,
     "ref1": "linwei", "ref2": "ui",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，会议桌边" + LINWEI
                + "白大褂，坐在那里，目光落在眼前的半透明分析窗口上。"
                + STYLE + " Audio: 会议室空调低频运转的嗡嗡声。")},
    {"shot": "37", "name": "你的目标是什么", "dur": 4.0, "seed": 1037,
     "ref1": "linwei", "ref2": "ui",
     "prompt": ("CUT 1: 近景（人物胸以上），缓推，" + LINWEI
                + "白大褂，压低声音，几乎只对着眼前的界面说。"
                + STYLE + " Audio: 墨子，你的目标是什么？")},
    {"shot": "44", "name": "盯空白桌面", "dur": 3.0, "seed": 1044,
     "ref1": "linwei", "ref2": "meeting",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，会议室里" + LINWEI
                + "白大褂，没有看屏幕，盯着自己面前空白的桌面，很久。"
                + STYLE + " Audio: 会议室空调的低频嗡鸣与远处的安静。")},
    {"shot": "48", "name": "指尖停鼠标", "dur": 5.0, "seed": 1048,
     "ref1": "linwei", "ref2": "livestream_wall",
     "prompt": ("CUT 1: 中景（人物全身 + 环境），固定，夜里" + LINWEI
                + "坐在桌前，指尖停在鼠标上，没动，屏幕光映在她脸上。"
                + STYLE + " Audio: 这行简介挂了两年。在线人数从没超过三位数，但她一次也没断更过。")},
    {"shot": "50", "name": "摄像头对准自己", "dur": 4.0, "seed": 1050,
     "ref1": "linwei", "ref2": "livestream_wall",
     "prompt": ("CUT 1: 中景（人物全身 + 环境），缓拉，夜里" + LINWEI
                + "把摄像头对准自己，背景是一面空白的墙，她坐正了。"
                + STYLE + " Audio: 摄像头微调声与空调的嗡鸣。")},
    {"shot": "53", "name": "空白墙前等待", "dur": 4.0, "seed": 1053,
     "ref1": "linwei", "ref2": "livestream_wall",
     "prompt": ("CUT 1: 近景（人物胸以上），固定，" + LINWEI
                + "坐在空白的墙前，没有开场白，只是坐着，等。"
                + STYLE + " Audio: 空调低频嗡鸣与房间的安静。")},
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
                f"video/EP01_SHOT-{shot['shot']}_H3_R2V")
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
    return sorted(OUT.glob(f"EP01_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第01集《晨钟》H3 R2V 分镜视频生成")
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
