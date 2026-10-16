#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第02集《经验》参考图生成（固化 · R2V 前置资产补全）。

补齐 `ASSETS/CHARACTERS/_scene/` 下 13 张参考图（16:9 1280×720）：
- 3 张一次性角色定妆照：laoshifu（老师傅）/ wang_youth（青年王建国）/ engineer（设备厂商年轻工程师）
- 10 张无角色场景/道具图：fab_door / etcher_old / etcher / fab_workshop / fab_yellow /
  ion_implanter / restroom / new_etcher / restroom_glass / palm

供 `gen_ep02_h3_r2v.py` 的 R2V 分镜作 `<Picture 1>`（角色/合影）/`<Picture 2>`（场景）底图。
- 工作流：`workflows/Z-Image-Turbo 文生图.json`（国产首选 T2I）
- 负面词：该工作流负面被 ConditioningZeroOut 置零 → 以 "Do NOT include: ..." 追加进正向
- 文件名权威：与 `gen_ep02_h3_r2v.py` 的 `REFS` / `REF_SLUG` 逐字一致
- 风格：与 `ASSETS/半写实半水墨视觉规范.md` 一致（Fab：洁净室冷白 + 黄光区暖黄 + 夜景低饱和）

用法:
  python scripts/gen_ep02_scenes.py --dry-run     # 仅打印计划
  python scripts/gen_ep02_scenes.py --key etcher  # 只生成某张
  python scripts/gen_ep02_scenes.py --wait        # 全部 13 张（阻塞等待）
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
    {"key": "laoshifu", "out": "02_laoshifu.png", "seed": 2101,
     "prompt": ("A Chinese master technician in his sixties, thin weathered face with deep "
                "wrinkles, grey close-cropped hair, wearing an old blue-grey work uniform, "
                "standing beside an old etching machine in a 1990s semiconductor cleanroom, "
                "leaning slightly and pointing at his own ear as if listening, warm faded yellow "
                "industrial light, nostalgic film grain, " + STYLE + ", ochre and light ink"),
     "neg": NEG_PORTRAIT},
    {"key": "wang_youth", "out": "02_wang_youth.png", "seed": 2102,
     "prompt": ("A Chinese factory worker around thirty years old, short black hair, lean build, "
                "wearing an old light-blue work uniform, standing in a 1990s semiconductor "
                "cleanroom, listening attentively to an older master beside a machine, warm faded "
                "yellow light, nostalgic film grain, " + STYLE + ", ochre and light ink"),
     "neg": NEG_PORTRAIT},
    {"key": "engineer", "out": "02_engineer.png", "seed": 2103,
     "prompt": ("A Chinese field engineer around thirty years old, short neat hair, wearing a dark "
                "navy work jacket and safety glasses, holding a tablet, standing in a modern "
                "semiconductor Fab, cool white cleanroom light, " + STYLE +
                ", cool grey and light ink"),
     "neg": NEG_PORTRAIT},
    # ── 无角色场景/道具图（R2V 的 <Picture 2>）──
    {"key": "fab_door", "out": "02_fab_door.png", "seed": 2111,
     "prompt": ("A semiconductor cleanroom entrance with a waist-height access-control card reader, "
                "a red indicator light turning green, white cleanroom corridor walls, cool white "
                "light, " + STYLE + ", cool grey and light ink"),
     "neg": NEG_NO_PEOPLE},
    {"key": "etcher_old", "out": "02_etcher_old.png", "seed": 2112,
     "prompt": ("A 1990s semiconductor etching machine line inside an old cleanroom, weathered "
                "beige metal cabinets, round quartz viewport windows, retro industrial control "
                "panels, warm faded yellow light, " + STYLE + ", ochre and light ink"),
     "neg": NEG_NO_PEOPLE},
    {"key": "etcher", "out": "02_etcher.png", "seed": 2113,
     "prompt": ("A large modern semiconductor plasma etching machine in a cleanroom, stainless "
                "steel chamber with a round quartz viewport, small status indicator lights, cool "
                "white overhead light with a faint yellow accent, " + STYLE +
                ", cool grey and light ink"),
     "neg": NEG_NO_PEOPLE},
    {"key": "fab_workshop", "out": "02_fab_workshop.png", "seed": 2114,
     "prompt": ("A vast semiconductor Fab cleanroom workshop interior, rows of large machines and "
                "automated wafer-handling equipment, cleanroom lighting, cold white and warm yellow "
                "mixed light, distant machine status lights, no people, " + STYLE +
                ", light ink with generous negative space"),
     "neg": NEG_NO_PEOPLE},
    {"key": "fab_yellow", "out": "02_fab_yellow.png", "seed": 2115,
     "prompt": ("A semiconductor Fab yellow-light zone, amber-yellow industrial lighting washing "
                "over machines and cleanroom walls, cool grey shadows, no people, " + STYLE +
                ", ochre with cool grey shadows"),
     "neg": NEG_NO_PEOPLE},
    {"key": "ion_implanter", "out": "02_ion_implanter.png", "seed": 2116,
     "prompt": ("A large semiconductor ion implantation machine in a cleanroom, metal housing with "
                "control panels and cabling, cool white light, no people, " + STYLE +
                ", cool grey and light ink"),
     "neg": NEG_NO_PEOPLE},
    {"key": "restroom", "out": "02_restroom.png", "seed": 2117,
     "prompt": ("A modest factory break room just outside a semiconductor cleanroom, plastic "
                "chairs, a small table with a thermos and a lunch box, through a glass wall the "
                "warm yellow cleanroom light is visible, cool neutral indoor light, no people, " +
                STYLE + ", warm grey and soft yellow"),
     "neg": NEG_NO_PEOPLE},
    {"key": "new_etcher", "out": "02_new_etcher.png", "seed": 2118,
     "prompt": ("A brand-new semiconductor etching machine, pristine stainless steel surface, "
                "overly clean polished metal reflecting cold white light, no people, " + STYLE +
                ", cool grey and light ink, subtle unease"),
     "neg": NEG_NO_PEOPLE},
    {"key": "restroom_glass", "out": "02_restroom_glass.png", "seed": 2119,
     "prompt": ("View through a glass wall from a factory break room into a semiconductor "
                "cleanroom, warm yellow cleanroom light on the far side, machines visible, no "
                "people, " + STYLE + ", warm yellow through cool glass"),
     "neg": NEG_NO_PEOPLE},
    {"key": "palm", "out": "02_palm.png", "seed": 2120,
     "prompt": ("Close-up of an old Chinese factory worker's hand, large rough hand with swollen "
                "knuckles, thick layered calluses on the palm, age spots on the back of the hand, "
                "right index finger with an old scar, yellow cleanroom light in background, " +
                STYLE + ", high-contrast callus texture, ochre"),
     "neg": NEG_PORTRAIT},
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
    ap = argparse.ArgumentParser(description="第02集《经验》参考图生成（Z-Image-Turbo）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--key", type=str, default="", help="只生成某张（逻辑名，如 etcher）")
    ap.add_argument("--wait", action="store_true", help="阻塞等待（默认只提交）")
    args = ap.parse_args()

    assets = [a for a in ASSETS if not args.key or a["key"] == args.key]
    if args.key and not assets:
        raise SystemExit(f"找不到 {args.key}；可选：{[a['key'] for a in ASSETS]}")

    print("=" * 64)
    print(f" EP02《经验》参考图  |  共 {len(assets)} 张  |  out: {OUT}")
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

