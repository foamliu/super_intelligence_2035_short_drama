#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第03集《种子》 Minimax H3 T2V 分镜视频生成脚本（无角色镜 · 14 镜 · 固化）。

作用：把第 03 集「无角色镜 → H3 T2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 有角色镜走 `gen_ep03_h3_r2v.py`（38 镜）；本脚本只做 14 个无角色镜
  （城市夜景 / 迭代时间轴 / 墨子 UI / 手绘草图 / 日志界面 / 架构图 / 手机消息），无需参考图。
- 分镜权威：`SCENES/03_种子.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威，
  标「（T2V）」或纯场景/道具/UI 的镜头都归本脚本）。
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep03_h3_t2v.py --dry-run
  python scripts/gen_ep03_h3_t2v.py --limit 4
  python scripts/gen_ep03_h3_t2v.py --shot 07
  python scripts/gen_ep03_h3_t2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（T2V 单参考图 · 16GB VRAM 红线内，约 1056×608）
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
OUT = ROOT / "OUTPUT" / "03_种子" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6   # T2V 单参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 14 个无角色镜（镜号 / 名称 / 时长 / seed / prompt）──
# 台词（L1）写进 Audio；无台词镜只写正向音景；seed = 4000 + 镜号（与 R2V/T2V 不冲突）
SHOTS = [
    # ── 一、速度（城市夜景 / 迭代时间轴 / 墨子 UI）──
    {"shot": "01", "name": "杭州实验室凌晨夜景", "dur": 4.0, "seed": 4001,
     "prompt": ("CUT 1: 远景（城市全景），固定，2030年6月，杭州，凌晨，实验室落地窗外城市灯火零散，室内冷蓝。"
                + STYLE + " Audio: 服务器风扇低鸣。")},
    {"shot": "03", "name": "迭代时间轴", "dur": 6.0, "seed": 4003,
     "prompt": ("CUT 1: 近景（屏幕特写），缓慢横移，屏幕上的迭代时间轴密密麻麻，像蚁群的路径，冷蓝数据光。"
                + STYLE + " Audio: 每一次迭代，人类工程师都能看懂——调整了哪里，为什么调整。但没有人能在同一个晚上跑完三千次。")},
    {"shot": "07", "name": "墨子扬声器", "dur": 5.0, "seed": 4007,
     "prompt": ("CUT 1: 中近景（界面），固定，扬声器亮起，声波光效在暗处微微亮起，无实体AI。"
                + STYLE + " Audio: 第三千零一次迭代完成。能效比当前最优设计提升百分之三十二。需要原型验证。")},
    # ── 二、唤醒（草图 / 日志）──
    {"shot": "13", "name": "泛黄手绘草图", "dur": 5.0, "seed": 4013,
     "prompt": ("CUT 1: 特写（道具），缓推，一张泛黄的手绘草图，纸上折痕深得像刀刻，蓝色圆珠笔线条，暖黄台灯单光源，四周偏暗。"
                + STYLE + " Audio: 不是代码，是手绘的草图，纸张泛黄，折痕深得像刀刻。")},
    {"shot": "16", "name": "日志唤醒值", "dur": 5.0, "seed": 4016,
     "prompt": ("CUT 1: 特写（界面），缓推，日志界面翻页，时间戳显示三天跨度，唤醒值0.97高亮。"
                + STYLE + " Audio: 界面翻页电子音与轻微提示音。")},
    {"shot": "19", "name": "日志墨子自注", "dur": 4.0, "seed": 4019,
     "prompt": ("CUT 1: 特写（界面），缓推，日志备注栏里，墨子的一行自注文字清晰可见。"
                + STYLE + " Audio: 该路径终端的寄生电容估计值超过安全阈值。实验终止。")},
    # ── 三、归因（草图 / 归因链）──
    {"shot": "30", "name": "草图再推一格", "dur": 4.0, "seed": 4030,
     "prompt": ("CUT 1: 特写（道具），缓推，泛黄手绘草图再往下推一格，蓝色圆珠笔线条，暖黄台灯光。"
                + STYLE + " Audio: 第二个我想让你看的东西——归因。")},
    {"shot": "33", "name": "归因链逐环拆开", "dur": 8.0, "seed": 4033,
     "prompt": ("CUT 1: 中景（界面），缓推，屏幕上一条归因链被逐环拆开，全息冷蓝光。"
                + STYLE + " Audio: 能拆，能追到具体那一环。如果环境变了，重建世界模型；如果检测到对手的欺骗模式——标记，但不等同于确认。归因是一个概率分配的过程。")},
    # ── 五、锁（夜景 / 架构总图）──
    {"shot": "36", "name": "深夜实验室", "dur": 4.0, "seed": 4036,
     "prompt": ("CUT 1: 全景（环境），固定，深夜实验室，只剩服务器风扇的低鸣，幽蓝指示灯。"
                + STYLE + " Audio: 服务器风扇低鸣。")},
    {"shot": "37", "name": "架构总图三层", "dur": 5.0, "seed": 4037,
     "prompt": ("CUT 1: 特写（界面），缓推，全息架构总图展开，感知层、判断层、执行层三层排开，冷蓝电子光。"
                + STYLE + " Audio: 界面展开电子音。")},
    {"shot": "42", "name": "架构图小字警报", "dur": 6.0, "seed": 4042,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，架构图上的一行小字特写，红色高亮「二级警报触发器」与「双重生物特征验证」等文字，冷青背景。"
                + STYLE + " Audio: 看这里——二级警报触发器。任何针对目标函数的写入请求，无论是否被拦截，立即发送加密通知。核心参数层与开发环境物理隔离，任何修改，双重生物特征验证。")},
    # ── 六、种子（日志 / 手机消息）──
    {"shot": "48", "name": "日志04:32:17拦截", "dur": 4.0, "seed": 4048,
     "prompt": ("CUT 1: 特写（界面），缓推，屏幕上的日志停在04:32:17，一行红色的拦截记录，幽暗留白。"
                + STYLE + " Audio: 轻微警报余音。")},
    {"shot": "50", "name": "手机震动·王建国", "dur": 4.0, "seed": 4050,
     "prompt": ("CUT 1: 近景（手机特写），固定，手机屏幕震了一下，发件人显示「王建国」。"
                + STYLE + " Audio: 手机震动声。")},
    {"shot": "51", "name": "消息内容浮现", "dur": 5.0, "seed": 4051,
     "prompt": ("CUT 1: 特写（手机屏幕·文字），缓推，消息内容在屏幕上浮现。"
                + STYLE + " Audio: 小华今天说了句话。它说：老王，你说的长出来的，我可能永远不会有。")},
]

# ── ComfyUI 通用（与 R2V 脚本同构 · 固化）────────────
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


def _save_outputs(hist):
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
    # 参数注入（对齐 MCP _apply_h3_common + PrimitiveStringMultiline=prompt）
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "MiniMaxH3ImageToVideo":
            node.setdefault("inputs", {})["prompt"] = shot["prompt"]
        elif ct == "PrimitiveStringMultiline":
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
                f"video/EP03_SHOT-{shot['shot']}_H3_T2V")
    return wf


def run_one(shot, wait=True, timeout=3600):
    wf = build_workflow(shot)
    res = _prompt(wf)
    pid = res["prompt_id"]
    print(f"[{shot['shot']}] {shot['name']} → pid={pid} dur={shot['dur']}s "
          f"seed={shot['seed']}")
    if not wait:
        return pid
    hist = _queue_until_done(pid, timeout=timeout)
    files = _save_outputs(hist)
    print(f"[{shot['shot']}] 完成：{len(files)} 个文件 → {[f.name for f in files]}")
    return files


def _existing_files(shot):
    return sorted(OUT.glob(f"EP03_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第03集《种子》H3 T2V 分镜视频生成（无角色镜）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 07）")
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
        print(f"\n计划生成 {len(shots)} 镜（T2V · mp={MEGAPIXELS} · steps={STEPS} · {ASPECT}）：")
        for s in shots:
            note = " [已出片]" if _existing_files(s) else ""
            print(f"  镜{s['shot']} {s['name']} {s['dur']}s{note}")
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
