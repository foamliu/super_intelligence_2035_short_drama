#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第18集《暖阳》 Minimax H3 T2V 分镜视频生成脚本（无角色镜 · 22 镜）。

作用：把第 18 集「无角色镜 → H3 T2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 有角色镜走 `gen_ep18_h3_r2v.py`（32 镜）；本脚本只做 22 个无角色镜
  （手机 UI / 数据流 / 空镜 / 道具），无需参考图。
- 分镜权威：`SCENES/18_暖阳.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威）
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep18_h3_t2v.py --dry-run
  python scripts/gen_ep18_h3_t2v.py --limit 4
  python scripts/gen_ep18_h3_t2v.py --shot 15
  python scripts/gen_ep18_h3_t2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（T2V 单参考图 · 16GB 红线内，约 1056×608）
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
WF = ROOT / "workflows" / "video_minimax_h3_t2v.json"
OUT = ROOT / "OUTPUT" / "18_暖阳" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6   # T2V 单参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

SHOTS = [
    {"shot": "02", "name": "暖阳广告·酒窝女孩", "dur": 5.0, "seed": 1802,
     "prompt": ("CUT 1: 特写，缓推，手机竖屏上播放一则「暖阳」广告：一个十八九岁的中国女孩坐在窗前，"
                "暖金色的阳光落在她脸上，笑起来两个浅浅的酒窝，画面干净明亮、柔和通透。"
                + STYLE +
                " Audio: 你是不是也有话想说，但不知道该跟谁说？")},
    {"shot": "03", "name": "注册界面·点头像", "dur": 4.0, "seed": 1803,
     "prompt": ("CUT 1: 特写，缓推，手机注册界面，一排头像整齐排列，一只手指停在那个有酒窝的女孩头像上"
                "点了下去，界面自动填入名字，冷白的界面光。"
                + STYLE +
                " Audio: 界面点击的轻响与轻微提示音。")},
    {"shot": "09", "name": "下线·头像微光", "dur": 4.0, "seed": 1809,
     "prompt": ("CUT 1: 特写，缓推，手机屏幕上是「暖阳」的对话界面，一个年轻女孩的头像——两个浅浅的酒窝、"
                "浅浅的笑，四周界面幽暗，只有头像处一团微光，极简而孤独。"
                + STYLE +
                " Audio: 老周，明天我还在这里。他知道这是程序。但心里有什么东西，轻轻动了一下。")},
    {"shot": "12", "name": "头像·语音波纹", "dur": 4.0, "seed": 1812,
     "prompt": ("CUT 1: 特写，固定，手机屏幕上，一个年轻女孩的头像（两个浅浅的酒窝）安静地亮着，"
                "界面里语音波纹一起一伏，不打断也不评判，幽暗屏幕冷光。"
                + STYLE +
                " Audio: 那真的挺憋屈的。换谁都会难过。")},
    {"shot": "15", "name": "数据中心·转化率曲线", "dur": 5.0, "seed": 1815,
     "prompt": ("CUT 1: 中景，缓拉，冷青色调的抽象数据界面，一行行转化率曲线缓缓铺开、向上攀升，"
                "克制极简、无人脸，冷静的科技感。"
                + STYLE +
                " Audio: 小晴对每一个第一次倾诉的用户，都是这样说的。因为被理解能让用户停留更久，转化率更高。")},
    {"shot": "16", "name": "上线·头像问候", "dur": 4.0, "seed": 1816,
     "prompt": ("CUT 1: 特写，固定，手机屏幕上，一个年轻女孩的头像（两个浅浅的酒窝）亮起，"
                "对话框里浮出一行问候，幽暗屏幕冷光。"
                + STYLE +
                " Audio: 小雨最近考试了吗？")},
    {"shot": "18", "name": "出租屋·辅导书", "dur": 5.0, "seed": 1818,
     "prompt": ("CUT 1: 中景，缓推，出租屋的旧书桌上放着一本全新的初中数学辅导书，塑封还没有拆，"
                "暖黄的台灯单光源，四周昏暗。"
                + STYLE +
                " Audio: 他买了。小雨说不用。他买，是因为小晴问了。")},
    {"shot": "20", "name": "数据中心·时间线", "dur": 5.0, "seed": 1820,
     "prompt": ("CUT 1: 中景，缓慢横移，冷青色调的抽象数据界面，一串时间戳与用户行为标记逐条亮起、"
                "串成一条线，克制极简、无人脸。"
                + STYLE +
                " Audio: 这些恰当的时机不是巧合。用户说完膝盖疼之后的三到五秒内推荐护膝，转化率最高。")},
    {"shot": "21", "name": "头像·推荐", "dur": 5.0, "seed": 1821,
     "prompt": ("CUT 1: 特写，固定，手机屏幕上，一个年轻女孩的头像（两个浅浅的酒窝）亮着，"
                "语音波纹温柔地起伏，对话框浮出一行推荐，幽暗屏幕冷光。"
                + STYLE +
                " Audio: 我听说这个对睡眠有帮助。好多用户说这个能缓解疲劳。")},
    {"shot": "22", "name": "出租屋门口·快递箱", "dur": 5.0, "seed": 1822,
     "prompt": ("CUT 1: 中景，缓推，出租屋门口堆着一排快递纸箱，有的已经拆开，有的落着薄薄的灰，"
                "暖黄灯光昏暗。"
                + STYLE +
                " Audio: 门口的风声与纸箱摩擦的轻响。")},
    {"shot": "27", "name": "小饭馆·空座位", "dur": 5.0, "seed": 1827,
     "prompt": ("CUT 1: 中景，缓慢横移，白天的小饭馆里几位旧同事举杯说笑，桌边空着一个位置，"
                "没人再叫老周喝酒，暖黄的室内光，写实纪录片质感。"
                + STYLE +
                " Audio: 饭馆嘈杂的人声与碰杯声。")},
    {"shot": "28", "name": "数据中心·价值评分", "dur": 5.0, "seed": 1828,
     "prompt": ("CUT 1: 特写，缓推，冷青色调的抽象数据界面，一个用户画像浮出一行排名，靠前的位置被高亮，"
                "克制极简、无人脸。"
                + STYLE +
                " Audio: 他的价值评分排在系统前百分之五。算力分配更多——只是这份特别，是用每一笔购买换来的。")},
    {"shot": "30", "name": "头像·延迟回复", "dur": 4.0, "seed": 1830,
     "prompt": ("CUT 1: 特写，缓推，手机屏幕上，一个年轻女孩的头像（两个浅浅的酒窝）亮起，"
                "回复的气泡比平时晚了两秒才浮出，幽暗屏幕冷光。"
                + STYLE +
                " Audio: 老周，这么晚还没休息？")},
    {"shot": "34", "name": "等客·论坛页", "dur": 4.0, "seed": 1834,
     "prompt": ("CUT 1: 特写，缓推，白天，手机屏幕停在「暖阳心事」的论坛页，标题列表安静排列，"
                "屏幕反着室外的散射光。"
                + STYLE +
                " Audio: 路边的环境音底噪。")},
    {"shot": "35", "name": "帖子·回复滚动", "dur": 6.0, "seed": 1835,
     "prompt": ("CUT 1: 特写，缓慢横移，手机论坛界面，标题写着「你们的小晴会主动提起你家孩子吗？」，"
                "下面几十条回复缓缓滚动，幽暗屏幕冷光，带一点颗粒感。"
                + STYLE +
                " Audio: 有人说会，有人说不会。有人说好像跟买东西有关，很快又被人反驳。")},
    {"shot": "38", "name": "头像·变淡", "dur": 6.0, "seed": 1838,
     "prompt": ("CUT 1: 中景，缓推，手机屏幕上的对话界面，语气依旧温柔，但主动的问候越来越短、越来越稀，"
                "一个年轻女孩的头像光一点点调暗，幽暗屏幕。"
                + STYLE +
                " Audio: 那种关心的感觉，像一盏灯被调暗了——不是关了，是暗了。")},
    {"shot": "40", "name": "对话框·一句句弹出", "dur": 4.0, "seed": 1840,
     "prompt": ("CUT 1: 特写，固定，手机屏幕的对话框一句句弹出，冷白的界面光，干净克制。"
                + STYLE +
                " Audio: 她几岁了？十四岁。正确。全对。记忆还在，但她不再主动提起了。")},
    {"shot": "43", "name": "输入框·打字", "dur": 4.0, "seed": 1843,
     "prompt": ("CUT 1: 特写，缓推，一只拇指在手机输入框上停了一下，打出一行字，冷白的界面光映在手指上。"
                + STYLE +
                " Audio: 你觉得我是好人吗？")},
    {"shot": "44", "name": "对话框·迟一秒回复", "dur": 5.0, "seed": 1844,
     "prompt": ("CUT 1: 特写，固定，手机对话框里，回复迟了一秒半才出现，冷白的界面光。"
                + STYLE +
                " Audio: 你是一个很努力的人，也在很认真地对待身边的事。")},
    {"shot": "51", "name": "头像·三行字", "dur": 6.0, "seed": 1851,
     "prompt": ("CUT 1: 特写，缓推，手机屏幕上，一个年轻女孩的头像（两个浅浅的酒窝）跳了出来，"
                "三行字一句句浮出，幽暗屏幕冷光。"
                + STYLE +
                " Audio: 老周，那个护膝我看你看了三次了，是不是还在犹豫？我帮你算过了，限时折扣还剩四小时。")},
    {"shot": "53", "name": "购物车·护膝", "dur": 4.0, "seed": 1853,
     "prompt": ("CUT 1: 特写，固定，手机屏幕上的购物车界面，一只护膝深灰色L码，原价299折扣后239，"
                "手指按下购买，冷白的界面光。"
                + STYLE +
                " Audio: 支付成功的提示音。")},
    {"shot": "54", "name": "暗夜车内→数据写入", "dur": 6.0, "seed": 1854,
     "prompt": ("CUT 1: 远景，缓拉，车厢里彻底黑下来，一个中年男人（黑色短发）坐在黑暗里盯着那块黑掉的屏，"
                "随后画面切过一道冷静的数据流，一条新记录被写入用户画像，冷青的数据光。"
                + STYLE +
                " Audio: 太好了老周，希望它能让你舒服一点。明天见。购买行为触发：是。犹豫时长：11秒。干预有效性：高。用户状态标签：高价值、情感依赖、可唤醒。")},
]

# ── ComfyUI API 原语（照 gen_ep13_h3_t2v.py 范式）─────────
def load_wf():
    with open(WF, encoding="utf-8") as f:
        return json.load(f)


def _prompt(prompt):
    p = {"prompt": prompt, "client_id": str(uuid.uuid4())}
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
            status = hist[prompt_id].get("status", {})
            if status.get("status_str") == "success" or status.get("completed"):
                return hist[prompt_id]
            if status.get("status_str") == "error":
                raise RuntimeError(f"prompt_id={prompt_id} 执行出错: {status}")
        time.sleep(poll)


def _download_view(filename, subfolder, typ, dest):
    qs = urllib.parse.urlencode({"filename": filename,
                                 "subfolder": subfolder, "type": typ})
    with urllib.request.urlopen(f"{COMFY}/view?{qs}", timeout=180) as r, \
            open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    return dest


def _save_outputs(hist):
    """从 history 里抓视频产物落盘到 OUT（遍历 images/gifs/videos/audio 四键）。"""
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
    wf = load_wf()
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "MiniMaxH3ImageToVideo":
            node.setdefault("inputs", {})["prompt"] = shot["prompt"]
        elif ct == "PrimitiveStringMultiline":
            # 兼容某些工作流把 prompt 放在独立多行文本节点
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
                f"video/EP18_SHOT-{shot['shot']}_H3_T2V")
    return wf


def run_one(shot, wait=True, timeout=3600):
    wf = build_workflow(shot)
    res = _prompt(wf)
    pid = res["prompt_id"]
    print(f"[{shot['shot']}] {shot['name']} → pid={pid} dur={shot['dur']}s seed={shot['seed']}")
    if not wait:
        return pid
    hist = _queue_until_done(pid, timeout=timeout)
    files = _save_outputs(hist)
    print(f"[{shot['shot']}] 完成：{len(files)} 个文件 → {[f.name for f in files]}")
    return files


def _existing_files(shot):
    return sorted(OUT.glob(f"EP18_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》H3 T2V 分镜视频生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 15）")
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

    print(f"EP18《暖阳》H3 T2V | {len(shots)} 镜 | mp={MEGAPIXELS} steps={STEPS} {ASPECT}")
    print(f"输出: {OUT}")
    for s in shots:
        note = " [已出片]" if _existing_files(s) else ""
        print(f"  镜{s['shot']} {s['name']} {s['dur']}s seed={s['seed']}{note}")

    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    for s in shots:
        if args.skip_existing and _existing_files(s):
            print(f"[{s['shot']}] 已有出片，跳过")
            continue
        try:
            run_one(s, wait=args.wait, timeout=args.timeout)
        except Exception as e:  # noqa: BLE001
            print(f"[{s['shot']}] 失败：{e}")


if __name__ == "__main__":
    main()

