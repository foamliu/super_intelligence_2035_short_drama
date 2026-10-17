#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第04集《棋子》参考图生成（固化 · R2V 前置资产补全）。

补齐 `ASSETS/CHARACTERS/_scene/` 下 15 张参考图（16:9 1280×720）：
- 2 张角色定妆照/合影：programmer（程序员·买家）· couple（退休老夫妻合影）
- 13 张无角色场景/界面图：monitoring_room / monitor_ui / calc_logic_ui /
  archive_ui / property_platform / negotiation_ui / elevator / elevator_door /
  livingroom_cam / notebook / hotel_desk / hotel_window / hands_keyboard

供 `gen_ep04_h3_r2v.py` 的 R2V 分镜作 `<Picture 1>`（角色/合影）/`<Picture 2>`（场景）底图。
- 工作流：`workflows/Z-Image-Turbo 文生图.json`（国产首选 T2I）
- 负面词：该工作流负面被 ConditioningZeroOut 置零 → 以 "Do NOT include: ..." 追加进正向
- 文件名权威：与 `gen_ep04_h3_r2v.py` 的 `REFS` / `REF_SLUG` 逐字一致
- 风格：与 `ASSETS/半写实半水墨视觉规范.md` 一致（上海雨夜冷蓝 + 监控室荧光冷白 + 克制现实科技）

用法:
  python scripts/gen_ep04_scenes.py --dry-run     # 仅打印计划
  python scripts/gen_ep04_scenes.py --key notebook  # 只生成某张
  python scripts/gen_ep04_scenes.py --wait        # 全部 15 张（阻塞等待）
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
    # ── 角色定妆照/合影（R2V 的 <Picture 1>）──
    {"key": "programmer", "out": "04_programmer.png", "seed": 4101,
     "prompt": ("A Chinese male programmer in his early thirties, medium-slim build, black short "
                "hair slightly messy, wearing black-rimmed glasses and a plain dark hoodie, sitting "
                "before a computer in a dim monitoring room, focused gaze on the screen, cold screen "
                "glow on his face, " + STYLE + ", muted desaturated palette, shallow depth of field"),
     "neg": NEG_PORTRAIT},
    {"key": "couple", "out": "04_couple.png", "seed": 4102,
     "prompt": ("An elderly Chinese retired couple in their sixties sitting together on a living "
                "room sofa, the husband with short grey hair wearing a dark jacket, the wife with grey "
                "hair tied back wearing a dark red knit sweater, discussing and pointing at a "
                "smartphone, warm home lighting, slightly elevated camera angle, " + STYLE +
                ", warm amber palette, two people"),
     "neg": NEG_PORTRAIT},
    {"key": "monitoring_room", "out": "04_monitoring_room.png", "seed": 4103,
     "prompt": ("Interior of a small AI negotiation monitoring room in Shanghai at night, three "
                "monitors side by side on a desk, card-based data UI on the screens, an ordinary "
                "office not sci-fi, cold white fluorescent light, a worn notebook and keyboard on the "
                "desk, " + STYLE + ", cold blue-grey palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "monitor_ui", "out": "04_monitor_ui.png", "seed": 4104,
     "prompt": ("Close-up of a monitoring screen displaying a structured negotiation audit panel, "
                "card-based user interface with buyer data stream and seller logs in cold green and "
                "cyan, dark background, " + STYLE + ", cold blue palette, no people, no readable words"),
     "neg": NEG_UI},
    {"key": "calc_logic_ui", "out": "04_calc_logic_ui.png", "seed": 4105,
     "prompt": ("Close-up of a monitor showing a real-estate pricing calculation interface, several "
                "stacked data cards with numeric estimate ranges, cold green and cyan UI on dark "
                "background, clean restrained design, " + STYLE + ", no people, no readable words"),
     "neg": NEG_UI},
    {"key": "archive_ui", "out": "04_archive_ui.png", "seed": 4106,
     "prompt": ("Close-up of a monitor showing an encrypted audit archive interface, minimalist "
                "system UI with white background and dark text rows, a timestamp and digital signature "
                "block, cold precise institutional design, " + STYLE + ", no people, no readable words"),
     "neg": NEG_UI},
    {"key": "property_platform", "out": "04_property_platform.png", "seed": 4107,
     "prompt": ("Close-up of a real-estate trading platform interface on a monitor, listing card of "
                "a school-district apartment, cold green and cyan data cards, clean minimal UI, "
                + STYLE + ", no people, no readable words"),
     "neg": NEG_UI},
    {"key": "negotiation_ui", "out": "04_negotiation_ui.png", "seed": 4108,
     "prompt": ("Close-up of a negotiation interface on a monitor, two agent panels exchanging "
                "structured offer messages, cold blue and green data flow, card-based UI, restrained "
                "design, " + STYLE + ", no people, no readable words"),
     "neg": NEG_UI},
    {"key": "elevator", "out": "04_elevator.png", "seed": 4109,
     "prompt": ("Interior of an ordinary office building elevator at night, brushed metal walls "
                "reflecting cold fluorescent light, slightly desaturated cold blue memory tone, "
                + STYLE + ", cold grey palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "elevator_door", "out": "04_elevator_door.png", "seed": 4110,
     "prompt": ("Close-up of closed elevator metal doors, cold reflective surface with a thin shadow "
                "line at the door seam, faint blurred reflection, cold grey palette, " + STYLE +
                ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "livingroom_cam", "out": "04_livingroom_cam.png", "seed": 4111,
     "prompt": ("Slightly elevated surveillance-camera view of a retired couple's living room, "
                "ordinary Chinese home with sofa, warm yellow indoor light, subtle monitor grain and "
                "soft noise, observed distance, " + STYLE + ", warm amber palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "notebook", "out": "04_notebook.png", "seed": 4112,
     "prompt": ("Close-up of a well-worn A5 softcover notebook open beside a keyboard, pages filled "
                "with small handwritten Chinese characters, one sentence circled in red ink, curled "
                "paper edges, warm desk lamp light, " + STYLE + ", warm amber palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "hotel_desk", "out": "04_hotel_desk.png", "seed": 4113,
     "prompt": ("A hotel room desk at night with an open laptop glowing cold white, a question list "
                "on screen, dark room around, cold screen light on the desk, " + STYLE +
                ", cold blue palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "hotel_window", "out": "04_hotel_window.png", "seed": 4114,
     "prompt": ("View through a hotel window at Shanghai after the rain stopped, wet glass with "
                "streaks, city night lights scattering, cool blue night turning faintly warm, " +
                STYLE + ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "hands_keyboard", "out": "04_hands_keyboard.png", "seed": 4115,
     "prompt": ("Close-up of hands typing on a keyboard with rhythmic tapping, fingers on dark "
                "keycaps, cold screen glow, shallow depth of field, " + STYLE +
                ", cold blue palette, no face"),
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
    ap = argparse.ArgumentParser(description="第04集《棋子》参考图生成（Z-Image-Turbo）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--key", type=str, default="", help="只生成某张（逻辑名，如 notebook）")
    ap.add_argument("--wait", action="store_true", help="阻塞等待（默认只提交）")
    args = ap.parse_args()

    assets = [a for a in ASSETS if not args.key or a["key"] == args.key]
    if args.key and not assets:
        raise SystemExit(f"找不到 {args.key}；可选：{[a['key'] for a in ASSETS]}")

    print("=" * 64)
    print(f" EP04《棋子》参考图  |  共 {len(assets)} 张  |  out: {OUT}")
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
