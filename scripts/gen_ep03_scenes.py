#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第03集《种子》参考图生成（固化 · R2V 前置资产补全）。

补齐 `ASSETS/CHARACTERS/_scene/` 下 11 张参考图（16:9 1280×720）：
- 1 张一次性角色定妆照：assistant（助手，仅镜4出场一次）
- 10 张无角色场景/道具图：lab / lab_multiscreen / screen / sketch / log_ui /
  lab_window_night / architecture / lab_doorframe / tree_hologram / lab_window_dawn

供 `gen_ep03_h3_r2v.py` 的 R2V 分镜作 `<Picture 1>`（角色/合影）/`<Picture 2>`（场景）底图。
- 工作流：`workflows/Z-Image-Turbo 文生图.json`（国产首选 T2I）
- 负面词：该工作流负面被 ConditioningZeroOut 置零 → 以 "Do NOT include: ..." 追加进正向
- 文件名权威：与 `gen_ep03_h3_r2v.py` 的 `REFS` / `REF_SLUG` 逐字一致
- 风格：与 `ASSETS/半写实半水墨视觉规范.md` 一致（杭州实验室夜蓝冷青 + 克制的现实科幻）

用法:
  python scripts/gen_ep03_scenes.py --dry-run     # 仅打印计划
  python scripts/gen_ep03_scenes.py --key sketch  # 只生成某张
  python scripts/gen_ep03_scenes.py --wait        # 全部 11 张（阻塞等待）
"""
import argparse
import json
import shutil
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "workflows" / "Z-Image-Turbo 文生图.json"
OUT = ROOT / "ASSETS" / "CHARACTERS" / "_scene"
OUT.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1280, 720
STEPS, CFG = 8, 1.0  # Turbo 配方

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

NEG_NO_PEOPLE = ("people, person, human, human face, text, watermark, logo, signature, "
                 "caption, cartoon, anime, 3D render, illustration, deformed, extra fingers, "
                 "low quality, jpeg artifacts")
NEG_UI = ("people, person, human, human face, hand, watermark, logo, signature, cartoon, anime, "
          "3D render, illustration, low quality, jpeg artifacts")
NEG_PORTRAIT = ("ugly, deformed, bad anatomy, disfigured, poorly drawn face, mutation, "
                "extra limb, extra fingers, fused fingers, too many fingers, blurry, watermark, "
                "text, logo, oversaturated, plastic skin, heavy makeup, beauty filter, anime, "
                "cartoon, illustration, 3D render, bright neon, saturated digital colors, CGI look, "
                "Western oil painting style")

# key → (out 文件名, seed, 正向提示词, 负面词)
ASSETS = [
    # ── 一次性角色定妆照（R2V 的 <Picture 1>）──
    {"key": "assistant", "out": "03_assistant.png", "seed": 2311,
     "prompt": ("A Chinese male lab assistant around thirty years old, short black hair, wearing a "
                "white lab coat over a dark t-shirt, standing in a Hangzhou AI laboratory beside a "
                "workstation, looking at a screen, cold white fluorescent light, " + STYLE +
                ", cool grey-blue palette"),
     "neg": NEG_PORTRAIT},
    # ── 无角色场景/道具图（R2V 的 <Picture 2>）──
    {"key": "lab", "out": "03_lab.png", "seed": 2301,
     "prompt": ("Interior of a Hangzhou deep-tech AI laboratory at late night, cold white fluorescent "
                "lighting, several desks with arrays of monitors and computer screens glowing softly, "
                "floor-to-ceiling windows showing pitch black city night outside, server rack with faint "
                "blue indicator lights, clean minimalist high-tech research space, empty of people, " +
                STYLE + ", cold blue-grey palette"),
     "neg": NEG_NO_PEOPLE},
    {"key": "lab_multiscreen", "out": "03_lab_multiscreen.png", "seed": 2302,
     "prompt": ("Close view of a multi-monitor workstation in a Hangzhou AI laboratory at night, several "
                "large screens arranged in an array displaying dense timeline data and code, cold blue "
                "screen glow illuminating the desk, dark room around, " + STYLE +
                ", cold blue palette, no people"),
     "neg": NEG_UI},
    {"key": "screen", "out": "03_screen.png", "seed": 2303,
     "prompt": ("Close-up of a monitor screen displaying thousands of optimization iteration paths, dense "
                "ant-colony-like trail visualization, translucent glowing lines spreading like root systems "
                "on a dark background, green and cyan data glow, " + STYLE +
                ", shallow depth of field, no people"),
     "neg": NEG_UI},
    {"key": "sketch", "out": "03_sketch.png", "seed": 2304,
     "prompt": ("Close-up of a yellowed hand-drawn paper sketch, blue ballpoint ink lines of a circuit and "
                "architecture diagram, deep fold creases like knife cuts, curled aged paper edges, warm yellow "
                "desk lamp single light source, dark surroundings, " + STYLE +
                ", warm amber palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "log_ui", "out": "03_log_ui.png", "seed": 2305,
     "prompt": ("Dark AI system log interface on a monitor, rows of timestamped event logs in cyan monospace "
                "glyphs on near black background, a few entries highlighted in red, subtle holographic glow, " +
                STYLE + ", cold blue palette, no people, no readable words"),
     "neg": NEG_UI},
    {"key": "lab_window_night", "out": "03_lab_window_night.png", "seed": 2306,
     "prompt": ("View from inside a laboratory through floor-to-ceiling windows at Hangzhou predawn, sparse "
                "city lights scattered in the distance, cold blue night, faint reflection of interior on the "
                "glass, " + STYLE + ", cold blue-grey palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "architecture", "out": "03_architecture.png", "seed": 2307,
     "prompt": ("Full-screen holographic architecture diagram of an AI system, three horizontal layers stacked "
                "vertically, a glowing line highlighted between the middle and bottom layers, cold blue "
                "electronic light on dark background, " + STYLE + ", no people"),
     "neg": NEG_UI},
    {"key": "lab_doorframe", "out": "03_lab_doorframe.png", "seed": 2308,
     "prompt": ("Doorframe of a Hangzhou AI laboratory at night, cold white fluorescent corridor light spilling "
                "into a dimmer room, clean metal doorframe, minimalist high-tech interior, " + STYLE +
                ", cold blue-grey palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "tree_hologram", "out": "03_tree_hologram.png", "seed": 2309,
     "prompt": ("Holographic image of a single tree floating in a dark laboratory, some branches trimmed and "
                "pruned, translucent cold blue hologram glow, roots reaching deep downward, " + STYLE +
                ", cold blue palette, no people"),
     "neg": NEG_UI},
    {"key": "lab_window_dawn", "out": "03_lab_window_dawn.png", "seed": 2310,
     "prompt": ("View through laboratory floor-to-ceiling windows at Hangzhou dawn, a thin line of pale light "
                "brightening the horizon, city silhouettes emerging, cold blue turning to faint warm grey, " +
                STYLE + ", no people"),
     "neg": NEG_NO_PEOPLE},
]
def load_wf():
    with open(WF, encoding="utf-8") as f:
        return json.load(f)


def _prompt(wf):
    p = {"prompt": wf, "client_id": str(uuid.uuid4())}
    data = json.dumps(p).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def _queue_until_done(prompt_id, poll=10, timeout=600):
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


def _find_images(hist):
    imgs = []
    for _nid, node in hist.get("outputs", {}).items():
        for item in node.get("images", []):
            imgs.append(item)
    return imgs


def _download_image(item, dest):
    qs = urllib.parse.urlencode({"filename": item["filename"],
                                 "subfolder": item.get("subfolder", ""),
                                 "type": item.get("type", "output")})
    with urllib.request.urlopen(f"{COMFY}/view?{qs}", timeout=180) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    return dest


def build_workflow(asset):
    wf = load_wf()
    full = asset["prompt"]
    if asset.get("neg"):
        full += " Do NOT include: " + asset["neg"]
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "CLIPTextEncode":
            node.setdefault("inputs", {})["text"] = full
        elif ct in ("EmptySD3LatentImage", "EmptyLatentImage"):
            node.setdefault("inputs", {}).update(width=WIDTH, height=HEIGHT)
        elif ct == "KSampler":
            node.setdefault("inputs", {}).update(seed=int(asset["seed"]),
                                                 steps=int(STEPS), cfg=float(CFG))
    return wf


def run_one(asset, wait=True):
    dst = OUT / asset["out"]
    if dst.exists():
        print(f"[{asset['key']}] 已存在，跳过：{dst.name}")
        return dst
    wf = build_workflow(asset)
    pid = _prompt(wf)["prompt_id"]
    print(f"[{asset['key']}] {asset['out']} → pid={pid[:8]} seed={asset['seed']}")
    if not wait:
        return pid
    hist = _queue_until_done(pid)
    imgs = _find_images(hist)
    if not imgs:
        print(f"[{asset['key']}] ❌ 无输出")
        return None
    _download_image(imgs[0], dst)
    print(f"[{asset['key']}] ✅ {dst.name} ({dst.stat().st_size // 1024} KB)")
    return dst


def main():
    ap = argparse.ArgumentParser(description="第03集《种子》参考图生成（Z-Image-Turbo）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--key", type=str, default="", help="只生成某张（逻辑名，如 sketch）")
    ap.add_argument("--wait", action="store_true", help="阻塞等待（默认只提交）")
    args = ap.parse_args()

    assets = [a for a in ASSETS if not args.key or a["key"] == args.key]
    if args.key and not assets:
        raise SystemExit(f"找不到 {args.key}；可选：{[a['key'] for a in ASSETS]}")

    print("=" * 64)
    print(f" EP03《种子》参考图  |  共 {len(assets)} 张  |  out: {OUT}")
    print("=" * 64)
    for a in assets:
        print(f"  - {a['key']:<16} → {a['out']}  (seed={a['seed']})")
    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    ok = 0
    for i, a in enumerate(assets, 1):
        print(f"\n[{i}/{len(assets)}] {a['key']}")
        try:
            if run_one(a, wait=args.wait) is not None:
                ok += 1
        except Exception as e:
            print(f"  ❌ {e}")
        time.sleep(1)
    print(f"\n{'=' * 64}\n 完成: {ok}/{len(assets)}  输出: {OUT}")


if __name__ == "__main__":
    main()
