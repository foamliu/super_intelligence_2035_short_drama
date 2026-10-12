#!/usr/bin/env python3
"""
第18集《暖阳》T2I 静态图批量生成脚本（固化 · S3 放量第 1 章）。

作用：生成第 18 集「定妆照 + 场景图 + 道具 + 头像」共 13 张基础图，
      作为后续 I2V（Minimax H3）的分镜帧输入。与 MCP 工具口径一致：
  - 老周角色镜头（含人物）→ LongCat Image Edit（输入=老周 01_正面定妆，保角色一致）
  - 非人物镜头（小晴头像 / 城市夜景 / 道具）→ Z-Image-Turbo 文生图

用法:
  python scripts/generate_ep18_t2i.py --dry-run      # 仅打印计划
  python scripts/generate_ep18_t2i.py --shot 老周-02  # 仅生成某张
  python scripts/generate_ep18_t2i.py                 # 全部 13 张

产出（均已按此规格生成于 2026-10-11 S3 首轮，见 OUTPUT/18_暖阳/frames/manifest.json）：
  ASSETS/CHARACTERS/07_老周/02_半侧面沉思.png  03_落泪.png（角色锚点）
  OUTPUT/18_暖阳/frames/18_*.png（13 张）
"""
import json
import time
import uuid
import re
import shutil
import urllib.request
import urllib.error
import urllib.parse
import argparse
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
COMFYUI_URL = "http://127.0.0.1:8188"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "OUTPUT" / "18_暖阳" / "frames"
ZIMAGE_WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "Z-Image-Turbo 文生图.json"
IMAGE_EDIT_WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "Image Edit (LongCat Image Edit).json"

LAOZHOU_REF = PROJECT_ROOT / "ASSETS" / "CHARACTERS" / "07_老周" / "01_正面定妆.png"
LAOZHOU_REF_TARGET = "ref_laozhou_18.png"

NEG_LAOZHOU = (
    "ugly, deformed, bad anatomy, disfigured, poorly drawn face, mutation, extra limb, "
    "extra fingers, fused fingers, too many fingers, blurry, watermark, text, logo, "
    "oversaturated, plastic skin, heavy makeup, beauty filter, anime, cartoon, illustration, "
    "3D render, smiling, grinning, cheerful, confident, energetic, handsome, model-like, "
    "sharp suit, luxury, executive, young, baby face, clear skin, thick hair, muscular, "
    "bright natural sunlight, warm atmosphere, happy vibe, Western oil painting, "
    "Baroque lighting, CGI look, doll-like"
)
NEG_XIAOQING = (
    "sexy, heavy makeup, glamour, studio portrait, fashion model, unrealistic skin, "
    "plastic surgery, mature, older than 20, western face"
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


# ── 13 张基础图规格 ────────────────────────────────────
# image_edit 的 megapixels=0.92 → 实际输出约 1312×736（16:9，LongCat 按 32 倍数取整）
SPECS = [
    # — 老周定妆（image_edit，输入 01 正面定妆）—
    {
        "name": "老周-02_半侧面沉思", "mode": "image_edit", "megapixels": 0.92, "seed": 43,
        "out": "18_laozhou_02_profile_thinking.png",
        "prompt": (
            "Same 45-year-old Chinese man with round gaunt face, tired eyes with dark circles, "
            "now in 45-degree half profile, eyes looking down to the left toward a smartphone, "
            "cold white phone screen light illuminating the lower half of his face, lips slightly "
            "parted as if about to speak, rough fingers with old scars resting on a steering wheel, "
            "dark blue car interior reading light from upper left, half face in light half in shadow, "
            "semi-realistic ink wash style, photorealistic base"
        ),
    },
    {
        "name": "老周-03_落泪", "mode": "image_edit", "megapixels": 0.92, "seed": 44,
        "out": "18_laozhou_03_tears.png",
        "prompt": (
            "Same 45-year-old Chinese man with round gaunt face, close-up shot, reddened eyes, "
            "a single tear trail sliding from right eye corner down to jaw, lips trembling slightly, "
            "silent weeping not sobbing, cold white phone screen light reflecting faintly on the "
            "tear trail, dark blue car interior, twenty years of suppressed emotion finally released, "
            "semi-realistic ink wash style, photorealistic base"
        ),
    },
    # — 出租屋（image_edit，老周在画面中）—
    {
        "name": "出租屋-01_床上夜景", "mode": "image_edit", "megapixels": 0.92, "seed": 200,
        "out": "18_room_01_bed_night.png",
        "prompt": (
            "Same 45-year-old Chinese man now lying on a bed in a small dim rental apartment at "
            "night, holding a smartphone above his face, cold white screen light illuminating his "
            "face and pupils, half-lit half-shadow, simple old but tidy furniture, simple curtains, "
            "distant city lights through window, dark grey and black dominant with cold white screen "
            "light accent, loneliness, semi-realistic ink wash style, photorealistic base"
        ),
    },
    {
        "name": "出租屋-02_床边坐姿", "mode": "image_edit", "megapixels": 0.92, "seed": 201,
        "out": "18_room_02_sitting_bedside.png",
        "prompt": (
            "Same 45-year-old Chinese man now sitting on the edge of a bed in a small dim rental "
            "apartment at night, body slightly leaning forward, smartphone held in hands resting on "
            "lap with screen glowing, slumped shoulders showing relief and exhaustion of finally "
            "speaking, nightstand photo frame visible in soft focus, window showing deep night, "
            "semi-realistic ink wash style, photorealistic base"
        ),
    },
    # — 网约车内（image_edit，老周在驾驶座）—
    {
        "name": "车内-01_夜晚驾驶位", "mode": "image_edit", "megapixels": 0.92, "seed": 300,
        "out": "18_car_01_night_driving.png",
        "prompt": (
            "Same 45-year-old Chinese man sitting in a ride-hailing car driver seat at night, "
            "phone mounted on dashboard holder, city traffic outside window with red taillights and "
            "warm yellow streetlights as blurred flowing light trails, dark blue interior reading "
            "light from overhead, worn leather steering wheel, rough right hand with old scars "
            "resting on steering wheel, semi-realistic ink wash style, photorealistic base"
        ),
    },
    {
        "name": "车内-02_凌晨路边停靠", "mode": "image_edit", "megapixels": 0.92, "seed": 301,
        "out": "18_car_02_parked_midnight.png",
        "prompt": (
            "Same 45-year-old Chinese man in a car parked on a city roadside at 2am, empty street "
            "with occasional distant car, warm yellow streetlight slanting in from left window across "
            "his face, interior reading light on, looking down at phone, cold white screen versus warm "
            "yellow streetlight contrast on his face, quiet but something feels wrong, semi-realistic "
            "ink wash style, photorealistic base"
        ),
    },
    {
        "name": "车内-03_实验期白天", "mode": "image_edit", "megapixels": 0.92, "seed": 302,
        "out": "18_car_03_daytime_forum.png",
        "prompt": (
            "Same 45-year-old Chinese man in a car during daytime, low-saturation cool grey tone, "
            "overcast scattered light through window, less dramatic than night, holding phone with "
            "faint forum page on screen, expression of beginning doubt but not yet sure, "
            "semi-realistic ink wash style, photorealistic base"
        ),
    },
    {
        "name": "车内-04_最终选择", "mode": "image_edit", "megapixels": 0.92, "seed": 303,
        "out": "18_car_04_final_choice.png",
        "prompt": (
            "Same 45-year-old Chinese man in a car at dawn, phone screen showing purchase "
            "confirmation page payment successful, finger just lifted from screen, expression complex "
            "not angry not sad but resigned acceptance, city lights distant, dark interior with only "
            "screen light and distant streetlights, hand gripping steering wheel then slowly relaxing, "
            "semi-realistic ink wash style, photorealistic base"
        ),
    },
    # — 非人物（zimage T2I）—
    {
        "name": "小晴-头像定妆", "mode": "zimage", "width": 1024, "height": 1024, "seed": 100,
        "out": "18_xiaoqing_avatar.png", "neg": NEG_XIAOQING,
        "prompt": (
            "Portrait headshot of a Chinese girl, 18-19 years old, front-facing head slightly tilted, "
            "smiling gently with two shallow dimples, small but bright attentive eyes, black "
            "medium-length natural hair unstyled, plain light-grey background, soft window-side "
            "natural light, warm caring expression, semi-realistic ink wash style with photorealistic "
            "base, clean composition"
        ),
    },
    {
        "name": "城市-01_车窗外流动夜景", "mode": "zimage", "width": 1280, "height": 720, "seed": 400,
        "out": "18_city_01_driving_night_view.png", "neg": "",
        "prompt": (
            "View from inside a moving car through the window at night, city street lights passing "
            "one by one, red taillights forming flowing light trails, dense distant building lights, "
            "slight motion blur, warm yellow streetlights with red taillights and dark blue night sky, "
            "semi-realistic ink wash style, photorealistic base"
        ),
    },
    {
        "name": "城市-02_凌晨空荡街道远景", "mode": "zimage", "width": 1280, "height": 720, "seed": 401,
        "out": "18_city_02_empty_street_dawn.png", "neg": "",
        "prompt": (
            "Wide shot of empty city street at dawn, a single car with taillights driving into the "
            "distance, streetlights in a line extending far, dark blue and warm yellow streetlight "
            "tones, lonely but calm atmosphere, semi-realistic ink wash style, photorealistic base"
        ),
    },
    {
        "name": "道具-01_床头柜相框", "mode": "zimage", "width": 1024, "height": 1024, "seed": 500,
        "out": "18_prop_01_photo_frame.png", "neg": "",
        "prompt": (
            "An old wooden photo frame with worn corners, containing a photo of an 8-year-old "
            "Chinese girl with two braids, missing a front tooth, laughing carefree, photo slightly "
            "faded, on a nightstand beside an old alarm clock, dim warm rental room light, "
            "semi-realistic ink wash style, photorealistic base"
        ),
    },
    {
        "name": "道具-02_护膝包装盒", "mode": "zimage", "width": 1024, "height": 1024, "seed": 501,
        "out": "18_prop_02_knee_brace_box.png", "neg": "",
        "prompt": (
            "A dark grey knee brace packaging box, size L, simple design like typical sports "
            "protective gear packaging on an e-commerce platform, on a table in a rental room, "
            "smartphone beside it with screen just dimmed, dim rental room light, semi-realistic "
            "ink wash style, photorealistic base"
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
    payload = {"prompt": workflow, "client_id": f"ep18_{uuid.uuid4().hex[:8]}"}
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
        if not LAOZHOU_REF.exists():
            print(f"  [ERROR] 缺老周定妆照: {LAOZHOU_REF}")
            return False
        ref = upload_ref_to_comfyui(LAOZHOU_REF, LAOZHOU_REF_TARGET)
        wf = build_image_edit(spec["prompt"], NEG_LAOZHOU, ref,
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


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》T2I 基础图批量生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--shot", type=str, help="按名称模糊筛选")
    args = ap.parse_args()

    specs = [s for s in SPECS if not args.shot or args.shot in s["name"]]

    print("=" * 62)
    print(f" EP18《暖阳》T2I 基础图  |  共 {len(specs)} 张  |  out: {OUTPUT_DIR}")
    print("=" * 62)
    for s in specs:
        tag = "🖼️ Image Edit(老周01)" if s["mode"] == "image_edit" else "📝 Z-Image-Turbo"
        print(f"  - {s['name']}  →  {s['out']}  [{tag}] seed={s['seed']}")
    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ok_n = 0
    for i, s in enumerate(specs, 1):
        print(f"\n[{i}/{len(specs)}] {s['name']}")
        try:
            if run_one(s, OUTPUT_DIR):
                ok_n += 1
        except Exception as e:
            print(f"    ❌ {e}")
        time.sleep(1)
    print(f"\n{'=' * 62}\n 完成: {ok_n}/{len(specs)}  输出: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

