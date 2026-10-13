#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第18集《暖阳》场景参考图生成（固化 · R2V 前置资产补全）。

补齐 `ASSETS/CHARACTERS/_scene/` 下 6 张「无角色/单人物」参考图（16:9 1280×720），
供 `gen_ep18_h3_r2v.py` 的 R2V 分镜作 `<Picture 2>` 场景底图，以及镜 6 闪回的
车间主任定妆照（`<Picture 1>`，后与老周程序拼版成合影）。
- 工作流：`workflows/Z-Image-Turbo 文生图.json`（国产首选 T2I）
- 口径：场景无角色/无身份一致性诉求（角色由 R2V 的 `<Picture 1>` 定妆照保证）
- 负面词：该工作流负面被 ConditioningZeroOut 置零 → 以 "Do NOT include: ..." 追加进正向
- 文件名权威：与 `gen_ep18_h3_r2v.py` 的 `REFS` / `REF_SLUG` 逐字一致

用法:
  python scripts/gen_ep18_scenes.py --dry-run     # 仅打印计划
  python scripts/gen_ep18_scenes.py --key ride    # 只生成某场景
  python scripts/gen_ep18_scenes.py --wait        # 阻塞等待（默认只提交）
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
# 手机屏：允许头像（一张脸），但禁全身人物/群像
NEG_PHONE = ("full body person, group of people, crowd, watermark, logo, signature, caption, "
             "cartoon, anime, 3D render, illustration, low quality, jpeg artifacts, "
             "distorted face, extra fingers")
# 车间主任定妆照：单人像，禁艺术化/塑料感
NEG_PORTRAIT = ("ugly, deformed, bad anatomy, disfigured, extra fingers, watermark, text, logo, "
                "oversaturated, plastic skin, cartoon, anime, illustration, 3D render, "
                "low quality, jpeg artifacts")

# key → (out 文件名, seed, 正向提示词, 负面词)
SCENES = [
    {"key": "ride", "out": "18_ride_interior.png", "seed": 1801,
     "prompt": ("Interior of a ride-hailing car at night viewed from the back seat, dark cabin, "
                "empty driver seat, steering wheel, dashboard with warm orange instrument glow, "
                "car window showing blurred Shanghai night city lights and neon signs, "
                "cold blue ambient from outside mixing with warm dashboard glow, "
                "no people, empty, cinematic wide shot, " + STYLE),
     "neg": NEG_NO_PEOPLE},
    {"key": "room", "out": "18_rental_room.png", "seed": 1802,
     "prompt": ("Small one-bedroom rental apartment at night, old but tidy furniture, a worn "
                "wooden desk with a warm desk lamp, simple curtains, nightstand with a framed "
                "photo, dim room lit only by faint street light through the window and a warm "
                "dim lamp, no people, empty, cinematic, " + STYLE),
     "neg": NEG_NO_PEOPLE},
    {"key": "bedroom", "out": "18_rental_bedroom.png", "seed": 1803,
     "prompt": ("Small bedroom in an old rental apartment at night, single bed with plain grey "
                "bedding, bedside table with a faintly glowing smartphone, dim warm lamp, dark "
                "window with faint city glow outside, no people, empty, cinematic, " + STYLE),
     "neg": NEG_NO_PEOPLE},
    {"key": "factory_office", "out": "18_factory_office.png", "seed": 1804,
     "prompt": ("Old factory manager office in daylight, grey metal desk with two tea cups and a "
                "paper document folder, filing cabinet, calendar on the wall, window showing the "
                "factory workshop floor beyond, cold fluorescent ceiling light, no people, empty, "
                "cinematic, " + STYLE),
     "neg": NEG_NO_PEOPLE},
    {"key": "phone", "out": "18_phone_screen.png", "seed": 1805,
     "prompt": ("Close-up of a smartphone screen showing a warm AI companion chat interface, a "
                "young girl avatar with two shallow dimples and a soft gentle smile in a rounded "
                "profile picture at the top of a chat, speech bubbles below, cold white screen "
                "glow against a dark blurred background, screen UI, cinematic, " + STYLE),
     "neg": NEG_PHONE},
    {"key": "manager", "out": "18_factory_manager.png", "seed": 1806,
     "prompt": ("A 50-year-old Chinese male factory workshop manager, short black hair with some "
                "grey at the temples, plain face with deep frown lines and tired stern eyes, "
                "wearing a dark blue work jacket over a shirt, standing in a factory office, "
                "neutral serious expression, head and shoulders centered, cinematic photorealistic "
                "portrait, " + STYLE),
     "neg": NEG_PORTRAIT},
]


def load_wf():
    with open(WF, encoding="utf-8") as f:
        return json.load(f)


def _prompt(prompt):
    p = {"prompt": prompt, "client_id": str(uuid.uuid4())}
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
            status = hist[prompt_id].get("status", {})
            if status.get("status_str") == "success" or status.get("completed"):
                return hist[prompt_id]
            if status.get("status_str") == "error":
                raise RuntimeError(f"prompt_id={prompt_id} 执行出错: {status}")
        time.sleep(poll)


def _find_images(hist: dict) -> list:
    imgs = []
    for _nid, node in hist.get("outputs", {}).items():
        for item in node.get("images", []):
            imgs.append(item)
    return imgs


def _download_image(item: dict, dest: Path) -> Path:
    qs = urllib.parse.urlencode({"filename": item["filename"],
                                 "subfolder": item.get("subfolder", ""),
                                 "type": item.get("type", "output")})
    with urllib.request.urlopen(f"{COMFY}/view?{qs}", timeout=180) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    return dest


def build_workflow(scene: dict) -> dict:
    wf = load_wf()
    full = scene["prompt"]
    if scene.get("neg"):
        full += " Do NOT include: " + scene["neg"]
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "CLIPTextEncode":
            node.setdefault("inputs", {})["text"] = full
        elif ct in ("EmptySD3LatentImage", "EmptyLatentImage"):
            node.setdefault("inputs", {}).update(width=WIDTH, height=HEIGHT)
        elif ct == "KSampler":
            node.setdefault("inputs", {}).update(seed=int(scene["seed"]),
                                                 steps=int(STEPS), cfg=float(CFG))
    return wf


def run_one(scene: dict, wait: bool = True):
    dst = OUT / scene["out"]
    if dst.exists():
        print(f"[{scene['key']}] 已存在，跳过：{dst.name}")
        return dst
    wf = build_workflow(scene)
    pid = _prompt(wf)["prompt_id"]
    print(f"[{scene['key']}] {scene['out']} → pid={pid[:8]} seed={scene['seed']}")
    if not wait:
        return pid
    hist = _queue_until_done(pid)
    imgs = _find_images(hist)
    if not imgs:
        print(f"[{scene['key']}] ❌ 无输出")
        return None
    _download_image(imgs[0], dst)
    print(f"[{scene['key']}] ✅ {dst.name} ({dst.stat().st_size // 1024} KB)")
    return dst


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》场景参考图生成（Z-Image-Turbo）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--key", type=str, default="", help="只生成某场景（逻辑名，如 ride）")
    ap.add_argument("--wait", action="store_true", help="阻塞等待（默认只提交）")
    args = ap.parse_args()

    scenes = [s for s in SCENES if not args.key or s["key"] == args.key]
    if args.key and not scenes:
        raise SystemExit(f"找不到场景 {args.key}；可选：{[s['key'] for s in SCENES]}")

    print("=" * 64)
    print(f" EP18《暖阳》场景参考图  |  共 {len(scenes)} 张  |  out: {OUT}")
    print("=" * 64)
    for s in scenes:
        print(f"  - {s['key']:<16} → {s['out']}  (seed={s['seed']})")
    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    ok = 0
    for i, s in enumerate(scenes, 1):
        print(f"\n[{i}/{len(scenes)}] {s['key']}")
        try:
            if run_one(s, wait=args.wait) is not None:
                ok += 1
        except Exception as e:
            print(f"  ❌ {e}")
        time.sleep(1)
    print(f"\n{'=' * 64}\n 完成: {ok}/{len(scenes)}  输出: {OUT}")


if __name__ == "__main__":
    main()
