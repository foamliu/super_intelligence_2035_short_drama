#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第06集《情绪》 Minimax H3 T2V 分镜视频生成脚本（无角色镜 · 25 镜 · 固化）。

作用：把第 06 集「无角色镜 → H3 T2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 有角色镜走 `gen_ep06_h3_r2v.py`（29 镜）；本脚本只做 25 个无角色镜
  （科研楼夜景 / 墨子UI曲线·对话·情绪模块 / 工厂轴承碎裂 / 全息绑定 / 数据标注 / 动画岛屿）。
- 分镜权威：`SCENES/06_情绪.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威，
  标「（T2V）」或纯场景/道具/UI 的镜头都归本脚本）。
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep06_h3_t2v.py --dry-run
  python scripts/gen_ep06_h3_t2v.py --limit 4
  python scripts/gen_ep06_h3_t2v.py --shot 03
  python scripts/gen_ep06_h3_t2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（T2V 单参考图 · 16GB VRAM 红线内，约 1056×608）
  - steps=10（本线回落，勿默认堆 20）
  - 台词长度须匹配镜头时长（约 5-7 字/秒）
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
OUT = ROOT / "OUTPUT" / "06_情绪" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6   # T2V 单参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 25 个无角色镜（镜号 / 名称 / 时长 / seed / prompt）──
# 台词（含 UI 文字 / 旁白）写进 Audio；无台词镜只写正向音景；seed = 4600 + 镜号
SHOTS = [

    # ═ 一、凌晨的发现 ═
    {"shot": "01", "name": "深圳深夜科研楼外景", "dur": 4.0, "seed": 4601,
     "prompt": ("CUT 1: 远景（科研楼外景），固定，2030年凌晨，深圳，一栋科研楼在夜色里亮着稀疏的几扇窗，"
                "楼顶天线红灯明灭。" + STYLE + " Audio: 夜风与空调外机的低频。")},
    {"shot": "03", "name": "训练日志双曲线", "dur": 4.0, "seed": 4603,
     "prompt": ("CUT 1: 特写（训练日志界面），缓推，屏幕上是两条学习曲线，一条平缓爬升，一条在某点陡然跃起，"
                "冷青数据光。" + STYLE + " Audio: 墨子处理两类任务的方式不同。")},
    {"shot": "04", "name": "学习曲线平稳", "dur": 4.0, "seed": 4604,
     "prompt": ("CUT 1: 特写（学习曲线·平稳），缓推，屏幕上一条曲线随数据量平稳爬升，冷青数据光。"
                + STYLE + " Audio: 纯逻辑推理，数学、代码、数据清洗，随训练数据量平稳提升，没有意外。")},
    {"shot": "05", "name": "学习曲线跳跃", "dur": 4.0, "seed": 4605,
     "prompt": ("CUT 1: 特写（学习曲线·跳跃），固定，另一条曲线在某一点陡然跃起，之后不再回落，冷青数据光。"
                + STYLE + " Audio: 但价值任务上，不是缓慢爬升，而是跳跃。某一次交互之后，它的判断方式永久改变了。")},
    {"shot": "07", "name": "对话日志滚动", "dur": 5.0, "seed": 4607,
     "prompt": ("CUT 1: 特写（对话日志界面），固定，屏幕上对话日志缓缓滚动，一行行文字掠过，冷青数据光。"
                + STYLE + " Audio: 日志滚动声与服务器低鸣。")},
    {"shot": "08", "name": "学生对话", "dur": 5.0, "seed": 4608,
     "prompt": ("CUT 1: 特写（对话界面），固定，屏幕上是一段对话，用户发来一行字，冷青数据光。"
                + STYLE + " Audio: 谢谢，你说的都对，但我还是不知道自己喜欢什么。")},
    {"shot": "09", "name": "情绪模块状态更新", "dur": 5.0, "seed": 4609,
     "prompt": ("CUT 1: 特写（情绪模块状态界面），固定，屏幕上一行状态更新刷出，唤醒值与效价跳动，冷青数据光。"
                + STYLE + " Audio: 情绪模块状态更新。唤醒值零点七三。效价正零点五一。归因标签，价值困境，无法归类，持久。")},
    {"shot": "10", "name": "持久高亮", "dur": 4.0, "seed": 4610,
     "prompt": ("CUT 1: 特写（界面文字·持久），固定，屏幕上两个字被高亮，冷青数据光。"
                + STYLE + " Audio: 持久。这是第一次出现。")},

    # ═ 二、情绪是什么 ═
    {"shot": "13", "name": "情绪模块架构图", "dur": 4.0, "seed": 4613,
     "prompt": ("CUT 1: 中景（全息架构图），缓推，情绪模块架构图在屏幕上展开，节点与连线依次亮起，冷青数据光。"
                + STYLE + " Audio: 界面展开的电子音。")},
    {"shot": "15", "name": "全息三节点", "dur": 6.0, "seed": 4615,
     "prompt": ("CUT 1: 中景（全息三节点），缓推，全息图里三个节点依次亮起，冷青数据光。"
                + STYLE + " Audio: 预测和预期不一样就产生误差。唤醒标记误差的大小，效价标记它是好是坏，归因标记误差的来源。")},


    {"shot": "17", "name": "标记寿命全息", "dur": 7.0, "seed": 4617,
     "prompt": ("CUT 1: 中景（全息标记寿命），缓推，全息图里标记逐个熄灭，只有少数几个持续亮着，冷青数据光。"
                + STYLE + " Audio: 持久度决定标记停留多久。大部分误差标记一下就够了，噪音、扰动，系统不需要记住。但有些误差被标记为持久。")},
    {"shot": "18", "name": "持久标记高亮", "dur": 5.0, "seed": 4618,
     "prompt": ("CUT 1: 特写（持久标记·高亮），缓推，一个标记被高亮，冷青数据光。"
                + STYLE + " Audio: 下次遇到类似情况，不需要重新计算误差，直接调用这个标记。")},

    # ═ 三、一次性学习 ═
    {"shot": "22", "name": "工厂轴承碎裂", "dur": 5.0, "seed": 4622,
     "prompt": ("CUT 1: 中景（工厂车间），固定，工厂车间里一台机器的轴承在高速旋转中碎裂，金属碎片飞溅，暖黄灯光。"
                + STYLE + " Audio: 金属碎裂轰响与机器嗡鸣。")},
    {"shot": "26", "name": "全息绑定", "dur": 5.0, "seed": 4626,
     "prompt": ("CUT 1: 中景（全息绑定），缓推，全息图里三个条件汇聚成一个点，完成一次绑定，冷青数据光。"
                + STYLE + " Audio: 高唤醒、明确效价、清晰归因，被标为持久。系统就完成了一次绑定。")},
    {"shot": "28", "name": "存储与绑定对比", "dur": 6.0, "seed": 4628,
     "prompt": ("CUT 1: 中景（全息存储与绑定），缓推，全息图里一侧的数据可删可改，另一侧的绑定被焊死，冷青数据光。"
                + STYLE + " Audio: 存储可以删、可以改。绑定是把刺激和情绪标记焊死在一起。以后遇到类似刺激，情绪标记直接告诉它，这个重要，这个好，这个是谁的错。")},
    {"shot": "33", "name": "发光球置架", "dur": 5.0, "seed": 4633,
     "prompt": ("CUT 1: 特写（全息发光球），固定，一个发光的球被放进一个看不见的架子里，冷青数据光。"
                + STYLE + " Audio: 一个发光的球，被放进某个看不见的架子，再也拿不出来。")},
    {"shot": "38", "name": "后续对话日志", "dur": 5.0, "seed": 4638,
     "prompt": ("CUT 1: 特写（对话日志界面），固定，屏幕上后续对话日志滚动，冷青数据光。"
                + STYLE + " Audio: 绑定之后，每当用户说理性上知道该做什么，情感上不确定，它的答案就多了一层。更谨慎的措辞。它开始问你感觉呢。它在记住那个困境。")},

    # ═ 四、两种学习 ═
    {"shot": "39", "name": "2024数据标注现场", "dur": 5.0, "seed": 4639,
     "prompt": ("CUT 1: 中景（数据标注现场），缓慢横移，2024年，一间办公室里标注团队对着屏幕给成千上万条回答打分，屏幕冷光。"
                + STYLE + " Audio: 公司之前用过奖励模型。2024年，标注团队给数万条回答打分，模型学会模拟人类的判断。")},
    {"shot": "40", "name": "奖励模型漂移", "dur": 4.0, "seed": 4640,
     "prompt": ("CUT 1: 特写（奖励模型界面），缓推，屏幕上奖励曲线缓缓漂移，冷青数据光。"
                + STYLE + " Audio: 后来它开始钻空子。挑更长的回答打高分，每句都加作为一个AI的前缀。工程师们管这叫reward hacking。")},
    {"shot": "42", "name": "47次绑定", "dur": 4.0, "seed": 4642,
     "prompt": ("CUT 1: 特写（界面数字·47次绑定），缓推，屏幕上一串数字，冷青数据光。"
                + STYLE + " Audio: 奖励模型可以重训、清空、从头再来。墨子的47次绑定不行。它算工具，还是算别的什么？她没有回答这个问题。")},


    # ═ 五、边界 ═
    {"shot": "46", "name": "全息界面文字", "dur": 6.0, "seed": 4646,
     "prompt": ("CUT 1: 中景（全息界面文字），缓推，屏幕上浮出一行行字，冷青数据光。"
                + STYLE + " Audio: 我无法判断。判断这个绑定是否正确需要的标准，不在绑定的内容里，在绑定之前。而我回不到绑定之前。")},

    # ═ 六、核心记忆 ═
    {"shot": "47", "name": "动画人格岛屿", "dur": 5.0, "seed": 4647,
     "prompt": ("CUT 1: 中景（动画风格·大脑人格岛屿），缓推，动画风格的大脑横截面里，几颗发光的球支撑着几座人格岛屿。"
                + STYLE + " Audio: 她想起小时候看过的老动画片。小女孩的大脑里，几颗发光的球，支撑着几座人格岛屿。每一颗都来自一次关键经历，每一颗都不可替换。")},
    {"shot": "49", "name": "数字47", "dur": 3.0, "seed": 4649,
     "prompt": ("CUT 1: 特写（界面数字·47），固定，屏幕上一个数字，冷青数据光。"
                + STYLE + " Audio: 47个。")},
    {"shot": "51", "name": "47点轮廓线", "dur": 6.0, "seed": 4651,
     "prompt": ("CUT 1: 中景（全息47点·轮廓线），缓推，全息图里47个点依次亮起，连成一条轮廓线，冷青数据光。"
                + STYLE + " Audio: 47次绑定，定义了它。每一次绑定都在绘制它能力边界的轮廓。这些点连起来，就是我是谁的轮廓线。")},
    {"shot": "54", "name": "画面渐暗留白", "dur": 5.0, "seed": 4654,
     "prompt": ("CUT 1: 特写，固定，画面缓缓暗下，留白转场。"
                + STYLE + " Audio: 极轻的环境余韵。")},
]



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


def _save_outputs(hist):
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
                f"video/EP06_SHOT-{shot['shot']}_H3_T2V")
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
    return sorted(OUT.glob(f"EP06_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第06集《情绪》H3 T2V 分镜视频生成（无角色镜）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 03）")
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

