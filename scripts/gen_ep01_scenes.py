#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第1集《晨钟》参考图生成（固化 · R2V 前置资产补全）。

补齐 `ASSETS/CHARACTERS/_scene/` 下 16 张参考图（16:9 1280×720）：
- 4 张一次性角色定妆照：linwei_youth / father / worker / taipei_lead
- 12 张无角色场景图：bedroom / classroom / phone / bookshelf / livingroom /
  worker_room / apartment / livestream_wall / corridor / elevator / meeting / car_window

供 `gen_ep01_h3_r2v.py` 的 R2V 分镜作 `<Picture 1>`（角色）/`<Picture 2>`（场景）底图。
- 工作流：`workflows/Z-Image-Turbo 文生图.json`（国产首选 T2I）
- 负面词：该工作流负面被 ConditioningZeroOut 置零 → 以 "Do NOT include: ..." 追加进正向
- 文件名权威：与 `gen_ep01_h3_r2v.py` 的 `REFS` / `REF_SLUG` 逐字一致
- 风格：与 `ASSETS/半写实半水墨视觉规范.md` §3 风格分组一致

用法:
  python scripts/gen_ep01_scenes.py --dry-run     # 仅打印计划
  python scripts/gen_ep01_scenes.py --key bedroom # 只生成某张
  python scripts/gen_ep01_scenes.py               # 全部 16 张（阻塞等待）
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
    {"key": "linwei_youth", "out": "01_linwei_youth.png", "seed": 1101,
     "prompt": ("A young Chinese schoolgirl around twelve years old, neat low ponytail with soft "
                "stray strands, no makeup, fair clear skin, wearing a plain light school uniform "
                "with a white collar, looking out a bright classroom window with an intelligent but "
                "slightly bored expression, soft bright daylight on her face, clean youthful face, "
                + STYLE + ", light ink wash, generous negative space, very faint cyan accent"),
     "neg": NEG_PORTRAIT},
    {"key": "father", "out": "01_father.png", "seed": 1102,
     "prompt": ("A Chinese man around fifty years old, short graying hair, plain casual home "
                "clothes, sitting on a living-room sofa staring at a glowing livestream screen, the "
                "screen light falling on his weathered face, warm living-room at evening, "
                + STYLE + ", ochre and light ink, warm subdued tone"),
     "neg": NEG_PORTRAIT},
    {"key": "worker", "out": "01_worker.png", "seed": 1103,
     "prompt": ("A Chinese manual worker around fifty years old, dark worn work jacket, hands with "
                "rough calluses resting on a table, several sheets of a paper questionnaire spread "
                "on the table, thinking quietly with a tired but steady expression, a single warm "
                "tungsten desk lamp as the only light, dim rented room around him, "
                + STYLE + ", ochre and light ink, dry-brush worn texture"),
     "neg": NEG_PORTRAIT},
    {"key": "taipei_lead", "out": "01_taipei_lead.png", "seed": 1104,
     "prompt": ("An East Asian professional woman in her late thirties, short neat hair, subtle "
                "makeup, wearing a tailored dark blazer, speaking calmly to camera in a video-call "
                "framing, neutral office background, cool restrained lighting, "
                + STYLE + ", cyan and light ink, clear clean lines"),
     "neg": NEG_PORTRAIT},

    # ── 无角色场景图（R2V 的 <Picture 2>）──
    {"key": "bedroom", "out": "01_bedroom.png", "seed": 1105,
     "prompt": ("A dark apartment bedroom at three in the morning, an unmade bed, faint cold "
                "blue-gray light from a window edge falling across the bed and floor, deep shadows, "
                "empty and still, cinematic, " + STYLE + ", light ink and cyan, generous negative "
                "space, cold night tone"),
     "neg": NEG_NO_PEOPLE},
    {"key": "classroom", "out": "01_classroom.png", "seed": 1106,
     "prompt": ("A bright middle-school classroom in the afternoon, rows of empty wooden desks, a "
                "blackboard at the front, sunlight streaming through large windows, dust in the air, "
                "quiet and empty, cinematic, " + STYLE + ", light ink wash, generous negative space"),
     "neg": NEG_NO_PEOPLE},
    {"key": "phone", "out": "01_phone_screen.png", "seed": 1107,
     "prompt": ("Extreme close-up of a smartphone screen glowing in a dark room, a video streaming "
                "interface with a play button and a progress bar, a fast-scrolling feed, cold blue "
                "screen light, dark blurred surroundings, cinematic, " + STYLE + ", cyan and light ink"),
     "neg": NEG_UI},
    {"key": "bookshelf", "out": "01_bookshelf.png", "seed": 1108,
     "prompt": ("A home study bookshelf in a young student's room, rows of thick books, one thick "
                "book pulled partway out, soft daylight from a window beside it, quiet and clean, "
                "cinematic, " + STYLE + ", light ink wash, generous negative space"),
     "neg": NEG_NO_PEOPLE},
    {"key": "livingroom", "out": "01_livingroom.png", "seed": 1109,
     "prompt": ("A Chinese family living room at evening, a worn sofa facing a glowing livestream "
                "screen, the screen light washing over the room, warm dim lamps, quiet domestic "
                "atmosphere, cinematic, " + STYLE + ", ochre and light ink with faint gamboge glow"),
     "neg": NEG_NO_PEOPLE},
    {"key": "worker_room", "out": "01_worker_room.png", "seed": 1110,
     "prompt": ("A humble rented room of a manual worker at night, a simple wooden table with a few "
                "sheets of a paper questionnaire, a single warm tungsten desk lamp as the only light, "
                "everything else in deep shadow, worn walls, cinematic, " + STYLE + ", ochre and "
                "light ink, dry-brush worn texture"),
     "neg": NEG_NO_PEOPLE},
    {"key": "apartment", "out": "01_apartment.png", "seed": 1111,
     "prompt": ("A metal trash bin in an apartment building stairwell at night, a thick stack of "
                "paper questionnaires, cold dim corridor light, concrete wall, quiet and empty, "
                "cinematic, " + STYLE + ", light ink and cyan"),
     "neg": NEG_NO_PEOPLE},
    {"key": "livestream_wall", "out": "01_livestream_wall.png", "seed": 1112,
     "prompt": ("A plain white wall with a wooden desk in front of it at night, a small desk lamp "
                "with warm light, a blank wall as a livestream backdrop, cozy and quiet, cinematic, "
                + STYLE + ", ochre and light ink, warm subdued tone"),
     "neg": NEG_NO_PEOPLE},
    {"key": "corridor", "out": "01_corridor.png", "seed": 1113,
     "prompt": ("A tech-company office corridor, white walls and glass doors, cold fluorescent "
                "ceiling light, long clean perspective, no one present, cinematic, " + STYLE +
                ", light ink and cyan with dry-brush edges"),
     "neg": NEG_NO_PEOPLE},
    {"key": "elevator", "out": "01_elevator.png", "seed": 1114,
     "prompt": ("The interior of a modern office-building elevator with mirrored metal walls, cold "
                "neutral lighting, buttons and a floor indicator, empty and still, cinematic, "
                + STYLE + ", light ink and cyan"),
     "neg": NEG_NO_PEOPLE},
    {"key": "meeting", "out": "01_meeting.png", "seed": 1115,
     "prompt": ("A tech-company meeting room with a long table and chairs, a large screen at the far "
                "end of the table, cold gray daylight from windows, restrained institutional palette, "
                "empty, cinematic, " + STYLE + ", light ink and cyan, clear clean lines"),
     "neg": NEG_NO_PEOPLE},
    {"key": "car_window", "out": "01_car_window.png", "seed": 1116,
     "prompt": ("View through the rear window of an autonomous car at night, the Shenzhen city "
                "skyline and street lights passing outside, warm city lights against a dark ink sky, "
                "soft reflections on the glass, cinematic, " + STYLE + ", ochre and gamboge, light "
                "ink night sky"),
     "neg": NEG_NO_PEOPLE},
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


def build_workflow(asset: dict) -> dict:
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


def run_one(asset: dict, wait: bool = True):
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
    ap = argparse.ArgumentParser(description="第1集《晨钟》参考图生成（Z-Image-Turbo）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--key", type=str, default="", help="只生成某张（逻辑名，如 bedroom）")
    ap.add_argument("--wait", action="store_true", help="阻塞等待（默认只提交）")
    args = ap.parse_args()

    assets = [a for a in ASSETS if not args.key or a["key"] == args.key]
    if args.key and not assets:
        raise SystemExit(f"找不到 {args.key}；可选：{[a['key'] for a in ASSETS]}")

    print("=" * 64)
    print(f" EP01《晨钟》参考图  |  共 {len(assets)} 张  |  out: {OUT}")
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
