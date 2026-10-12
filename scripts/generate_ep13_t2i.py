#!/usr/bin/env python3
"""
第13集《外骨骼》T2I 静态图批量生成脚本（固化 · S3 重做 · 新口径·去 TTS）。

作用：生成第 13 集「角色状态帧 + 场景图 + 虚拟观众 + 道具 + UI」共 14 张基础图，
       作为后续 I2V（Minimax H3）的分镜帧输入。与 EP18 范式口径一致：
   - 人物镜头（莎拉 / 师兄）→ LongCat Image Edit（输入=各自主定妆照，保角色一致）
   - 非人物镜头（场景 / 虚拟观众 / 道具 / UI）→ Z-Image-Turbo 文生图

⚠️ 台词/人声一律由 MiniMax H3 随视频生成（写进 I2V prompt 的 Audio:），
   本脚本只出「帧」，不生成任何 TTS 音轨（2026-10-11 用户令：禁用 TTS）。

用法:
  python scripts/generate_ep13_t2i.py --dry-run      # 仅打印计划
  python scripts/generate_ep13_t2i.py --shot 莎拉-01 # 仅生成某张
  python scripts/generate_ep13_t2i.py                # 全部 14 张

产出:
  OUTPUT/13_外骨骼/frames/13_*.png（14 张）+ manifest.json
"""
import json
import time
import uuid
import shutil
import urllib.request
import urllib.error
import urllib.parse
import argparse
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
COMFYUI_URL = "http://127.0.0.1:8188"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "OUTPUT" / "13_外骨骼" / "frames"
ZIMAGE_WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "Z-Image-Turbo 文生图.json"
IMAGE_EDIT_WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "Image Edit (LongCat Image Edit).json"

SARAH_REF = PROJECT_ROOT / "ASSETS" / "CHARACTERS" / "08_莎拉·赵" / "主定妆照.png"
SHIXIONG_REF = PROJECT_ROOT / "ASSETS" / "CHARACTERS" / "师兄" / "主定妆照.png"
SARAH_REF_TARGET = "ref_sarah_13.png"
SHIXIONG_REF_TARGET = "ref_shixiong_13.png"

# ── 负面词 ────────────────────────────────────────────
NEG_SARAH = (
    "ugly, deformed, bad anatomy, disfigured, poorly drawn face, mutation, extra limb, "
    "extra fingers, fused fingers, too many fingers, blurry, watermark, text, logo, "
    "oversaturated, plastic skin, heavy makeup, beauty filter, anime, cartoon, illustration, "
    "3D render, nerd stereotype, thick glasses, awkward posture, overly dramatic stage "
    "performer, diva, professional actress, cheerful, smiling excessively, emotional outburst, "
    "perfect skin, beauty dish lighting, fashion magazine"
)
NEG_SHIXIONG = (
    "smile, laughing, happy, cheerful, young, handsome, energetic, muscular, romantic, "
    "clean-shaven model, makeup, skincare glow, suit, tie, CEO, luxury office, warm lighting, "
    "golden hour, fashion, influencer, celebrity, K-pop, idol, anime, cartoon, 3D render, "
    "oversaturated, plastic skin, beauty filter, deformed, ugly, duplicate, watermark, "
    "signature, text, logo"
)
NEG_GENERIC = (
    "cartoon, anime, 3D render, oversaturated, bright colors, deformed, extra fingers, "
    "mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, "
    "low quality, normal quality, jpeg artifacts"
)


def _detect_comfyui_base() -> Path:
    for c in [Path("E:/code/ComfyUI"),
              Path("E:/ComfyUI"),
              Path("E:/ComfyUI_windows_portable/ComfyUI"),
              Path.home() / "ComfyUI"]:
        if c.exists():
            return c
    return Path("E:/code/ComfyUI")


def get_comfyui_input_dir() -> Path:
    d = _detect_comfyui_base() / "input"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_comfyui_output_dir() -> Path:
    return _detect_comfyui_base() / "output"


# ── 14 张基础图规格 ────────────────────────────────────
# image_edit 的 megapixels=0.92 → 实际输出约 1312×736（16:9，LongCat 按 32 倍数取整）
SPECS = [
    # — 莎拉状态帧（image_edit，输入主定妆照）—
    {
        "name": "莎拉-01_工位解释外骨骼", "mode": "image_edit", "megapixels": 0.92, "seed": 100,
        "out": "13_sarah_01_desk_explaining.png",
        "ref": SARAH_REF, "ref_target": SARAH_REF_TARGET, "neg": NEG_SARAH,
        "prompt": (
            "Same 30-year-old Chinese woman with medium-short dark hair, sitting at a tech office "
            "desk, two monitors glowing — left monitor plays her own stand-up performance video, "
            "right monitor shows a world-model interface rendering virtual audience faces with a "
            "green/yellow/red laughter heatmap, one hand gesturing pointing at the heatmap region, "
            "explaining something important but unsure if others can understand, cold white office "
            "fluorescent light mixed with warm screen light, semi-realistic ink wash style bleeding "
            "from monitor edges, photorealistic base"
        ),
    },
    {
        "name": "莎拉-02_地铁观察者", "mode": "image_edit", "megapixels": 0.92, "seed": 101,
        "out": "13_sarah_02_subway_observing.png",
        "ref": SARAH_REF, "ref_target": SARAH_REF_TARGET, "neg": NEG_SARAH,
        "prompt": (
            "Same 30-year-old Chinese woman standing in a crowded Shanghai morning subway car, one "
            "hand holding an overhead strap, NOT looking at a phone while others around her stare at "
            "screens, quietly observing a middle-aged woman with a grocery bag, a student with leaky "
            "headphones, a dozing old man, harsh fluorescent light plus tunnel light sweeping through "
            "windows, ink wash only faintly in the window reflections, semi-realistic ink wash style, "
            "photorealistic base"
        ),
    },
    {
        "name": "莎拉-03_吧台散场", "mode": "image_edit", "megapixels": 0.92, "seed": 102,
        "out": "13_sarah_03_bar_aftermath.png",
        "ref": SARAH_REF, "ref_target": SARAH_REF_TARGET, "neg": NEG_SARAH,
        "prompt": (
            "Same 30-year-old Chinese woman sitting sideways at a closed comedy-club bar counter after "
            "the show, warm dim light, smartphone screen glowing with a WeChat message, cold white "
            "screen light on the lower half of her face, finger just finished typing a reply not yet "
            "sent, expression sincere and quiet, rest of the frame in darkness, warm amber + dark wine "
            "red + phone cold white, ink bleeding from bar shadows, semi-realistic ink wash style, "
            "photorealistic base"
        ),
    },
    # — 师兄状态帧（image_edit，输入主定妆照）—
    {
        "name": "师兄-01_咖啡杯", "mode": "image_edit", "megapixels": 0.92, "seed": 200,
        "out": "13_shixiong_01_coffee.png",
        "ref": SHIXIONG_REF, "ref_target": SHIXIONG_REF_TARGET, "neg": NEG_SHIXIONG,
        "prompt": (
            "Same 31-year-old Chinese man with black-framed glasses, thin and tall, tousled short dark "
            "hair, deep-set tired eyes with subtle dark circles, holding a white ceramic coffee mug with "
            "company logo, half profile, dark grey hoodie over black t-shirt, cold white fluorescent "
            "office light from above, faint knowing micro-expression at corner of mouth, pores and eye "
            "lines visible, semi-realistic ink wash style bleeding from background edges, "
            "photorealistic base"
        ),
    },
    # — 场景图（zimage）—
    {
        "name": "工位-01_外骨骼UI", "mode": "zimage", "seed": 600,
        "out": "13_office_01_exoskeleton_ui.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "A dual-monitor engineering UI for an AI comedy tool, left monitor shows a video input "
            "window of a woman on an open-mic stage holding a wired microphone with playback timecode, "
            "center shows virtual audience rendering — rows of imaginary audience faces each with "
            "expressions, one face marked with a green AI box, right shows a laughter-intensity heatmap "
            "over virtual audience seats in green/yellow/red zones, engineering interface not sci-fi "
            "HUD, grey-blue engineering color + green/yellow/red heatmap colors, clean restrained UI, "
            "16:9"
        ),
    },
    {
        "name": "地铁-01_早高峰", "mode": "zimage", "seed": 601,
        "out": "13_subway_01_rush_hour.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "Shanghai subway line-2 style train car during 7-8am rush hour, long stainless seats with "
            "blue plastic panels, overhead grab handles, red LED information screen above the door, "
            "crowded but not suffocating — middle-aged woman with grocery bag, student with leaky "
            "headphones, old man dozing in a corner, some on phones some staring blankly, harsh "
            "fluorescent tube light with occasional tunnel light sweeping through windows, window glass "
            "reflects blurred figures, real everyday not sci-fi, warm grey + harsh white fluorescent, "
            "faint ink wash only in window reflections, 16:9"
        ),
    },
    {
        "name": "实验室-01_2017深夜", "mode": "zimage", "seed": 602,
        "out": "13_lab_01_2017_night.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "A Chinese university computer lab in 2017, grey floor, several old desktop PC towers "
            "stacked under desks, old CRT/LCD monitors with wide bezels and warmer blue glow, "
            "whiteboard with handwritten formulas scrawled, late night with only a desk lamp warm light "
            "on the work area, dust motes floating in light, two chairs side by side one empty, a coffee "
            "mug on the desk in front of the empty chair still steaming, nostalgic warm yellow + old "
            "CRT blue, ink bleeding from frame edges, 16:9"
        ),
    },
    {
        "name": "酒吧-01_散场吧台", "mode": "zimage", "seed": 603,
        "out": "13_bar_01_aftermath.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "An open-mic comedy club bar after the show has ended, audience gone, chairs pushed under "
            "tables, empty mic stand on stage, one warm dim light still on at the bar counter, wood "
            "grain with beer glass water rings, an empty beer bottle, a stainless bottle opener, "
            "blurred figure tidying chairs in the deep background, not lonely but quiet after it is "
            "over, warm amber + dark wine red, ink bleeding from shadows, 16:9"
        ),
    },
    # — 虚拟观众（zimage · P0 视觉心脏）—
    {
        "name": "虚拟观众-01_想象的脸", "mode": "zimage", "seed": 700,
        "out": "13_virtual_audience_01_imaginary_face.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "A single rendered virtual audience face, a face that does not exist in reality, smiling "
            "and laughing, skin slightly too perfect and too smooth, marked with a green AI bounding box, "
            "cold blue-grey synthetic tone, uncanny subtle artificiality, semi-realistic with ink wash "
            "bleeding at the edges, cinematic close-up, 16:9"
        ),
    },
    {
        "name": "虚拟观众-02_渲染vs真实", "mode": "zimage", "seed": 701,
        "out": "13_virtual_audience_02_render_vs_real.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "A diptych split composition: top half a rendered virtual face smiling with green AI box "
            "and too-perfect skin; bottom half the same camera angle but a real open-mic audience — a "
            "real young man wearing a baseball cap holding a beer glass, laughing a real imperfect laugh "
            "with pores and tooth gaps and eye wrinkles, top half cool blue-grey synthetic, bottom half "
            "warm real light, ink wash only in the top half, bottom fully realistic, 16:9"
        ),
    },
    # — 道具（zimage）—
    {
        "name": "道具-01_笔记本标签", "mode": "zimage", "seed": 800,
        "out": "13_prop_01_notebook_label.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "Close-up of a dark hardcover A5 notebook cover, a strip of white paper masking tape on the "
            "cover with handwritten Chinese characters, tape edge slightly lifting with transparency, "
            "corner of a monitor blue glow reflection on the desk, cold white office light plus one warm "
            "desk lamp, ink bleeding from the tape edge, 16:9"
        ),
    },
    {
        "name": "道具-02_微信对话", "mode": "zimage", "seed": 801,
        "out": "13_prop_02_wechat_hao.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "Close-up of a smartphone screen on an office desk, WeChat chat interface, top green message "
            "bubbles from the user, below an empty white bubble just transitioned from typing, then a "
            "white bubble with a single short reply, phone cold white light is the only light in the "
            "pre-dawn blue-grey dark, faint fingerprints on the screen, ink bleeding from phone edge "
            "into desk shadow, 16:9"
        ),
    },
    # — UI（zimage）—
    {
        "name": "UI-01_外骨骼主界面", "mode": "zimage", "seed": 900,
        "out": "13_ui_01_exoskeleton_clean.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "Engineering UI of an AI comedy tool without any person, left 40 percent a video player "
            "frame black with playback controls and timecode, center 40 percent virtual audience "
            "rendering area grey background with multiple audience boxes each a rendered face with "
            "heatmap overlay green/yellow/red regions, right 20 percent a data panel with green yellow "
            "red thresholds and a model version label, top small caption text, grey-blue engineering "
            "tone + green/yellow/red heatmap, practical tool not sci-fi, 16:9"
        ),
    },
    {
        "name": "UI-02_双标注小周", "mode": "zimage", "seed": 901,
        "out": "13_ui_02_double_annotation_xiaozhou.png", "width": 1280, "height": 720, "neg": NEG_GENERIC,
        "prompt": (
            "Close-up detail of a virtual audience seat third row, a rendered audience face with a "
            "machine-style green AI bounding box in light green rectangle and white text, overlaid with "
            "a red handwritten name in rounded irregular handwriting, the same data with two annotations "
            "— machine world green box versus human world red handwritten name, background is the "
            "rendered virtual face smiling, grey-blue engineering + green box + red text, 16:9"
        ),
    },
]

# ── ComfyUI API ───────────────────────────────────────
def comfyui_request(endpoint, data=None, method="POST"):
    url = f"{COMFYUI_URL}{endpoint}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def queue_prompt(workflow):
    payload = {"prompt": workflow, "client_id": f"ep13_{uuid.uuid4().hex[:8]}"}
    pid = comfyui_request("/prompt", payload).get("prompt_id", "")
    if not pid:
        raise RuntimeError("提交失败")
    return pid


def wait_for_prompt(prompt_id, timeout=900):
    start = time.time()
    while time.time() - start < timeout:
        try:
            history = comfyui_request(f"/history/{prompt_id}", method="GET")
        except urllib.error.URLError:
            time.sleep(3)
            continue
        if prompt_id in history:
            return history[prompt_id]
        time.sleep(3)
    raise TimeoutError(f"Prompt {prompt_id} 超时")


def find_output_files(history_entry):
    outputs = []
    for _nid, nd in history_entry.get("outputs", {}).items():
        for img in nd.get("images", []):
            outputs.append({"filename": img["filename"],
                            "subfolder": img.get("subfolder", ""),
                            "type": img.get("type", "output")})
    return outputs


def download_output_image(out, dst):
    params = urllib.parse.urlencode({"filename": out["filename"],
                                     "subfolder": out.get("subfolder", ""),
                                     "type": out.get("type", "output")})
    url = f"{COMFYUI_URL}/view?{params}"
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = resp.read()
            if len(data) > 100:
                dst.write_bytes(data)
                return True
    except Exception as e:
        print(f"    [WARNING] /view 失败: {e}")
    src = get_comfyui_output_dir() / out.get("subfolder", "") / out["filename"]
    if src.exists():
        shutil.copy2(src, dst)
        return True
    return False


def upload_ref_to_comfyui(ref_path, target_name):
    """把定妆照复制到 ComfyUI input，供 LoadImage 使用。"""
    dst = get_comfyui_input_dir() / target_name
    if not (dst.exists() and dst.stat().st_size == ref_path.stat().st_size):
        shutil.copy2(ref_path, dst)
    return target_name


def load_workflow(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_zimage_t2i(prompt, neg_prompt, width, height, seed):
    wf = load_workflow(ZIMAGE_WORKFLOW_PATH)
    full_prompt = prompt.strip()
    if neg_prompt:
        full_prompt += f"\n\nDo NOT include: {neg_prompt}"
    for _nid, node in wf.items():
        ct = node.get("class_type")
        if ct == "CLIPTextEncode":
            node["inputs"]["text"] = full_prompt
        elif ct == "EmptySD3LatentImage":
            node["inputs"]["width"] = width
            node["inputs"]["height"] = height
            node["inputs"]["batch_size"] = 1
        elif ct == "KSampler":
            node["inputs"]["seed"] = int(seed)
    return wf


def build_image_edit(prompt, neg_prompt, ref_filename, megapixels, seed):
    wf = load_workflow(IMAGE_EDIT_WORKFLOW_PATH)
    for _nid, node in wf.items():
        if node.get("class_type") == "LoadImage":
            node["inputs"]["image"] = ref_filename
    for _nid, node in wf.items():
        if node.get("class_type") == "ImageScaleToTotalPixels":
            node["inputs"]["megapixels"] = float(megapixels)
    enc = []
    for _nid, node in wf.items():
        if node.get("class_type") == "TextEncodeQwenImageEdit":
            enc.append((_nid, node))
    enc.sort(key=lambda x: x[0])
    if len(enc) >= 1:
        enc[0][1]["inputs"]["prompt"] = prompt.strip()
    if len(enc) >= 2:
        enc[1][1]["inputs"]["prompt"] = neg_prompt.strip() if neg_prompt else ""
    for _nid, node in wf.items():
        if node.get("class_type") == "KSampler":
            node["inputs"]["seed"] = int(seed)
    return wf


# ── 单张生成 ──────────────────────────────────────────
def run_one(spec, output_dir):
    out_file = output_dir / spec["out"]
    if spec["mode"] == "image_edit":
        ref = spec["ref"]
        if not ref.exists():
            print(f"  [ERROR] 缺定妆照: {ref}")
            return False
        target = upload_ref_to_comfyui(ref, spec["ref_target"])
        wf = build_image_edit(spec["prompt"], spec.get("neg", ""), target,
                              spec["megapixels"], spec["seed"])
    else:
        wf = build_zimage_t2i(spec["prompt"], spec.get("neg", ""),
                              spec["width"], spec["height"], spec["seed"])

    pid = queue_prompt(wf)
    print(f"    已提交 {pid[:8]}...")
    hist = wait_for_prompt(pid)
    outs = find_output_files(hist)
    if not outs:
        print(f"    [ERROR] 无输出")
        return False
    output_dir.mkdir(parents=True, exist_ok=True)
    ok = download_output_image(outs[0], out_file)
    if ok:
        kb = out_file.stat().st_size // 1024
        print(f"    ✅ {out_file.name} ({kb}KB, seed={spec['seed']})")
    else:
        print(f"    ❌ 下载失败")
    return ok


def write_manifest(ok_map):
    rows = []
    for s in SPECS:
        p = OUTPUT_DIR / s["out"]
        rows.append({
            "out": s["out"],
            "name": s["name"],
            "mode": s["mode"],
            "seed": s["seed"],
            "ok": ok_map.get(s["out"], False),
            "bytes": p.stat().st_size if p.exists() else 0,
        })
    manifest = {"chapter": "13_外骨骼", "frames": rows, "total": len(rows)}
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"    manifest.json → {len(rows)} 条")


def main():
    ap = argparse.ArgumentParser(description="第13集《外骨骼》T2I 基础图批量生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--shot", type=str, help="按名称模糊筛选")
    args = ap.parse_args()

    specs = [s for s in SPECS if not args.shot or args.shot in s["name"]]

    print("=" * 62)
    print(f" EP13《外骨骼》T2I 基础图  |  共 {len(specs)} 张  |  out: {OUTPUT_DIR}")
    print("=" * 62)
    for s in specs:
        tag = "🖼️ Image Edit(定妆照)" if s["mode"] == "image_edit" else "📝 Z-Image-Turbo"
        print(f"  - {s['name']}  →  {s['out']}  [{tag}] seed={s['seed']}")
    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ok_map = {}
    ok_n = 0
    for i, s in enumerate(specs, 1):
        print(f"\n[{i}/{len(specs)}] {s['name']}")
        try:
            ok = run_one(s, OUTPUT_DIR)
            ok_map[s["out"]] = ok
            if ok:
                ok_n += 1
        except Exception as e:
            ok_map[s["out"]] = False
            print(f"    ❌ {e}")
        time.sleep(1)
    write_manifest(ok_map)
    print(f"\n{'=' * 62}\n 完成: {ok_n}/{len(specs)}  输出: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()


