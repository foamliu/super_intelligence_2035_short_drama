#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第06集《情绪》参考图生成（固化 · R2V 前置资产补全）。

补齐 `ASSETS/CHARACTERS/_scene/` 下 4 张参考图（16:9 1280×720）：
- 1 张一次性角色定妆照：old_worker(老工人·闪回，镜 21/23 的 <Picture 1>)
- 3 张场景/界面图（R2V 的 <Picture 2> 底图）：
  lab(深智实验室) / factory(工厂车间) / mozi_ui(墨子UI界面，镜 43 的 <Picture 2>)

供 `gen_ep06_h3_r2v.py` 的 R2V 分镜用 `<Picture 1>`（角色定妆照）+ `<Picture 2>`（场景）底图。
- 工作流：`workflows/Z-Image-Turbo 文生图.json`（国产首选 T2I）
- 负面词：该工作流负面被 ConditioningZeroOut 置零 → 以 "Do NOT include: ..." 追加进正向
- 文件名权威：与 `gen_ep06_h3_r2v.py` 的 `REFS` / `REF_SLUG` 逐字一致

用法:
  python scripts/gen_ep06_scenes.py --dry-run
  python scripts/gen_ep06_scenes.py --key old_worker
  python scripts/gen_ep06_scenes.py --wait
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
    {"key": "old_worker", "out": "06_old_worker.png", "seed": 4601,
     "prompt": ("A Chinese male factory worker in his sixties, thin build with slightly stooped "
                "shoulders, short grey-white hair, rough dark weathered face with deep wrinkles, "
                "tired but focused eyes, oil-stained old blue work uniform, standing in a dim "
                "factory workshop, warm yellow light, three-quarter view, "
                + STYLE + ", muted desaturated palette"),
     "neg": NEG_PORTRAIT},
    # ── 场景/界面图（R2V 的 <Picture 2>）──
    {"key": "lab", "out": "06_lab_night.png", "seed": 4602,
     "prompt": ("A deep-tech AI laboratory at 2am, cold blue screen glow from monitors, server "
                "racks with small indicator lights, one workstation desk with multiple screens, "
                "sparse warm desk lamp light cutting a lonely circle in vast dark workspace, "
                "Shenzhen night city lights through floor-to-ceiling window, no people, "
                + STYLE + ", muted cold palette"),
     "neg": NEG_NO_PEOPLE},
    {"key": "factory", "out": "06_factory_workshop.png", "seed": 4603,
     "prompt": ("An old Chinese factory workshop interior, aged machinery, oily concrete floor, "
                "warm yellow overhead workshop lights mixed with cold side light, dust in the air, "
                "documentary realism, no people, "
                + STYLE + ", muted warm palette"),
     "neg": NEG_NO_PEOPLE},
    {"key": "mozi_ui", "out": "06_mozi_ui.png", "seed": 4604,
     "prompt": ("A minimalist dark holographic AI interface, cold cyan data glow, clean thin "
                "typographic lines, subtle grid, floating data points, restrained sci-fi UI "
                "aesthetic, no people, "
                + STYLE + ", muted cold palette"),
     "neg": NEG_UI},
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
    ap = argparse.ArgumentParser(description="第06集《情绪》参考图生成（Z-Image-Turbo）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--key", type=str, default="", help="只生成某张（逻辑名，如 old_worker）")
    ap.add_argument("--wait", action="store_true", help="阻塞等待（默认只提交）")
    args = ap.parse_args()

    assets = [a for a in ASSETS if not args.key or a["key"] == args.key]
    if args.key and not assets:
        raise SystemExit(f"找不到 {args.key}；可选：{[a['key'] for a in ASSETS]}")

    print("=" * 64)
    print(f" EP06《情绪》参考图  |  共 {len(assets)} 张  |  out: {OUT}")
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

