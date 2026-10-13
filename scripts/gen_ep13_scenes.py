#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第13集《外骨骼》场景参考图生成（固化 · R2V 前置资产补全）。

补齐 `ASSETS/CHARACTERS/_scene/` 下 14 张「无角色」场景参考图（16:9 1280×720），
供 `gen_ep13_h3_r2v.py` 的 R2V 分镜作 `<Picture 2>` 场景底图。
- 工作流：`workflows/Z-Image-Turbo 文生图.json`（国产首选 T2I）
- 口径：无角色 / 无身份一致性诉求（角色由 R2V 的 `<Picture 1>` 定妆照保证）
- 负面词：该工作流负面被 ConditioningZeroOut 置零 → 以 "Do NOT include: ..." 追加进正向
- 文件名权威：与 `gen_ep13_h3_r2v.py` 的 `REFS` / `REF_SLUG` 逐字一致

用法:
  python scripts/gen_ep13_scenes.py --dry-run     # 仅打印计划
  python scripts/gen_ep13_scenes.py --key cafe    # 只生成某场景
  python scripts/gen_ep13_scenes.py               # 全部 14 张
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
NEG_UI = ("people, person, human, human face, watermark, logo, signature, cartoon, anime, "
          "3D render, illustration, low quality, jpeg artifacts")

# key → (out 文件名, seed, 正向提示词, 负面词)
SCENES = [
    {"key": "backstage", "out": "13_theatre_backstage.png", "seed": 1401,
     "prompt": ("Backstage of a small comedy club theater at night, makeup mirror vanity with warm "
                "dim tungsten bulbs, clothes rack with costumes, coiled cables on the floor, a chair, "
                "faint warm stage light leaking through the curtain edge, cold backstage fluorescent "
                "light, no people, empty, cinematic wide shot, " + STYLE), "neg": NEG_NO_PEOPLE},
    {"key": "openmic", "out": "13_openmic_stage.png", "seed": 1402,
     "prompt": ("Empty open-mic comedy stage in a small theater, a single microphone on a stand in a "
                "pool of warm spotlight, dark empty audience seating rows in the foreground, plain dark "
                "backdrop, warm stage light against deep shadows, no people, empty, cinematic, " + STYLE),
     "neg": NEG_NO_PEOPLE},
    {"key": "interview", "out": "13_interview_room.png", "seed": 1403,
     "prompt": ("Interview room in a tech startup office, two chairs facing each other across a small "
                "table, cold white fluorescent ceiling lights, plain light walls, a glass wall showing "
                "the open office beyond, no people, empty, cinematic, " + STYLE), "neg": NEG_NO_PEOPLE},
    {"key": "testcar", "out": "13_testcar_interior.png", "seed": 1404,
     "prompt": ("Interior of a self-driving test car viewed from the passenger seat, dashboard with "
                "sensor displays and a central screen, steering wheel, car window showing a Shanghai "
                "street with a convenience store ahead, cool screen glow mixed with daylight, no people, "
                "empty cabin, cinematic, " + STYLE), "neg": NEG_NO_PEOPLE},
    {"key": "annualparty", "out": "13_annual_party_stage.png", "seed": 1405,
     "prompt": ("Company annual party stage in a banquet hall, warm stage lighting, festive banner "
                "backdrop, round dining tables in the foreground shadow, an empty stage with a "
                "microphone stand, no people, cinematic, " + STYLE), "neg": NEG_NO_PEOPLE},
    {"key": "cafe", "out": "13_cafe.png", "seed": 1406,
     "prompt": ("Cozy coffee shop interior, two armchairs facing each other across a small round table "
                "by a window, warm yellow pendant light, empty cups on the table, bookshelf and plants, "
                "warm interior light meeting cool window light, no people, empty, cinematic, " + STYLE),
     "neg": NEG_NO_PEOPLE},
    {"key": "office", "out": "13_office.png", "seed": 1407,
     "prompt": ("Open-plan startup office, rows of desks with dual monitors and office chairs, whiteboard "
                "on the wall, cold white ceiling light mixed with a few warm desk lamps, glass meeting "
                "room, no people, empty, cinematic, " + STYLE), "neg": NEG_NO_PEOPLE},
    {"key": "lab", "out": "13_lab_night.png", "seed": 1408,
     "prompt": ("Computer lab at night in 2017, old CRT and LCD monitors on desks, whiteboard with "
                "handwritten formulas, a desk lamp casting warm yellow light over a cluttered desk, a "
                "coffee cup, dim room, nostalgic, no people, cinematic, " + STYLE), "neg": NEG_NO_PEOPLE},
    {"key": "subway", "out": "13_subway_car.png", "seed": 1409,
     "prompt": ("Shanghai metro subway car interior, rows of stainless steel and blue plastic seats, "
                "overhead handrails, red LED information display above the door, pale fluorescent "
                "lighting, window reflections with tunnel lights, no people, empty car, cinematic, " + STYLE),
     "neg": NEG_NO_PEOPLE},
    {"key": "street", "out": "13_street.png", "seed": 1410,
     "prompt": ("Shanghai street in early winter morning, low-rise buildings and street trees, pale cold "
                "winter light, a crosswalk, shopfronts, thin morning haze, no people, empty street, "
                "cinematic, " + STYLE), "neg": NEG_NO_PEOPLE},
    {"key": "phone", "out": "13_phone_screen.png", "seed": 1411,
     "prompt": ("Close-up of a smartphone lying on a table, screen showing a messaging chat interface, "
                "cold white screen glow against dark surroundings, no people, cinematic, " + STYLE),
     "neg": NEG_UI},
    {"key": "screen_ui", "out": "13_screen_ui.png", "seed": 1412,
     "prompt": ("Close-up of a computer monitor showing a clean engineering tool interface, a world-model "
                "viewer rendering rows of virtual audience faces with a laughter-intensity heatmap overlay "
                "in green yellow and red, cold white and cold cyan data colors, restrained clean UI, no "
                "people, cinematic, " + STYLE), "neg": NEG_UI},
    {"key": "virtual_audience", "out": "13_virtual_audience.png", "seed": 1413,
     "prompt": ("Grid of rendered synthetic virtual audience faces smiling, slightly unreal uncanny "
                "quality, smooth perfect skin texture, green yellow red laughter-intensity regions "
                "overlaid, cold cyan rendered tone with a faint grey-blue filter, synthetic not "
                "photographic, cinematic, " + STYLE),
     "neg": ("real photograph, real person, recognizable person, celebrity, realistic skin pores, "
             "watermark, logo, caption, cartoon, anime, illustration, low quality, jpeg artifacts")},
    {"key": "theatre_door", "out": "13_theatre_door.png", "seed": 1414,
     "prompt": ("Entrance of a small theater at night, a door with a warm sign light, Shanghai winter "
                "night cold blue tones, street lamp warm light, wet pavement reflection, no people, "
                "empty, cinematic, " + STYLE), "neg": NEG_NO_PEOPLE},
]

def load_wf() -> dict:
    return json.loads(WF.read_text(encoding="utf-8"))


def _prompt(prompt: dict) -> dict:
    payload = {"prompt": prompt, "client_id": str(uuid.uuid4())}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def _queue_until_done(prompt_id: str, poll: int = 10, timeout: int = 600) -> dict:
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


# ── 工作流注入（按 class_type 通用注入，不硬编码节点 id）──
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
    ap = argparse.ArgumentParser(description="第13集《外骨骼》场景参考图生成（Z-Image-Turbo）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--key", type=str, default="", help="只生成某场景（逻辑名，如 cafe）")
    ap.add_argument("--wait", action="store_true", help="阻塞等待（默认只提交）")
    args = ap.parse_args()

    scenes = [s for s in SCENES if not args.key or s["key"] == args.key]
    if args.key and not scenes:
        raise SystemExit(f"找不到场景 {args.key}；可选：{[s['key'] for s in SCENES]}")

    print("=" * 64)
    print(f" EP13《外骨骼》场景参考图  |  共 {len(scenes)} 张  |  out: {OUT}")
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
