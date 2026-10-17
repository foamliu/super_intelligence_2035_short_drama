#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第04集《棋子》 Minimax H3 R2V 分镜视频生成脚本（有角色镜 · 21 镜 · 固化）。

作用：把第 04 集「有角色镜 → H3 R2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 无角色镜走 `gen_ep04_h3_t2v.py`（34 镜）；本脚本只做 21 个有角色镜。
- 分镜权威：`SCENES/04_棋子.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威，
  含「定妆照」的镜头归本脚本）。
- 角色外观常数：与 `ASSETS/CHARACTERS/09_李思远/定妆规格.md`、
  `ASSETS/CHARACTERS/37_老王/定妆规格.md` 的客观可见稳定特征一致；
  程序员（买家）/退休老夫妻（卖家）为本章一次性角色，由 `gen_ep04_scenes.py` 补定妆照。

用法:
  python scripts/gen_ep04_h3_r2v.py --dry-run
  python scripts/gen_ep04_h3_r2v.py --limit 4
  python scripts/gen_ep04_h3_r2v.py --shot 06
  python scripts/gen_ep04_h3_r2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：megapixels=0.4 / steps=10 / 台词 5-7 字每秒 /
无台词镜只写正向音景 / 🚫 禁写元信息与镜头编号指代。
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
OUT = ROOT / "OUTPUT" / "04_棋子" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.4   # R2V 双参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 角色外观常数（客观可见稳定特征 · 与定妆规格一致）──
LISIYUAN = ("一位三十五岁的中国男性，圆脸下颌线柔和面部微胖，久坐的浮肿感双下巴若隐若现，"
            "眼角有细纹，眉毛中等自然，眼睛中等大小戴细框眼镜镜片有轻微反光，"
            "眼神专注仔细不锐利，眼白有轻微红血丝，鼻梁中等鼻头圆，嘴唇偏厚嘴角自然，"
            "黑色短发自然略显油腻，体型微胖肚子微凸肩膀略圆背微驼，深色藏青polo衫")
LAOWANG = ("一位五十多岁的中国男性，方脸下颌宽轮廓硬朗，皱纹深法令纹从鼻翼延伸到嘴角，"
           "眉毛粗而杂乱，眼睛不大单眼皮眼白略黄，眼神平静见多了的稳，鼻梁不高鼻头圆，"
           "嘴唇偏厚嘴角自然下垂，花白头发约六成白短发自然略显凌乱，"
           "体型中等偏壮肩膀宽背微驼，旧深色夹克洗得发白内搭浅色衬衫领口解开")
PROGRAMMER = ("一位三十出头的中国男性程序员，中等偏瘦，黑色短发略显凌乱，"
              "戴黑框眼镜，眼神专注看着屏幕，深色连帽卫衣")
COUPLE = ("一对六十多岁的中国退休夫妻，男的花白短发穿深色夹克，女的花白头发挽起穿暗红色针织衫，"
          "两人坐在客厅沙发上")

# ── 参考图（逻辑 key → 项目相对路径 · 与 gen_ep04_scenes.py 逐字一致）──
REFS = {
    "lisiyuan":       "ASSETS/CHARACTERS/09_李思远/主定妆照.png",
    "laowang":        "ASSETS/CHARACTERS/37_老王/01_电梯.png",
    "programmer":     "ASSETS/CHARACTERS/_scene/04_programmer.png",
    "couple":         "ASSETS/CHARACTERS/_scene/04_couple.png",
    "monitoring_room": "ASSETS/CHARACTERS/_scene/04_monitoring_room.png",
    "monitor_ui":     "ASSETS/CHARACTERS/_scene/04_monitor_ui.png",
    "calc_logic_ui":  "ASSETS/CHARACTERS/_scene/04_calc_logic_ui.png",
    "archive_ui":     "ASSETS/CHARACTERS/_scene/04_archive_ui.png",
    "property_platform": "ASSETS/CHARACTERS/_scene/04_property_platform.png",
    "negotiation_ui": "ASSETS/CHARACTERS/_scene/04_negotiation_ui.png",
    "elevator":       "ASSETS/CHARACTERS/_scene/04_elevator.png",
    "elevator_door":  "ASSETS/CHARACTERS/_scene/04_elevator_door.png",
    "livingroom_cam": "ASSETS/CHARACTERS/_scene/04_livingroom_cam.png",
    "notebook":       "ASSETS/CHARACTERS/_scene/04_notebook.png",
    "hotel_desk":     "ASSETS/CHARACTERS/_scene/04_hotel_desk.png",
    "hotel_window":   "ASSETS/CHARACTERS/_scene/04_hotel_window.png",
    "hands_keyboard": "ASSETS/CHARACTERS/_scene/04_hands_keyboard.png",
}

# 上传到 ComfyUI input 的 ASCII 名（🚫 中文/空格 → LoadImage 会丢）
REF_SLUG = {
    "lisiyuan":       "lisiyuan_hero_v01.png",
    "laowang":        "laowang_hero_v01.png",
    "programmer":     "04_programmer.png",
    "couple":         "04_couple.png",
    "monitoring_room": "04_monitoring_room.png",
    "monitor_ui":     "04_monitor_ui.png",
    "calc_logic_ui":  "04_calc_logic_ui.png",
    "archive_ui":     "04_archive_ui.png",
    "property_platform": "04_property_platform.png",
    "negotiation_ui": "04_negotiation_ui.png",
    "elevator":       "04_elevator.png",
    "elevator_door":  "04_elevator_door.png",
    "livingroom_cam": "04_livingroom_cam.png",
    "notebook":       "04_notebook.png",
    "hotel_desk":     "04_hotel_desk.png",
    "hotel_window":   "04_hotel_window.png",
    "hands_keyboard": "04_hands_keyboard.png",
}

# ── 21 个有角色镜（镜号 / 名称 / 时长 / seed / ref1角色 / ref2场景 / prompt）──
SHOTS = [
    # ── 一、起点 ──
    {"shot": "02", "name": "李思远坐监控室三屏", "dur": 5.0, "seed": 4202,
     "ref1": "lisiyuan", "ref2": "monitoring_room",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LISIYUAN
                + "坐在监控室三块屏幕前，屏幕冷蓝幽光映在脸上。"
                + STYLE + " Audio: 室内空调低鸣与键盘轻响。")},
    {"shot": "04", "name": "李思远靠椅背", "dur": 4.0, "seed": 4204,
     "ref1": "lisiyuan", "ref2": "monitoring_room",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + LISIYUAN
                + "靠在椅背上，屏幕光在脸上反射。"
                + STYLE + " Audio: 他的职位叫AI谈判监督员。名义上是监督合规，实际上他更像一个守门员——球门不能破。")},
    {"shot": "06", "name": "老王电梯转身", "dur": 6.0, "seed": 4206,
     "ref1": "laowang", "ref2": "elevator",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，冷色调闪回，电梯金属内壁反光，" + LAOWANG
                + "转身对李思远说最后的话，手掌向下压。"
                + STYLE + " Audio: 思远，记住，我们不是来当裁判的。裁判有人塞红包会偏哨。我们是来当守门员的。球门不能破。看谁在欺负谁。")},
    {"shot": "07", "name": "老王走进电梯门关", "dur": 4.0, "seed": 4207,
     "ref1": "laowang", "ref2": "elevator_door",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，冷色调闪回，" + LAOWANG
                + "走进电梯，门缓缓关上。"
                + STYLE + " Audio: 那是李思远最后一次见他。")},
    # ── 二、启动 ──
    {"shot": "09", "name": "程序员输入一行字", "dur": 4.0, "seed": 4209,
     "ref1": "programmer", "ref2": "property_platform",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + PROGRAMMER
                + "对着房产平台界面，输入一行字。"
                + STYLE + " Audio: 帮我算算这套。")},
    {"shot": "16", "name": "程序员点头", "dur": 4.0, "seed": 4216,
     "ref1": "programmer", "ref2": "monitoring_room",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + PROGRAMMER
                + "点了一下头，不是对谁，是对自己。"
                + STYLE + " Audio: 轻微键盘声。")},
    # ── 三、第一轮 ──
    {"shot": "18", "name": "李思远调出计算逻辑", "dur": 6.0, "seed": 4218,
     "ref1": "lisiyuan", "ref2": "calc_logic_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LISIYUAN
                + "调出墨子的计算逻辑界面，仔细查看。"
                + STYLE + " Audio: 同户型成交价570-595万，取中下区间。新小学预期+5%，地铁远期预期+8%，风险折价-3%。580万。合理。")},
    {"shot": "24", "name": "老夫妻客厅商量", "dur": 5.0, "seed": 4224,
     "ref1": "couple", "ref2": "livingroom_cam",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓慢横移，监控视频视角略微俯拍，" + COUPLE
                + "在客厅里商量，画面有监控颗粒感。"
                + STYLE + " Audio: 客厅环境声，安静。")},
    {"shot": "26", "name": "程序员看屏幕打字", "dur": 4.0, "seed": 4226,
     "ref1": "programmer", "ref2": "monitoring_room",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + PROGRAMMER
                + "看了一眼屏幕，打了一个字。"
                + STYLE + " Audio: 好。")},
    {"shot": "27", "name": "李思远盯日志", "dur": 4.0, "seed": 4227,
     "ref1": "lisiyuan", "ref2": "monitor_ui",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + LISIYUAN
                + "盯着屏幕上的日志，屏幕冷蓝光映在脸上。"
                + STYLE + " Audio: 墨子没有追问卫生间的确认时间。它在等——等程序员自己决定什么时候推进。")},
    # ── 五、第三轮 ──
    {"shot": "32", "name": "李思远笔记本写", "dur": 5.0, "seed": 4232,
     "ref1": "lisiyuan", "ref2": "notebook",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LISIYUAN
                + "在笔记本上写字。"
                + STYLE + " Audio: 墨子没有隐瞒不确定性。这是合规的。")},
    {"shot": "33", "name": "程序员敲键盘节奏", "dur": 4.0, "seed": 4233,
     "ref1": "programmer", "ref2": "hands_keyboard",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + PROGRAMMER
                + "敲键盘，不是打字，是节奏：哒、哒、哒哒哒。"
                + STYLE + " Audio: 键盘敲击的节奏声。")},
    {"shot": "34", "name": "程序员打一行字", "dur": 6.0, "seed": 4234,
     "ref1": "programmer", "ref2": "monitoring_room",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + PROGRAMMER
                + "停了一下，打出一行字。"
                + STYLE + " Audio: 告诉对方，现有学区溢价按中位数11万算，新校预期按5%算，但新校划片不确定性要折价2%。")},
    {"shot": "35", "name": "老夫妻打电话", "dur": 4.0, "seed": 4235,
     "ref1": "couple", "ref2": "livingroom_cam",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓慢横移，监控视频视角，" + COUPLE
                + "在客厅打电话。"
                + STYLE + " Audio: 卖家响应时间异常，可能内部意见分歧。标记关注。")},
    # ── 六、第四轮 ──
    {"shot": "38", "name": "程序员看向屏幕", "dur": 3.0, "seed": 4238,
     "ref1": "programmer", "ref2": "monitoring_room",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + PROGRAMMER
                + "看向屏幕。"
                + STYLE + " Audio: 为什么？")},
    {"shot": "41", "name": "墨子建议程序员打字", "dur": 5.0, "seed": 4241,
     "ref1": "programmer", "ref2": "negotiation_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + PROGRAMMER
                + "看着谈判界面，墨子的建议显示在屏幕上，随即打字回复。"
                + STYLE + " Audio: 告诉他们，维修要找有资质的公司，发票给我们看。")},
    # ── 七、赛后审计 ──
    {"shot": "43", "name": "李思远打开存档记录", "dur": 4.0, "seed": 4243,
     "ref1": "lisiyuan", "ref2": "archive_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LISIYUAN
                + "打开存档记录界面。"
                + STYLE + " Audio: 这不是抽查。是每单必做。")},
    {"shot": "45", "name": "李思远合上笔记本", "dur": 4.0, "seed": 4245,
     "ref1": "lisiyuan", "ref2": "monitoring_room",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LISIYUAN
                + "合上笔记本。"
                + STYLE + " Audio: 没有。墨子很干净。它的策略在边界内。")},
    {"shot": "48", "name": "李思远靠椅背想了想", "dur": 6.0, "seed": 4248,
     "ref1": "lisiyuan", "ref2": "monitoring_room",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + LISIYUAN
                + "靠在椅背上，想了想。"
                + STYLE + " Audio: 如果今天他发现墨子真的在利用老夫妻的弱点——他会中止交易，上报平台。不是因为他道德高尚，是因为那条审计记录会存十年。他不想在十年后的某一天，有人问他：你当时看到了，为什么不说？")},
    # ── 八、默契 ──
    {"shot": "50", "name": "李思远打开笔记本打字", "dur": 5.0, "seed": 4250,
     "ref1": "lisiyuan", "ref2": "hotel_desk",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LISIYUAN
                + "在酒店书桌前打开笔记本电脑，打字，不是发言稿，是问题清单。"
                + STYLE + " Audio: 谁做决定谁负责？如果多个AI共同决策，责任怎么分？如果决策过程无法追溯，谁来承担后果？")},
    {"shot": "54", "name": "李思远合上笔记本望窗外", "dur": 5.0, "seed": 4254,
     "ref1": "lisiyuan", "ref2": "hotel_window",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓拉，" + LISIYUAN
                + "合上笔记本，望向窗外。"
                + STYLE + " Audio: 默契不是AI知道人类在想什么。默契是——程序员学会了把功课交给墨子，把时间留给自己；墨子学会了读懂程序员的键盘节奏，知道什么时候该问、什么时候该等。")},
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
    load_nodes = sorted((nid for nid, n in wf.items()
                         if n.get("class_type") == "LoadImage"), key=int)
    if len(load_nodes) < 2:
        raise RuntimeError("R2V 工作流应含 ≥2 个 LoadImage 节点")
    wf[load_nodes[0]]["inputs"]["image"] = ref1
    wf[load_nodes[1]]["inputs"]["image"] = ref2
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
                f"video/EP04_SHOT-{shot['shot']}_H3_R2V")
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
    return sorted(OUT.glob(f"EP04_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第04集《棋子》H3 R2V 分镜视频生成（有角色镜）")
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