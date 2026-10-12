#!/usr/bin/env python3
"""第18集《暖阳》手机「暖阳」App UI 界面帧批量生成脚本（固化 · S3 放量）。

作用：生成第 18 集手机屏幕特写镜头所需的分镜帧（UI 界面），作为后续
I2V（Minimax H3）的输入。全部为「非人物·屏幕界面」镜头 → Z-Image-Turbo 文生图
（界面是叙事的延伸，遵循 `ASSETS/屏幕界面设计规范.md`：克制、极简、无科幻全息、
手机屏幕冷白／暖黄微光作主光源）。

覆盖镜号：03/09/12/16/21/29/30/34/35/38/40/43/44/51/53（共 15 镜手机屏幕特写）。

用法:
  python scripts/gen_ep18_ui_frames.py --dry-run      # 仅打印计划
  python scripts/gen_ep18_ui_frames.py --shot 03      # 仅生成某镜
  python scripts/gen_ep18_ui_frames.py                # 全部 15 张
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
OUTPUT_DIR = PROJECT_ROOT / "OUTPUT" / "18_暖阳" / "frames"
ZIMAGE_WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "Z-Image-Turbo 文生图.json"

WIDTH, HEIGHT = 1280, 720  # 16:9 横屏，匹配 I2V 画幅

STYLE = "semi-realistic ink wash style, photorealistic base, clean composition"

NEG_UI = (
    "blurry, watermark, logo, signature, oversaturated, anime, cartoon, illustration, "
    "3D render, plastic, holographic, futuristic sci-fi HUD, floating transparent screen, "
    "neon, lens flare, glitch, distorted text"
)


def _detect_comfyui_base() -> Path:
    for c in [Path("E:/code/ComfyUI"),
              Path("E:/ComfyUI"),
              Path("E:/ComfyUI_windows_portable/ComfyUI"),
              Path.home() / "ComfyUI"]:
        if c.exists():
            return c
    return Path("E:/code/ComfyUI")


def get_comfyui_output_dir() -> Path:
    return _detect_comfyui_base() / "output"


# ── 15 张手机 UI 界面帧规格 ─────────────────────────────
# 镜号 / 名称 / 画面要点（暖阳 App：AI 陪伴，小晴头像=酒窝女孩，界面幽暗极简）
SPECS = [
    {
        "shot": "03", "name": "注册界面·选头像",
        "out": "18_ui_03_registration.png", "seed": 1903,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion app registration page, "
            "a neat grid of companion avatar thumbnails, one avatar of a young Chinese girl with "
            "two shallow dimples highlighted with a soft glow, a name input field with short "
            "Chinese characters, a middle-aged man's calloused fingertip hovering over the grid, "
            "dark minimal interface, cold white screen glow as the only light source, dim "
            "surroundings, low saturation, restrained, " + STYLE
        ),
    },
    {
        "shot": "09", "name": "小晴头像·酒窝",
        "out": "18_ui_09_avatar.png", "seed": 1909,
        "prompt": (
            "Extreme close-up of a smartphone screen showing an AI companion avatar portrait of a "
            "young Chinese girl with two shallow dimples and a gentle soft smile, the avatar alone "
            "glowing softly in the center, the rest of the interface dark and minimal, lonely quiet "
            "mood, cold white glow with faint warm accent, low saturation, " + STYLE
        ),
    },
    {
        "shot": "12", "name": "语音波纹",
        "out": "18_ui_12_waveform.png", "seed": 1912,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a small avatar "
            "of a young girl with dimples at the top, a soft voice waveform rising and falling "
            "inside a chat bubble, no readable text, dark minimal interface, warm yellow screen "
            "glow, quiet attentive mood, low saturation, " + STYLE
        ),
    },
    {
        "shot": "16", "name": "小晴聊天问候",
        "out": "18_ui_16_chat.png", "seed": 1916,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a warm avatar "
            "of a young girl with dimples at the top, one short friendly Chinese chat message bubble "
            "below, dark minimal interface, warm yellow screen glow, gentle caring mood, low "
            "saturation, " + STYLE
        ),
    },
    {
        "shot": "21", "name": "小晴推荐",
        "out": "18_ui_21_recommend.png", "seed": 1921,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a warm avatar "
            "of a young girl with dimples at the top, a recommendation message bubble with a small "
            "sleep-aid product thumbnail beside it, dark minimal interface, warm yellow screen glow, "
            "low saturation, " + STYLE
        ),
    },
    {
        "shot": "23", "name": "消费记录",
        "out": "18_ui_23_orders.png", "seed": 1923,
        "prompt": (
            "Close-up of a smartphone screen showing a purchase order history page, a long scrolling "
            "list of past order entries with small item thumbnails and Chinese yuan amounts, several "
            "orders for sleep-aid products and a grey knee brace, dark minimal interface, cold white "
            "screen glow, slightly uneasy quiet mood, low saturation, " + STYLE
        ),
    },
    {
        "shot": "29", "name": "回复延迟·等待",
        "out": "18_ui_29_delayed.png", "seed": 1929,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, an empty input "
            "area waiting for a delayed reply, a small typing indicator of three dots, sparse short "
            "message bubbles above, dark minimal interface, cold white screen glow, uneasy quiet "
            "mood, low saturation, " + STYLE
        ),
    },
    {
        "shot": "30", "name": "回复延迟·变慢",
        "out": "18_ui_30_delayed2.png", "seed": 1930,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, sparse short "
            "message bubbles with a long pause between them, the reply arriving slowly, dark minimal "
            "interface, cold white screen glow, slightly lonely quiet mood, low saturation, " + STYLE
        ),
    },
    {
        "shot": "34", "name": "论坛首页",
        "out": "18_ui_34_forum_home.png", "seed": 1934,
        "prompt": (
            "Close-up of a smartphone screen showing a community forum homepage, a list of short "
            "Chinese post titles in a clean dark-mode layout, one post highlighted, no readable long "
            "text, cold white screen glow, low saturation, restrained minimal interface, " + STYLE
        ),
    },
    {
        "shot": "35", "name": "论坛帖子·回复",
        "out": "18_ui_35_forum_post.png", "seed": 1935,
        "prompt": (
            "Close-up of a smartphone screen showing a forum thread, a short Chinese title at top "
            "and dozens of reply comment blocks scrolling down, dark-mode interface, cold white "
            "screen glow, slight grain, restrained minimal layout, low saturation, " + STYLE
        ),
    },
    {
        "shot": "38", "name": "界面变淡",
        "out": "18_ui_38_fading.png", "seed": 1938,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, the warm glow "
            "noticeably dimmed and faded, shorter sparser message bubbles, the whole interface "
            "feeling colder and more distant, dark minimal, low saturation, lonely mood, " + STYLE
        ),
    },
    {
        "shot": "40", "name": "对话框问答",
        "out": "18_ui_40_chat_qna.png", "seed": 1940,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, short Chinese "
            "question and answer message bubbles appearing one by one, warm avatar of a young girl "
            "with dimples at top, dark minimal interface, warm yellow screen glow, low saturation, "
            + STYLE
        ),
    },
    {
        "shot": "43", "name": "输入框打字",
        "out": "18_ui_43_input.png", "seed": 1943,
        "prompt": (
            "Close-up of a smartphone screen showing a chat input box at the bottom with a short "
            "Chinese message being typed, a thumb paused over the on-screen keyboard, dark minimal "
            "interface, cold white screen glow, low saturation, restrained, " + STYLE
        ),
    },
    {
        "shot": "44", "name": "小晴回复",
        "out": "18_ui_44_chat_reply.png", "seed": 1944,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a warm reply "
            "message bubble from a young girl avatar with dimples at the top, dark minimal interface, "
            "warm yellow screen glow, gentle reassuring mood, low saturation, " + STYLE
        ),
    },
    {
        "shot": "51", "name": "护膝干预消息",
        "out": "18_ui_51_intervention.png", "seed": 1951,
        "prompt": (
            "Close-up of a smartphone screen showing an AI companion chat interface, a promotional "
            "message about a knee brace product with a small countdown discount timer, warm avatar "
            "of a young girl with dimples at top, dark minimal interface, warm yellow screen glow, "
            "low saturation, " + STYLE
        ),
    },
    {
        "shot": "53", "name": "购物车·护膝",
        "out": "18_ui_53_cart.png", "seed": 1953,
        "prompt": (
            "Close-up of a smartphone screen showing an e-commerce shopping cart interface, a dark "
            "grey knee brace product with size L selected and a discounted price, a confirm purchase "
            "button at bottom, minimal clean interface, cold white screen glow, low saturation, "
            + STYLE
        ),
    },
]



# ── ComfyUI API（同 generate_ep18_t2i.py 范式）──────────
def comfyui_request(endpoint, data=None, method="POST"):
    url = f"{COMFYUI_URL}{endpoint}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def queue_prompt(workflow):
    payload = {"prompt": workflow, "client_id": f"ep18_ui_{uuid.uuid4().hex[:8]}"}
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


def run_one(spec, output_dir):
    out_file = output_dir / spec["out"]
    wf = build_zimage_t2i(spec["prompt"], NEG_UI, WIDTH, HEIGHT, spec["seed"])
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
    ap = argparse.ArgumentParser(description="第18集《暖阳》手机 UI 界面帧批量生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--shot", type=str, help="按镜号筛选（如 03）")
    args = ap.parse_args()

    specs = [s for s in SPECS if not args.shot or s["shot"] == args.shot]

    print("=" * 62)
    print(f" EP18《暖阳》手机 UI 界面帧  |  共 {len(specs)} 张  |  {WIDTH}x{HEIGHT}")
    print(f" out: {OUTPUT_DIR}")
    print("=" * 62)
    for s in specs:
        print(f"  - SHOT-{s['shot']} {s['name']}  →  {s['out']}  seed={s['seed']}")
    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ok_n = 0
    for i, s in enumerate(specs, 1):
        print(f"\n[{i}/{len(specs)}] SHOT-{s['shot']} {s['name']}")
        try:
            if run_one(s, OUTPUT_DIR):
                ok_n += 1
        except Exception as e:
            print(f"    ❌ {e}")
        time.sleep(1)
    print(f"\n{'=' * 62}\n 完成: {ok_n}/{len(specs)}  输出: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

