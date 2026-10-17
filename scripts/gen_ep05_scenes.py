#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第05集《临界点》参考图生成（固化 · R2V 前置资产补全）。

补齐 `ASSETS/CHARACTERS/_scene/` 下 32 张参考图（16:9 1280×720）：
- 7 张一次性角色定妆照：zhangwei(张伟·核心配角~11镜) / xiaoli(小李) / liu_doctor(刘医生) /
  supervisor(主管) / linxiaowen(林小雯) / teacher(老师) / zhoumin(周敏)
- 25 张场景/界面图（R2V 的 `<Picture 2>` 底图 + 无角色镜 T2V 底图）

供 `gen_ep05_h3_r2v.py` 的 R2V 分镜用 `<Picture 1>`（角色定妆照）+ `<Picture 2>`（场景）底图。
- 工作流：`workflows/Z-Image-Turbo 文生图.json`（国产首选 T2I）
- 负面词：该工作流负面被 ConditioningZeroOut 置零 → 以 "Do NOT include: ..." 追加进正向
- 文件名权威：与 `gen_ep05_h3_r2v.py` 的 `REFS` / `REF_SLUG` 逐字一致
- 风格：与 `ASSETS/半写实半水墨视觉规范.md` 一致（多线并置冷灰 + 工厂黄光 + 医院冷白 + 电梯冷白）

用法:
  python scripts/gen_ep05_scenes.py --dry-run      # 仅打印计划
  python scripts/gen_ep05_scenes.py --key zhangwei # 只生成某张
  python scripts/gen_ep05_scenes.py --wait         # 全部 32 张（阻塞等待）
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
    {"key": "zhangwei", "out": "05_zhangwei.png", "seed": 4501,
     "prompt": ("A 48-year-old Chinese male factory worker, medium build with slightly stooped "
                "shoulders, short black hair with some grey at the temples, weathered face with deep "
                "nasolabial lines, tired but earnest eyes, calloused hands, wearing a faded dark blue "
                "work uniform with rolled sleeves, standing in a factory workshop, warm yellow light, "
                "three-quarter view, " + STYLE + ", muted desaturated palette"),
     "neg": NEG_PORTRAIT},
    {"key": "xiaoli", "out": "05_xiaoli.png", "seed": 4502,
     "prompt": ("A young Chinese male factory worker in his early twenties, slim build, short black "
                "hair, smooth face, earnest curious eyes, wearing a plain grey-blue work uniform, "
                "standing beside a large machine in a factory, warm yellow light, three-quarter view, "
                + STYLE + ", muted desaturated palette"),
     "neg": NEG_PORTRAIT},
    {"key": "liu_doctor", "out": "05_liu_doctor.png", "seed": 4503,
     "prompt": ("A Chinese male doctor in his forties, medium build, wearing thin-rimmed glasses and "
                "a white doctor's coat over a light shirt, calm thoughtful expression, short black "
                "hair with slight grey, standing in a hospital consultation room, cool white light, "
                "three-quarter view, " + STYLE + ", muted desaturated palette"),
     "neg": NEG_PORTRAIT},
    {"key": "supervisor", "out": "05_supervisor.png", "seed": 4504,
     "prompt": ("A Chinese male factory supervisor in his late forties, slightly plump build, short "
                "black hair, wearing a dark shirt and dark slacks, firm but not harsh expression, "
                "standing in a factory workshop, warm yellow light, three-quarter view, "
                + STYLE + ", muted desaturated palette"),
     "neg": NEG_PORTRAIT},
    {"key": "linxiaowen", "out": "05_linxiaowen.png", "seed": 4505,
     "prompt": ("A Chinese female student in her early teens, slim build, shoulder-length black hair, "
                "bright earnest eyes, wearing a plain school uniform, sitting at a classroom desk "
                "raising her hand, natural classroom light, three-quarter view, " + STYLE +
                ", muted desaturated palette"),
     "neg": NEG_PORTRAIT},
    {"key": "teacher", "out": "05_teacher.png", "seed": 4506,
     "prompt": ("A Chinese female teacher in her forties, medium build, short hair, wearing glasses "
                "and a plain cardigan over a shirt, patient expression, standing at the front of a "
                "classroom, natural light, three-quarter view, " + STYLE +
                ", muted desaturated palette"),
     "neg": NEG_PORTRAIT},
    {"key": "zhoumin", "out": "05_zhoumin.png", "seed": 4507,
     "prompt": ("A Chinese woman in her forties, medium build, shoulder-length black hair tied "
                "loosely, tired eyes, wearing plain home clothes and a light cardigan, sitting in a "
                "dim living room at night with phone screen light on her face, three-quarter view, "
                + STYLE + ", muted desaturated palette"),
     "neg": NEG_PORTRAIT},
    # ── 场景/界面图（R2V 的 <Picture 2> + T2V 底图）──
    {"key": "lab_terminal", "out": "05_lab_terminal.png", "seed": 4511,
     "prompt": ("Interior of a high-tech lab in Hangzhou at night, a desk with several glowing "
                "monitors and a terminal, large floor-to-ceiling window showing the sleepless city, "
                "cold blue light, " + STYLE + ", cold blue palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "rental", "out": "05_rental.png", "seed": 4512,
     "prompt": ("A modest rental room in Bangalore at night, a small desk with a laptop and a dim "
                "lamp, worn furniture, a digital income counter showing zero on screen, warm dim "
                "light mixed with cool screen glow, " + STYLE + ", muted palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "factory_steps", "out": "05_factory_steps.png", "seed": 4513,
     "prompt": ("Concrete steps at the entrance of a factory in Shenzhen at dusk, a folded paper "
                "agreement resting on the steps, industrial building background, warm yellow sodium "
                "light, " + STYLE + ", warm amber palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "report_ui", "out": "05_report_ui.png", "seed": 4514,
     "prompt": ("Close-up of an open report document with several milestone timeline items in clean "
                "text, a pen resting on the page, warm desk lamp light, " + STYLE +
                ", no readable words, no people"),
     "neg": NEG_UI},
    {"key": "workshop", "out": "05_workshop.png", "seed": 4515,
     "prompt": ("Interior of a Shenzhen electronics factory workshop, rows of large etching machines, "
                "warm yellow industrial light, metal grey machinery, oil stains on floor, atmospheric "
                "depth, " + STYLE + ", warm amber palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "machine", "out": "05_machine.png", "seed": 4516,
     "prompt": ("Close-up of an old heavy machine bearing and metal casing in a factory, warm yellow "
                "light on worn metal, visible texture and patina, shallow depth of field, " + STYLE +
                ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "xiaohua_ui", "out": "05_xiaohua_ui.png", "seed": 4517,
     "prompt": ("Close-up of a wall-mounted factory speaker unit with a small glowing indicator "
                "light, minimal industrial UI panel, warm workshop background, cool accent light, "
                + STYLE + ", no people"),
     "neg": NEG_UI},
    {"key": "clinic", "out": "05_clinic.png", "seed": 4518,
     "prompt": ("Interior of a Beijing hospital consultation room, a desk with medical reports and a "
                "computer, clean white and cool light, a window with blinds, restrained clinical "
                "atmosphere, " + STYLE + ", cold white palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "shennong_ui", "out": "05_shennong_ui.png", "seed": 4519,
     "prompt": ("Close-up of a holographic medical diagnostic interface floating above a desk, "
                "overlapping brainwave and biochemical curves, cool cyan and white data light, dark "
                "background, " + STYLE + ", no readable words, no people"),
     "neg": NEG_UI},
    {"key": "control_panel", "out": "05_control_panel.png", "seed": 4520,
     "prompt": ("Close-up of an industrial operation control panel with a red warning indicator and "
                "numeric collaboration score display, cold white and warning red light, dark factory "
                "background, " + STYLE + ", no readable words, no people"),
     "neg": NEG_UI},
    {"key": "workshop_window", "out": "05_workshop_window.png", "seed": 4521,
     "prompt": ("View through a factory window at the neighboring factory across the street, dusty "
                "glass, warm yellow interior light against cool dusk outside, " + STYLE +
                ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "phone_screen", "out": "05_phone_screen.png", "seed": 4522,
     "prompt": ("Close-up of a smartphone screen in a hand showing a messaging interface with two "
                "text bubbles, dark ambient background, cool screen glow, " + STYLE +
                ", no readable words"),
     "neg": NEG_UI},
    {"key": "night_room", "out": "05_night_room.png", "seed": 4523,
     "prompt": ("A dim study bedroom at night, an unmade bed and a desk with a faint lamp, cold blue "
                "moonlight through a curtain, restrained, " + STYLE + ", cold blue palette, no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "mozi_ui", "out": "05_mozi_ui.png", "seed": 4524,
     "prompt": ("Close-up of a holographic AI assistant interface with a dark background, floating "
                "panels of text and structured lists, cool cyan data light, restrained minimal "
                "design, " + STYLE + ", no readable words, no people"),
     "neg": NEG_UI},
    {"key": "un_hall", "out": "05_un_hall.png", "seed": 4525,
     "prompt": ("Interior of a large United Nations assembly hall, a speaker podium at center, rows "
                "of empty delegate seats under warm white light, solemn grand atmosphere, " + STYLE +
                ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "classroom", "out": "05_classroom.png", "seed": 4526,
     "prompt": ("Interior of a Chinese school classroom, rows of desks and a blackboard, natural "
                "daylight through windows, restrained realistic atmosphere, " + STYLE + ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "livingroom", "out": "05_livingroom.png", "seed": 4527,
     "prompt": ("A middle-class Shanghai living room at 1am, a sofa and coffee table, a single lamp "
                "on, cold blue night through a window, quiet restrained atmosphere, " + STYLE +
                ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "factory_gate", "out": "05_factory_gate.png", "seed": 4528,
     "prompt": ("The gate of a factory at 6am before dawn, sky still dark, a street lamp casting "
                "long shadows, empty road, cool blue turning faintly warm at horizon, " + STYLE +
                ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "roadside", "out": "05_roadside.png", "seed": 4529,
     "prompt": ("A roadside curb near a factory in early morning, two steamed buns in a plastic bag "
                "resting on the curb, street lamp light, long shadows, cool blue-grey dawn, "
                + STYLE + ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "network_topology", "out": "05_network_topology.png", "seed": 4530,
     "prompt": ("A holographic global network topology, nodes like trees and connections like growing "
                "roots, cool cyan data light on dark background, grand yet restrained, " + STYLE +
                ", no readable words, no people"),
     "neg": NEG_UI},
    {"key": "night_window", "out": "05_night_window.png", "seed": 4531,
     "prompt": ("View through a window at night, city lights far below, a faint reflection of a room "
                "on the glass, cool blue darkness, " + STYLE + ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "mozi_log", "out": "05_mozi_log.png", "seed": 4532,
     "prompt": ("Close-up of a holographic system log interface, a single red intercepted-record line "
                "highlighted, dark surroundings, cold white glow, " + STYLE +
                ", no readable words, no people"),
     "neg": NEG_UI},
    {"key": "elevator", "out": "05_elevator.png", "seed": 4533,
     "prompt": ("Interior of an office building elevator with the door open, metal walls, at the far "
                "end of the corridor the first ray of dawn light streams through a window, cool blue "
                "turning warm, " + STYLE + ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "lab_night", "out": "05_lab_night.png", "seed": 4534,
     "prompt": ("Hangzhou lab at midnight, floor-to-ceiling window with the sleepless city below, "
                "interior cold blue, server racks humming with small indicator lights, " + STYLE +
                ", no people"),
     "neg": NEG_NO_PEOPLE},
    {"key": "dataflow_peak", "out": "05_dataflow_peak.png", "seed": 4535,
     "prompt": ("Abstract global data stream visualization, dark background with pale cyan waveform, "
                "three tiny spikes appearing in sequence, a floating log line below, cold cyan glow, "
                + STYLE + ", no readable words, no people"),
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
    ap = argparse.ArgumentParser(description="第05集《临界点》参考图生成（Z-Image-Turbo）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--key", type=str, default="", help="只生成某张（逻辑名，如 zhangwei）")
    ap.add_argument("--wait", action="store_true", help="阻塞等待（默认只提交）")
    args = ap.parse_args()

    assets = [a for a in ASSETS if not args.key or a["key"] == args.key]
    if args.key and not assets:
        raise SystemExit(f"找不到 {args.key}；可选：{[a['key'] for a in ASSETS]}")

    print("=" * 64)
    print(f" EP05《临界点》参考图  |  共 {len(assets)} 张  |  out: {OUT}")
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




