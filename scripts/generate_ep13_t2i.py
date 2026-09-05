#!/usr/bin/env python3
"""
第13集《外骨骼》T2I 静态图批量生成脚本

解析 13_外骨骼_T2I_Prompts.md，调用 ComfyUI API 逐张生成。
- 莎拉角色镜头 → LongCat Image Edit（输入=莎拉主定妆照 + 场景Prompt，保持角色一致性）
- 非角色镜头 → Z-Image-Turbo 文生图

用法:
  python scripts/generate_ep13_t2i.py --dry-run          # 仅打印计划
  python scripts/generate_ep13_t2i.py --priority p0       # 仅 P0 (虚拟观众 ×2)
  python scripts/generate_ep13_t2i.py --shot 莎拉-01       # 仅某张图
  python scripts/generate_ep13_t2i.py                     # 全部 14 张
"""

import json
import os
import sys
import time
import uuid
import re
import urllib.request
import urllib.error
import urllib.parse
import argparse
import shutil
from pathlib import Path
from typing import Optional

# ── 配置 ──────────────────────────────────────────────
COMFYUI_URL = "http://127.0.0.1:8188"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "OUTPUT" / "13_外骨骼" / "frames"
T2I_SPEC_PATH = PROJECT_ROOT / "ASSETS" / "SHOT_SPECS" / "13_外骨骼_T2I_Prompts.md"
ZIMAGE_WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "Z-Image-Turbo 文生图.json"
IMAGE_EDIT_WORKFLOW_PATH = PROJECT_ROOT / "workflows" / "Image Edit (LongCat Image Edit).json"

# 角色定妆照映射 (镜头名前缀 → {ref_path, target_name})
# target_name 必须是 ASCII 文件名, 因为 ComfyUI LoadImage 不支持中文文件名
CHARACTER_REF_MAP = {
    "莎拉": {
        "ref_path": PROJECT_ROOT / "ASSETS" / "CHARACTERS" / "08_莎拉·赵" / "主定妆照.png",
        "target_name": "ref_sarah_zhao.png",
    },
}

# ComfyUI input 目录
_COMFYUI_INPUT_DIR = None


def _detect_comfyui_base() -> Path:
    """检测 ComfyUI 根目录"""
    candidates = [
        Path("E:/ComfyUI"),
        Path("E:/ComfyUI_windows_portable/ComfyUI"),
        Path.home() / "ComfyUI",
    ]
    for c in candidates:
        if c.exists():
            return c
    return Path("E:/ComfyUI")


def get_comfyui_input_dir() -> Path:
    """获取 ComfyUI input 目录 (用于上传参考图)"""
    global _COMFYUI_INPUT_DIR
    if _COMFYUI_INPUT_DIR:
        return _COMFYUI_INPUT_DIR
    _COMFYUI_INPUT_DIR = _detect_comfyui_base() / "input"
    _COMFYUI_INPUT_DIR.mkdir(parents=True, exist_ok=True)
    return _COMFYUI_INPUT_DIR


def get_comfyui_output_dir() -> Path:
    """获取 ComfyUI output 目录"""
    return _detect_comfyui_base() / "output"


# ── 优先级映射 ────────────────────────────────────────
PRIORITY_MAP = {
    "p0": ["虚拟观众-01_不存在的脸在笑", "虚拟观众-02_渲染vs真实·两张脸的对比"],
    "p1": ["地铁-01_早高峰·不在训练数据里的人",
           "工位-01_外骨骼工具主界面",
           "UI-01_外骨骼工具主界面（无人物）",
           "UI-02_双标注·小周"],
    "p2": ["莎拉-01_工位·解释外骨骼", "莎拉-02_地铁·观察者", "莎拉-03_吧台·0.52的散场",
           "师兄-01_咖啡杯·实验室传奇"],
    "p3": ["实验室-01_2017年深夜", "酒吧-01_散场后的吧台暗光",
           "道具-01_笔记本标签·不可迁移", "道具-02_微信对话·十秒沉默"],
}


# ── 角色路由 ──────────────────────────────────────────
def get_character_ref(img_name: str) -> Optional[dict]:
    """根据镜头名判断是否属于角色镜头，返回 CHARACTER_REF_MAP 中的 dict (含 ref_path, target_name)"""
    for prefix, info in CHARACTER_REF_MAP.items():
        if img_name.startswith(prefix):
            ref_path = info["ref_path"]
            if ref_path.exists():
                return info
            else:
                print(f"  [WARNING] 定妆照不存在: {ref_path}")
                return None
    return None


# ── ComfyUI API ───────────────────────────────────────
def comfyui_request(endpoint: str, data: Optional[dict] = None, method: str = "POST") -> dict:
    url = f"{COMFYUI_URL}{endpoint}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"  [ERROR] ComfyUI 请求失败: {e}")
        raise


def queue_prompt(workflow: dict) -> str:
    payload = {"prompt": workflow, "client_id": f"ep13_{uuid.uuid4().hex[:8]}"}
    result = comfyui_request("/prompt", payload)
    pid = result.get("prompt_id", "")
    if not pid:
        raise RuntimeError(f"提交失败: {result}")
    return pid


def get_history(prompt_id: str) -> dict:
    return comfyui_request(f"/history/{prompt_id}", method="GET")


def wait_for_prompt(prompt_id: str, timeout: int = 600) -> dict:
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
            outputs.append({
                "filename": img["filename"],
                "subfolder": img.get("subfolder", ""),
                "type": img.get("type", "output"),
            })
    return outputs


def download_output_image(out: dict, dst: Path) -> bool:
    fname = out["filename"]
    ftype = out.get("type", "output")
    subfolder = out.get("subfolder", "")

    # 方式1: HTTP /view API
    params = urllib.parse.urlencode({"filename": fname, "type": ftype})
    url = f"{COMFYUI_URL}/view?{params}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            if len(data) > 100:
                dst.write_bytes(data)
                return True
    except Exception as e:
        print(f"    [WARNING] HTTP /view 失败 ({fname}): {e}")

    # 方式2: 文件系统复制
    comfy_out = get_comfyui_output_dir()
    for src_path in [
        comfy_out / subfolder / fname,
        comfy_out / "temp" / fname,
        comfy_out / fname,
    ]:
        if src_path.exists():
            shutil.copy2(src_path, dst)
            return True

    print(f"    [WARNING] 源文件未找到: {fname} (type={ftype})")
    return False


# ── 参考图上传到 ComfyUI input ────────────────────────
def upload_ref_to_comfyui(ref_path: Path, target_name: str) -> str:
    """
    通过 ComfyUI /upload/image API 上传参考图，确保 LoadImage 可识别。
    如果已注册且文件大小相同则跳过。
    """
    import uuid as _uuid

    input_dir = get_comfyui_input_dir()
    dst = input_dir / target_name

    # 如果已注册且文件大小相同，跳过
    if dst.exists() and dst.stat().st_size == ref_path.stat().st_size:
        if _check_comfyui_has_image(target_name):
            print(f"    📎 参考图已注册: {target_name}")
            return target_name

    # 复制到 ComfyUI input 目录
    shutil.copy2(ref_path, dst)

    # 通过 /upload/image API 注册到 ComfyUI
    try:
        boundary = f"----{_uuid.uuid4().hex}"
        body = bytearray()

        for fn, fv in [("overwrite", "true"), ("type", "input")]:
            body.extend(f"--{boundary}\r\n".encode())
            body.extend(f'Content-Disposition: form-data; name="{fn}"\r\n\r\n'.encode())
            body.extend(f"{fv}\r\n".encode())

        file_data = dst.read_bytes()
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="image"; filename="{target_name}"\r\n'.encode())
        body.extend(f"Content-Type: image/png\r\n\r\n".encode())
        body.extend(file_data)
        body.extend(f"\r\n--{boundary}--\r\n".encode())

        url = f"{COMFYUI_URL}/upload/image"
        req = urllib.request.Request(url, data=bytes(body))
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        req.method = "POST"

        with urllib.request.urlopen(req, timeout=30) as resp:
            resp.read()

        print(f"    📤 已上传参考图: {ref_path.name} → ComfyUI ({target_name})")
    except Exception as e:
        print(f"    ⚠️  /upload/image API 失败: {e}")
        print(f"    ⚠️  文件已复制到 {dst}，可能需要刷新 ComfyUI 浏览器才能识别")

    return target_name


def _check_comfyui_has_image(filename: str) -> bool:
    """检查 ComfyUI LoadImage 是否已注册指定文件"""
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/object_info")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            images = data.get("LoadImage", {}).get("input", {}).get("required", {}).get("image", [[], {}])[0]
            return filename in images
    except Exception:
        return False


# ── Workflow 加载 ─────────────────────────────────────
def load_workflow(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Z-Image-Turbo T2I Workflow 构建 ──────────────────
def build_zimage_t2i(prompt: str, neg_prompt: str, width: int, height: int, seed: int) -> dict:
    wf = load_workflow(ZIMAGE_WORKFLOW_PATH)

    full_prompt = prompt.strip()
    if neg_prompt:
        full_prompt += f"\n\nDo NOT include: {neg_prompt}"

    for node_id, node in wf.items():
        if node.get("class_type") == "CLIPTextEncode":
            node["inputs"]["text"] = full_prompt

    for node_id, node in wf.items():
        if node.get("class_type") == "EmptySD3LatentImage":
            node["inputs"]["width"] = width
            node["inputs"]["height"] = height
            node["inputs"]["batch_size"] = 1

    for node_id, node in wf.items():
        if node.get("class_type") == "KSampler":
            node["inputs"]["seed"] = int(seed)

    return wf


# ── LongCat Image Edit Workflow 构建 ──────────────────
def build_image_edit(prompt: str, neg_prompt: str, ref_filename: str,
                     width: int, height: int, seed: int) -> dict:
    """
    构建 LongCat Image Edit workflow:
    - LoadImage → 加载参考图 (定妆照)
    - TextEncodeQwenImageEdit (正向) → 注入场景 Prompt
    - TextEncodeQwenImageEdit (负向) → 注入负面词
    - KSampler → 注入 seed
    - ImageScaleToTotalPixels → 注入分辨率
    """
    wf = load_workflow(IMAGE_EDIT_WORKFLOW_PATH)

    # 计算 megapixels (ImageScaleToTotalPixels 用的单位)
    megapixels = max(1.0, (width * height) / 1_000_000)

    # LoadImage → 注入参考图文件名
    for node_id, node in wf.items():
        if node.get("class_type") == "LoadImage":
            node["inputs"]["image"] = ref_filename

    # ImageScaleToTotalPixels → 注入分辨率
    for node_id, node in wf.items():
        if node.get("class_type") == "ImageScaleToTotalPixels":
            node["inputs"]["megapixels"] = megapixels

    # TextEncodeQwenImageEdit: 第一个=正向 prompt, 第二个=负向 prompt
    text_encode_nodes = []
    for node_id, node in wf.items():
        if node.get("class_type") == "TextEncodeQwenImageEdit":
            text_encode_nodes.append((node_id, node))

    # 按节点 ID 排序, 第一个注入正向 prompt
    text_encode_nodes.sort(key=lambda x: x[0])
    if len(text_encode_nodes) >= 1:
        text_encode_nodes[0][1]["inputs"]["prompt"] = prompt.strip()
    if len(text_encode_nodes) >= 2:
        text_encode_nodes[1][1]["inputs"]["prompt"] = neg_prompt.strip() if neg_prompt else ""

    # KSampler → 注入 seed
    for node_id, node in wf.items():
        if node.get("class_type") == "KSampler":
            node["inputs"]["seed"] = int(seed)

    return wf


# ── T2I Prompt 解析 ──────────────────────────────────
def parse_t2i_spec(spec_path: Path) -> list[dict]:
    if not spec_path.exists():
        print(f"  [ERROR] 文件不存在: {spec_path}")
        return []

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    images = []

    block_pattern = re.compile(
        r'###\s+(.+?)\n(.*?)(?=\n###\s+|\n---\s*\n##\s*制作优先级|\n##\s*文件命名规范|\Z)',
        re.DOTALL,
    )

    for match in block_pattern.finditer(content):
        name = match.group(1).strip()
        block = match.group(2)

        if "文件命名规范" in name or "制作优先级" in name:
            continue

        img = {"name": name}

        field_pattern = re.compile(r'-\s*\*\*(.*?)\*\*[：:]\s*(.*?)(?=\n-\s*\*\*|\n\n|\Z)', re.DOTALL)
        fields = {}
        for fm in field_pattern.finditer(block):
            key = fm.group(1).strip().lower()
            val = fm.group(2).strip()
            fields[key] = val

        img["prompt"] = fields.get("画面", fields.get("prompt", ""))
        img["neg_prompt"] = fields.get("负面词", fields.get("negative prompt", ""))

        size_str = fields.get("尺寸", fields.get("size", ""))
        size_match = re.findall(r'(\d+)', size_str)
        if len(size_match) >= 2:
            img["width"] = int(size_match[0])
            img["height"] = int(size_match[1])
        else:
            img["width"] = 1920
            img["height"] = 1920

        seed_str = fields.get("seed", "42")
        seed_match = re.search(r'(\d+)', seed_str)
        img["seed"] = int(seed_match.group(1)) if seed_match else 42

        file_val = fields.get("文件", fields.get("file", ""))
        file_val = file_val.strip("`'\" ")
        img["output_file"] = file_val if file_val else f"13_{name.replace(' ', '_')}.png"

        if not img["prompt"]:
            print(f"  [WARNING] {name}: 无画面描述 (prompt)，跳过")
            continue

        images.append(img)

    return images


# ── 单张生成 (自动路由 T2I / Image Edit) ──────────────
def run_one_image(img: dict, output_dir: Path) -> bool:
    name = img["name"]
    output_file = img["output_file"]

    # 检查是否为角色镜头 → Image Edit
    ref_info = get_character_ref(name)

    if ref_info:
        mode = "IMAGE_EDIT"
        ref_path = ref_info["ref_path"]
        target_name = ref_info["target_name"]
        ref_filename = upload_ref_to_comfyui(ref_path, target_name)
        print(f"\n  [IMAGE_EDIT] {name}")
        print(f"    参考图: {ref_path.name}")
        wf = build_image_edit(
            prompt=img["prompt"],
            neg_prompt=img["neg_prompt"],
            ref_filename=ref_filename,
            width=img["width"],
            height=img["height"],
            seed=img["seed"],
        )
    else:
        mode = "Z-IMAGE-TURBO"
        print(f"\n  [Z-IMAGE] {name}")
        wf = build_zimage_t2i(
            prompt=img["prompt"],
            neg_prompt=img["neg_prompt"],
            width=img["width"],
            height=img["height"],
            seed=img["seed"],
        )

    print(f"    文件: {output_file}")
    print(f"    尺寸: {img['width']}x{img['height']} | Seed: {img['seed']}")
    print(f"    Prompt: {img['prompt'][:120]}...")

    try:
        pid = queue_prompt(wf)
        print(f"    已提交 (prompt_id={pid})，等待生成...")
        history = wait_for_prompt(pid, timeout=600)
        outputs = find_output_files(history)

        if outputs:
            output_dir.mkdir(parents=True, exist_ok=True)
            ok = True
            for out in outputs:
                dst = output_dir / output_file
                if download_output_image(out, dst):
                    size_kb = dst.stat().st_size // 1024
                    print(f"    ✅ 已保存: {dst} ({size_kb}KB)")
                else:
                    print(f"    ❌ 下载失败: {out['filename']}")
                    ok = False
            return ok
        else:
            print(f"    [ERROR] 无输出文件")
            return False

    except Exception as e:
        print(f"    [ERROR] 失败: {e}")
        return False


# ── 主流程 ────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="第13集 T2I 静态图批量生成")
    parser.add_argument("--dry-run", action="store_true", help="仅打印计划，不实际提交")
    parser.add_argument("--priority", type=str, choices=["p0", "p1", "p2", "p3", "all"], default="all",
                        help="按优先级筛选")
    parser.add_argument("--shot", type=str, help="仅生成指定图 (名称模糊匹配)")
    args = parser.parse_args()

    images = parse_t2i_spec(T2I_SPEC_PATH)
    print(f"共解析 {len(images)} 张图像:")

    # 标注每张图使用的生成方式
    for img in images:
        ref_info = get_character_ref(img["name"])
        if ref_info:
            mode_str = f"🖼️ Image Edit (ref: {ref_info['ref_path'].name})"
        else:
            mode_str = "📝 Z-Image-Turbo"
        print(f"  - {img['name']} → {img['output_file']} ({img['width']}x{img['height']}) [{mode_str}]")

    if args.priority != "all":
        allowed = PRIORITY_MAP.get(args.priority, [])
        images = [img for img in images if any(a in img["name"] for a in allowed)]
        print(f"\n按优先级 {args.priority.upper()} 筛选后: {len(images)} 张")

    if args.shot:
        images = [img for img in images if args.shot in img["name"]]
        print(f"\n按关键词 '{args.shot}' 筛选后: {len(images)} 张")

    if not images:
        print("无符合条件的图像，退出")
        return

    if args.dry_run:
        print("\n[Dry-run] 以下是将要生成的图像:")
        for img in images:
            ref_info = get_character_ref(img["name"])
            if ref_info:
                mode_str = f"Image Edit (ref: {ref_info['ref_path'].name})"
            else:
                mode_str = "Z-Image-Turbo"
            print(f"  → {img['output_file']} [{mode_str}] ({img['width']}x{img['height']}, seed={img['seed']})")
        return

    output_dir = OUTPUT_DIR
    success = 0
    for i, img in enumerate(images, 1):
        print(f"\n{'─'*50}")
        print(f"[{i}/{len(images)}]")
        ok = run_one_image(img, output_dir)
        if ok:
            success += 1
        time.sleep(1)

    print(f"\n{'='*60}")
    print(f"生成完成: {success}/{len(images)}")
    print(f"输出目录: {output_dir}")


if __name__ == "__main__":
    main()