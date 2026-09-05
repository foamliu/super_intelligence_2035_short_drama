#!/usr/bin/env python3
"""
第13集(外骨骼) & 第14集(副作用) I2V 视频批量生成脚本

解析 I2V_Prompts.md 中的镜头规格，调用 ComfyUI API 生成视频。
仅支持 Wan 2.2 I2V workflow（高质量人物表演，640×640 @ 16fps）。

输入图像来源: 先用 Z-Image-Turbo 文生图生成 T2I 静态图。

用法:
  python scripts/generate_ep13_14_videos.py --dry-run          # 仅打印计划
  python scripts/generate_ep13_14_videos.py --episode 14       # 生成第14集
  python scripts/generate_ep13_14_videos.py --episode 13 --shot 01  # 仅某个镜头
  python scripts/generate_ep13_14_videos.py --episode 13 --priority p0  # 按优先级筛选
"""

import json
import os
import sys
import time
import uuid
import re
import urllib.request
import urllib.error
import argparse
import shutil
from pathlib import Path
from typing import Optional

# ── 配置 ──────────────────────────────────────────────
COMFYUI_URL = "http://127.0.0.1:8188"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ROOT = PROJECT_ROOT / "OUTPUT"
SHOT_SPECS_DIR = PROJECT_ROOT / "ASSETS" / "SHOT_SPECS"

# Workflow 模板路径
WAN_I2V_WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "Wan 2.2 图生视频.json"
T2I_WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "Z-Image-Turbo 文生图.json"

EPISODE_MAP = {
    "13": {
        "name": "13_外骨骼",
        "i2v_spec": "13_外骨骼_I2V_Prompts.md",
        "t2i_spec": "13_外骨骼_T2I_Prompts.md",
    },
    "14": {
        "name": "14_副作用",
        "i2v_spec": "14_副作用_I2V_Prompts.md",
        "t2i_spec": "14_副作用_T2I_Prompts.md",
    },
}

# ComfyUI 根目录统一探测
_COMFYUI_ROOT = None


def _detect_comfyui_root() -> Path:
    """找到实际运行 ComfyUI 服务的根目录。"""
    global _COMFYUI_ROOT
    if _COMFYUI_ROOT:
        return _COMFYUI_ROOT

    candidates = [
        Path("E:/ComfyUI"),
        Path("E:/ComfyUI_windows_portable/ComfyUI"),
        Path("C:/Users/Administrator/AppData/Local/Programs/ComfyUI"),
        Path.home() / "ComfyUI",
    ]

    for c in candidates:
        if c.exists() and ((c / "main.py").exists() or (c / "nodes.py").exists()):
            _COMFYUI_ROOT = c
            return c

    for c in candidates:
        if c.exists():
            _COMFYUI_ROOT = c
            return c

    _COMFYUI_ROOT = Path("E:/ComfyUI")
    return _COMFYUI_ROOT


def get_comfyui_input_dir() -> Path:
    root = _detect_comfyui_root()
    inp = root / "input"
    inp.mkdir(parents=True, exist_ok=True)
    return inp


def get_comfyui_output_dir() -> Path:
    root = _detect_comfyui_root()
    out = root / "output"
    out.mkdir(parents=True, exist_ok=True)
    return out


def stage_image_for_i2v(image_path: str) -> str:
    """通过 ComfyUI /upload/image API 上传图像到 ComfyUI input 目录，返回文件名 (basename)。"""
    src = Path(image_path)
    if not src.exists():
        raise FileNotFoundError(f"输入图像不存在: {image_path}")
    fname = src.name

    try:
        ext_info = comfyui_request("/object_info", method="GET")
        load_img = ext_info.get("LoadImage", {})
        known_files = load_img.get("input", {}).get("required", {}).get("image", [[], {}])[0]
        if fname in known_files:
            print(f"    已在 ComfyUI input (已注册): {fname}")
            dst = get_comfyui_input_dir() / fname
            if not dst.exists():
                shutil.copy2(src, dst)
            return fname
    except Exception:
        pass

    with open(src, "rb") as fh:
        img_data = fh.read()

    boundary = "----WebKitFormBoundaryEP13I2VUpload"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{fname}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8")
    body += img_data
    body += f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        f"{COMFYUI_URL}/upload/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            print(f"    已上传到 ComfyUI input: {fname}")
            return fname
    except urllib.error.URLError as e:
        dst = get_comfyui_input_dir() / fname
        if dst.exists():
            print(f"    ⚠ 上传失败 ({e})，回退使用已有文件: {fname}")
            return fname
        raise


# ── API 工具 ──────────────────────────────────────────
def comfyui_request(endpoint: str, data: Optional[dict] = None, method: str = "POST") -> dict:
    url = f"{COMFYUI_URL}{endpoint}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode("utf-8") if e.fp else ""
        except Exception:
            pass
        detail = err_body[:2000] if err_body else "(no body)"
        print(f"  [ERROR] ComfyUI HTTP {e.code}: {e.reason}")
        print(f"  [ERROR] Body: {detail}")
        raise
    except urllib.error.URLError as e:
        print(f"  [ERROR] ComfyUI 请求失败: {e}")
        raise


def queue_prompt(workflow: dict) -> str:
    payload = {"prompt": workflow, "client_id": f"ep_gen_{uuid.uuid4().hex[:8]}"}
    result = comfyui_request("/prompt", payload)
    pid = result.get("prompt_id", "")
    if not pid:
        raise RuntimeError(f"提交失败: {result}")
    return pid


def get_history(prompt_id: str) -> dict:
    return comfyui_request(f"/history/{prompt_id}", method="GET")


def wait_for_prompt(prompt_id: str, timeout: int = 1200) -> dict:
    start = time.time()
    while time.time() - start < timeout:
        history = get_history(prompt_id)
        if prompt_id in history:
            return history[prompt_id]
        time.sleep(3)
    raise TimeoutError(f"Prompt {prompt_id} 超时 ({timeout}s)")


def find_output_files(history_entry: dict) -> list[dict]:
    outputs = []
    for node_id, nd in history_entry.get("outputs", {}).items():
        for img in nd.get("images", []):
            outputs.append({"filename": img["filename"], "subfolder": img.get("subfolder", ""), "type": "image"})
        for vid in nd.get("videos", []):
            outputs.append({"filename": vid["filename"], "subfolder": vid.get("subfolder", ""), "type": "video"})
    return outputs


# ── Workflow 构建 ─────────────────────────────────────
def load_workflow(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_wan_i2v_workflow(
    image_path: str,
    prompt: str,
    neg_prompt: str = "",
    seed: int = 42,
    duration: int = 10,
    fps: int = 16,
    width: int = 640,
    height: int = 640,
) -> dict:
    """构建 Wan 2.2 I2V workflow

    Wan 2.2 节点结构 (workflows/Wan 2.2 图生视频.json):
    - 121: LoadImage -> image
    - 120:93: CLIPTextEncode (Positive Prompt) -> text
    - 120:89: CLIPTextEncode (Negative Prompt) -> text
    - 120:98: WanImageToVideo -> width, height, length, start_image
    - 120:86: KSamplerAdvanced (第一段) -> noise_seed
    - 120:85: KSamplerAdvanced (第二段, seed=0, add_noise=disable)
    - 120:117: CreateVideo -> fps
    - 122: SaveVideo
    length = fps * duration + 1 (最后 1 帧为结束帧)
    """
    if not WAN_I2V_WORKFLOW_PATH.exists():
        raise FileNotFoundError(f"Wan 2.2 workflow 不存在: {WAN_I2V_WORKFLOW_PATH}")

    wf = load_workflow(WAN_I2V_WORKFLOW_PATH)
    length = fps * duration + 1

    for node_id, node in wf.items():
        ct = node.get("class_type", "")
        title = node.get("_meta", {}).get("title", "")

        if ct == "LoadImage":
            node["inputs"]["image"] = image_path

        if ct == "CLIPTextEncode" and "positive" in title.lower():
            node["inputs"]["text"] = prompt

        if ct == "CLIPTextEncode" and "negative" in title.lower():
            node["inputs"]["text"] = neg_prompt

        if ct == "WanImageToVideo":
            node["inputs"]["width"] = width
            node["inputs"]["height"] = height
            node["inputs"]["length"] = length

        if ct == "KSamplerAdvanced" and node.get("inputs", {}).get("add_noise") == "enable":
            node["inputs"]["noise_seed"] = seed

        if ct == "CreateVideo":
            node["inputs"]["fps"] = fps

    return wf


# ── Prompt 解析 ───────────────────────────────────────
def clean_input_image(raw: str) -> str:
    """清理 input_image 字段，提取纯文件名"""
    raw = raw.strip().strip("`'\" ")
    if not raw:
        return ""
    if raw.startswith("无") or raw.startswith("None") or raw.startswith("none"):
        return ""
    raw = re.sub(r'[（(][^)）]*[)）]', '', raw)
    raw = re.sub(r'，?\s*可选参考.*', '', raw)
    return raw.strip().strip("`'\" ")


def parse_i2v_spec(spec_path: Path) -> list[dict]:
    """解析 I2V_Prompts.md，提取每个镜头的完整参数

    所有镜头统一使用 Wan 2.2 I2V workflow。
    原本标记为 T2V 且无输入图像的镜头，会尝试从 '可选参考' 中提取参考图。
    """
    if not spec_path.exists():
        print(f"  [WARNING] 文件不存在: {spec_path}")
        return []

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    shots = []
    shot_pattern = re.compile(
        r'##\s*镜头(\d+)[：:](.*?)\n(.*?)(?=\n##\s*镜头|\n---\s*\n##\s*制作优先级|\Z)',
        re.DOTALL,
    )

    for match in shot_pattern.finditer(content):
        shot_id = match.group(1).strip()
        shot_name = match.group(2).strip()
        block = match.group(3)

        shot = {"shot_id": shot_id, "shot_name": shot_name}

        table_pattern = re.compile(
            r'\|\s*\*?\*?(.*?)\*?\*?\s*\|\s*(.*?)\s*\|',
        )

        rows = table_pattern.findall(block)
        row_map = {}
        for key, val in rows:
            key_clean = re.sub(r'\*+', '', key).strip().lower()
            if 'workflow' in key_clean or '使用' in key_clean:
                row_map['workflow'] = val.strip()
            elif '输入图像' in key_clean or '输入图' in key_clean:
                row_map['input_image'] = val.strip().strip('`')
            elif '时长' in key_clean or '视频时长' in key_clean:
                row_map['duration'] = val.strip()
            elif 'prompt' in key_clean and '负面' not in key_clean and 'negative' not in key_clean:
                row_map['prompt'] = val.strip()
            elif '负面' in key_clean or 'negative' in key_clean:
                row_map['neg_prompt'] = val.strip()
            elif 'seed' in key_clean:
                row_map['seed'] = val.strip()
            elif '输出文件' in key_clean:
                row_map['output_file'] = val.strip().strip('`')

        shot["input_image"] = clean_input_image(row_map.get("input_image", ""))
        shot["_raw_input_image"] = row_map.get("input_image", "")
        duration_str = row_map.get("duration", "10 秒")
        duration_match = re.search(r'(\d+)', duration_str)
        shot["duration"] = int(duration_match.group(1)) if duration_match else 10
        shot["prompt"] = row_map.get("prompt", "")
        shot["neg_prompt"] = row_map.get("neg_prompt", "")
        seed_str = row_map.get("seed", "42")
        seed_match = re.search(r'(\d+)', seed_str)
        shot["seed"] = int(seed_match.group(1)) if seed_match else 42
        shot["output_file"] = row_map.get("output_file", f"EP_shot_{shot_id}.mp4")

        # 所有镜头统一走 Wan 2.2 I2V
        shot["width"], shot["height"] = 640, 640
        shot["fps"] = 16

        # T2V 或原本无输入图的镜头，尝试从 '可选参考' 提取参考图
        if not shot["input_image"] and shot["_raw_input_image"]:
            ref_match = re.search(r'`([^`]+\.png)`', shot["_raw_input_image"])
            if ref_match:
                shot["input_image"] = ref_match.group(1)
                print(f"  [INFO] SHOT-{shot_id}: 无直接输入图，使用可选参考图 {shot['input_image']}")

        if not shot["prompt"]:
            print(f"  [WARNING] 镜头{shot_id} 无 Prompt，跳过")
            continue

        shots.append(shot)

    return shots


# ── 主流程 ────────────────────────────────────────────
def find_input_image(shot: dict, episode_dir: Path) -> Optional[str]:
    """为 I2V shot 查找输入图像。返回绝对路径，或 None。"""
    img_name = shot.get("input_image", "")
    if not img_name:
        return None

    img_name = img_name.strip("`'\" ")

    candidates = [
        episode_dir / "frames" / img_name,
        Path(img_name) if Path(img_name).is_absolute() else None,
        get_comfyui_output_dir() / img_name,
    ]

    for c in candidates:
        if c and c.exists():
            return str(c.resolve())

    frames_dir = episode_dir / "frames"
    if frames_dir.exists():
        for f in frames_dir.iterdir():
            if img_name.lower() in f.name.lower():
                return str(f.resolve())

    return None


def log_shot_payload(shot: dict, output_dir: Path) -> None:
    """将镜头的完整 prompt/参数写入日志文件，确保可追溯。"""
    logs_dir = output_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"SHOT-{shot['shot_id']}_params.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "shot_id": shot["shot_id"],
            "shot_name": shot["shot_name"],
            "prompt": shot["prompt"],
            "neg_prompt": shot["neg_prompt"],
            "seed": shot["seed"],
            "duration": shot["duration"],
            "fps": shot["fps"],
            "width": shot["width"],
            "height": shot["height"],
            "input_image": shot.get("input_image", ""),
            "output_file": shot.get("output_file", ""),
            "workflow": "Wan 2.2 I2V",
        }, f, ensure_ascii=False, indent=2)
    print(f"    参数日志已写入: {log_path}")


def run_i2v_shot(shot: dict, episode: str, output_dir: Path) -> bool:
    """执行单个 I2V 镜头的生成（统一走 Wan 2.2 I2V）"""
    shot_id = shot["shot_id"]
    print(f"\n  [I2V] SHOT-{shot_id}: {shot['shot_name']}")
    print(f"    时长: {shot['duration']}s | Seed: {shot['seed']} | FPS: {shot['fps']}")
    print(f"    Prompt: {shot['prompt'][:200]}...")

    # 记录完整 payload 日志
    log_shot_payload(shot, output_dir)

    image_path = find_input_image(shot, output_dir)
    if not image_path:
        print(f"    [ERROR] 找不到输入图像 '{shot.get('input_image', 'N/A')}'")
        print(f"    请先生成 T2I 静态图 -> OUTPUT/{EPISODE_MAP[episode]['name']}/frames/")
        return False

    print(f"    输入图: {image_path}")

    image_fname = stage_image_for_i2v(image_path)

    wf = build_wan_i2v_workflow(
        image_path=image_fname,
        prompt=shot["prompt"],
        neg_prompt=shot["neg_prompt"],
        seed=shot["seed"],
        duration=shot["duration"],
        fps=shot["fps"],
    )

    try:
        pid = queue_prompt(wf)
        print(f"    已提交 (prompt_id={pid})，等待生成...")
        history = wait_for_prompt(pid, timeout=1200)
        outputs = find_output_files(history)

        if outputs:
            videos_dir = output_dir / "videos"
            videos_dir.mkdir(parents=True, exist_ok=True)

            out = outputs[0]
            src = get_comfyui_output_dir() / out.get("subfolder", "") / out["filename"]
            dst_name = f"EP{episode}_SHOT-{shot_id}_{out['filename']}"
            dst = videos_dir / dst_name
            if src.exists():
                shutil.copy2(src, dst)
                print(f"    ✅ 已保存: {dst}")
            else:
                print(f"    ⚠️ 源文件不在: {src}")
                print(f"    视频可能在 ComfyUI output 目录: {get_comfyui_output_dir() / out.get('subfolder', '')}")
            return True
        else:
            print(f"    [ERROR] 无输出文件")
            return False

    except Exception as e:
        print(f"    [ERROR] 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="批量生成第13/14集 I2V 视频 (Wan 2.2)")
    parser.add_argument("--episode", type=str, choices=["13", "14", "both"], default="both")
    parser.add_argument("--shot", type=str, help="仅生成指定镜头, e.g. 01")
    parser.add_argument("--dry-run", action="store_true", help="仅打印计划，不实际提交")
    parser.add_argument("--priority", type=str, choices=["p0", "p1", "p2", "p3", "p4", "all"], default="all",
                        help="按优先级筛选 (P0=核心表演, P1=主要人物, P2=氛围, P3=道具/UI)")
    args = parser.parse_args()

    # 优先级映射 (从 I2V specs 的制作优先级表格解析)
    PRIORITY_MAP = {
        "13": {
            "p0": ["01", "07", "08", "11"],
            "p1": ["06", "03", "10"],
            "p2": ["02", "04", "05"],
            "p3": ["09", "12"],
        },
        "14": {
            "p0": ["01", "06"],
            "p1": ["02", "04"],
            "p2": ["03", "05"],
            "p3": ["09", "10", "07"],
            "p4": ["08", "11"],
        },
    }

    episodes = ["13", "14"] if args.episode == "both" else [args.episode]

    for ep in episodes:
        ep_info = EPISODE_MAP[ep]
        spec_path = SHOT_SPECS_DIR / ep_info["i2v_spec"]
        output_dir = OUTPUT_ROOT / ep_info["name"]

        print(f"\n{'='*60}")
        print(f"Episode {ep}: {ep_info['name']}")
        print(f"规格文件: {spec_path}")
        print(f"输出目录: {output_dir}")
        print(f"{'='*60}")

        shots = parse_i2v_spec(spec_path)
        print(f"共解析 {len(shots)} 个镜头")

        # 筛选
        if args.shot:
            shots = [s for s in shots if s["shot_id"] == args.shot]
            print(f"筛选指定镜头后: {len(shots)} 个")
        elif args.priority != "all":
            allowed = PRIORITY_MAP.get(ep, {}).get(args.priority, [])
            shots = [s for s in shots if s["shot_id"] in allowed]
            print(f"按优先级 {args.priority.upper()} 筛选后: {len(shots)} 个")

        if not shots:
            print("无符合条件的镜头，跳过")
            continue

        for s in shots:
            print(f"\n  SHOT-{s['shot_id']}: {s['shot_name']}")
            print(f"    Workflow: Wan 2.2 I2V")
            print(f"    时长: {s['duration']}s | Seed: {s['seed']} | FPS: {s['fps']}")
            print(f"    Prompt: {s['prompt'][:200]}...")
            if s.get("input_image"):
                print(f"    输入图像: {s['input_image']}")

        if not args.dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)
            success = 0
            for s in shots:
                ok = run_i2v_shot(s, ep, output_dir)
                if ok:
                    success += 1
                time.sleep(1)

            print(f"\n  --- Episode {ep} 完成: {success}/{len(shots)} ---")

    print(f"\n{'='*60}")
    print("全部完成!")
    print(f"输出目录: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()