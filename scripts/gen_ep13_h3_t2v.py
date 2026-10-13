#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第13集《外骨骼》 Minimax H3 T2V 分镜视频生成脚本（固化 · 2026-10-12 推翻旧法 · 无角色镜走 T2V）。

作用：把第 13 集「无角色镜（场景/UI/道具 · 19 镜）→ H3 T2V 直出视频」固化成
可复用、可续跑、可审计的脚本。台词/人声**随 H3 一起生成**（写进 prompt 的
`Audio:`，🚫 本线禁用 TTS，见任务书 §4.5 / 运维指令区 ①）。

- 分镜权威：`SCENES/13_外骨骼.md` 的 `## 逐镜表`（7 列 · 参考图提示列标注 T2V）
- 有角色镜（29 镜）走 `gen_ep13_h3_r2v.py`（R2V）；本脚本只做无角色镜（19 镜）
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep13_h3_t2v.py --dry-run          # 仅打印计划
  python scripts/gen_ep13_h3_t2v.py --limit 4          # 只跑前 N 镜
  python scripts/gen_ep13_h3_t2v.py --shot 05          # 只跑某镜（按镜号）
  python scripts/gen_ep13_h3_t2v.py --skip-existing    # 跳过已出片镜（续跑）
  python scripts/gen_ep13_h3_t2v.py --wait             # 阻塞等待出片（默认只提交）

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（→1056×608；0.92/720p 必 OOM；要 1080p 事后 SeedVR2 超分）
  - steps=10（2026-10-12 运维指令「别默认堆 20」+「H3 在 10 步已基本收敛」；
    本批 19 镜均为静态/界面/道具/场景，无环境剧变镜。EP18 T2V 曾用 20，
    本线按新指令回落 10；若某镜画面持续剧变再单点提 20）
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
WF = ROOT / "workflows" / "video_minimax_h3_t2v.json"
OUT = ROOT / "OUTPUT" / "13_外骨骼" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6
STEPS = 10      # 见 docstring 参数纪律
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 无角色镜（T2V · 19 镜 · 台词随 H3 生成）────────────────
# prompt：`CUT 1:` + 景别 + 画面 + 运镜 + 风格 + `Audio:`（L1 台词原文 / 正向音景）
# ⚠️ 无台词镜只写正向音景；🚫 禁元信息/否定式/镜头编号指代
SHOTS = [
    {"shot": "01", "name": "剧场后台·空镜", "dur": 4.0, "seed": 1301,
     "prompt": ("CUT 1: 中景，缓推，2030年冬夜上海一间小剧场的后台，化妆镜一圈暖黄灯光昏昏亮着，"
                "衣架与道具箱半隐在暗处，冷暖交界。"
                + STYLE +
                " Audio: 后台安静的底噪，远处台前传来隐约的笑声与掌声。")},
    {"shot": "02", "name": "开放麦·大学生讲段子", "dur": 5.0, "seed": 1302,
     "prompt": ("CUT 1: 中景，缓慢横移，开放麦小剧场台前，一个年轻男生握着话筒讲段子，"
                "台下观众笑得很响，舞台暖光、背景压暗。"
                + STYLE +
                " Audio: 台下观众此起彼伏的笑声与掌声。")},
    {"shot": "04", "name": "手机·扣下", "dur": 5.0, "seed": 1304,
     "prompt": ("CUT 1: 特写，固定，一只手在手机屏幕上回了一个OK，然后把手机翻过去扣在桌上，"
                "屏幕冷光映在周围，暖黄环境光。"
                + STYLE +
                " Audio: 讲完了早点回去。明天九点。")},
    {"shot": "05", "name": "自动驾驶办公室·争论架构", "dur": 5.0, "seed": 1305,
     "prompt": ("CUT 1: 中景，缓推，2026年夏天自动驾驶公司的技术白板前，几位工程师围着白板争论架构，"
                "白板上画满模块图与箭头，冷白灯光。"
                + STYLE +
                " Audio: 那一年，自动驾驶行业正在经历一场静默的革命——从模块化架构，全面转向VLA，端到端模型。")},
    {"shot": "08", "name": "测试车·拐进停车场", "dur": 4.0, "seed": 1308,
     "prompt": ("CUT 1: 全景，固定，一辆测试车自己拐进露天停车场，车头摆正、完全没压线，停稳，冬夜冷调。"
                + STYLE +
                " Audio: 转向灯滴答声与低沉的路噪声。")},
    {"shot": "12", "name": "界面·世界模型", "dur": 6.0, "seed": 1312,
     "prompt": ("CUT 1: 特写，缓推，电脑屏幕上，一个可微调世界模型的工具界面，一排排参数与缩略图，"
                "冷白加冷青数据色，干净克制。"
                + STYLE +
                " Audio: 基座是一个世界模型。她只是在教模型，莎拉·赵的观众为什么笑。")},
    {"shot": "14", "name": "界面·外骨骼浮现", "dur": 5.0, "seed": 1314,
     "prompt": ("CUT 1: 特写，缓推，屏幕上缓缓浮现出「外骨骼」三个字，冷白界面，克制。"
                + STYLE +
                " Audio: 不是大脑，不是心脏。是骨架。撑着她，让她不会散架。但走路，还是她自己走。")},
    {"shot": "20", "name": "咖啡杯·桌上多一杯", "dur": 5.0, "seed": 1320,
     "prompt": ("CUT 1: 特写，缓推，第二天早上，一张办公桌上一杯咖啡，热气袅袅，暖黄晨光。"
                + STYLE +
                " Audio: 师兄后来再也不劝了。只是每次她熬完夜，第二天桌上会多一杯咖啡。")},
    {"shot": "22", "name": "观众席·小周与调音师", "dur": 5.0, "seed": 1322,
     "prompt": ("CUT 1: 中景，缓慢横移，开放麦观众席上坐满了人，第三排左侧坐着场务小周和一个兼职调音师，"
                "舞台暖光。"
                + STYLE +
                " Audio: 观众席里，有两个人是她认识的。")},
    {"shot": "25", "name": "屏幕·样本量示意", "dur": 6.0, "seed": 1325,
     "prompt": ("CUT 1: 特写，缓推，屏幕上的样本量示意图，小剧场样本少、大场子样本多，"
                "冷白界面，数据色。"
                + STYLE +
                " Audio: 样本量足够大的时候，小周的笑会被稀释。所以我用小剧场试新段子，用小周当托，然后去大场子验证。")},
    {"shot": "28", "name": "街头·路人玩笑", "dur": 5.0, "seed": 1328,
     "prompt": ("CUT 1: 中景，跟移，上海冬夜街头，一个路人和朋友开玩笑，旁边一位三十岁女性侧目看了一眼，"
                "冷调夜色与路灯暖光交界。"
                + STYLE +
                " Audio: 身体会告诉我，一个词从别人嘴里说出来的时候，是冒犯还是玩笑。模型看不到那个。")},
    {"shot": "30", "name": "屏幕·预测视频", "dur": 6.0, "seed": 1330,
     "prompt": ("CUT 1: 特写，缓推，屏幕上渲染出一段预测视频，一张张不存在的观众脸在想象中笑着，"
                "绿黄红三色区域覆盖，冷青科技感。"
                + STYLE +
                " Audio: 不存在的观众，在想象中笑着。绿色是安全，黄色是可能响，红色是大概率会响。")},
    {"shot": "31", "name": "屏幕·0.82标注", "dur": 5.0, "seed": 1331,
     "prompt": ("CUT 1: 特写，缓推，屏幕特写，模型给一张脸标注「第三排左侧，预测笑声强度0.82」，冷白界面。"
                + STYLE +
                " Audio: 但那张脸不存在。它不知道那个人是小周还是陌生人。")},
    {"shot": "37", "name": "手机·林薇消息", "dur": 5.0, "seed": 1337,
     "prompt": ("CUT 1: 近景，固定，手机屏幕上一条消息，一只手停在那里想了想，屏幕冷光。"
                + STYLE +
                " Audio: 那它算你的工具，还是你的搭档？")},
    {"shot": "40", "name": "屏幕·虚拟观众特写", "dur": 6.0, "seed": 1340,
     "prompt": ("CUT 1: 特写，缓推，屏幕上那些虚拟观众的脸静静渲染着，表情平和，冷青合成质感。"
                + STYLE +
                " Audio: 模型不知道意外。它只知道概率。它渲染不出一个因为没想到而愣住然后突然笑出来的脸。")},
    {"shot": "43", "name": "笔记本·合上", "dur": 5.0, "seed": 1343,
     "prompt": ("CUT 1: 特写，缓推，一双手合上一本笔记本，封面上贴着一个人自己贴的标签，暖光。"
                + STYLE +
                " Audio: 合上本子轻轻的一声，纸张摩擦声。")},
    {"shot": "44", "name": "笔记本·标签", "dur": 5.0, "seed": 1344,
     "prompt": ("CUT 1: 特写，缓推，笔记本封面标签特写，手写体「段子：不可迁移」，暖光下纸面细节。"
                + STYLE +
                " Audio: 有些东西可以备份，有些东西不能。不能备份的那些，才是你。")},
    {"shot": "46", "name": "手机·师兄沉默", "dur": 5.0, "seed": 1346,
     "prompt": ("CUT 1: 特写，固定，手机屏幕亮起一条消息，对方沉默了几秒，回了一个字，屏幕冷光。"
                + STYLE +
                " Audio: 你的车呢？在车库。我想看看那些人。好。")},
    {"shot": "48", "name": "街口·晨光", "dur": 5.0, "seed": 1348,
     "prompt": ("CUT 1: 远景，缓拉，清晨的上海街口，冬日的光从楼宇之间漏出，留白、晨光感。"
                + STYLE +
                " Audio: 清晨安静的街口，远处隐约的车流声。")},
]


# ── ComfyUI API 原语（照 gen_ep13_h3_r2v.py 范式）─────────
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
                f"video/EP13_SHOT-{shot['shot']}_H3_T2V")
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
    return sorted(OUT.glob(f"EP13_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第13集《外骨骼》H3 T2V 分镜视频生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 05）")
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

    print(f"EP13《外骨骼》H3 T2V | {len(shots)} 镜 | mp={MEGAPIXELS} steps={STEPS} {ASPECT}")
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
