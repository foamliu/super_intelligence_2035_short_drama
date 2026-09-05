"""Batch character image generator via ComfyUI API.

Usage:
    python scripts/generate_characters.py --priority P0          # Generate P0 first
    python scripts/generate_characters.py --character 林薇       # Single character
    python scripts/generate_characters.py --all                  # All characters
    python scripts/generate_characters.py --dry-run --priority P0  # Preview only
    python scripts/generate_characters.py --status               # Show progress
"""
import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path
from datetime import datetime

CHAR_DIR = Path("ASSETS/CHARACTERS")
BATCH_FILE = CHAR_DIR / "batch_prompts.json"
STATUS_FILE = CHAR_DIR / "generation_status.json"

# Default ComfyUI server
COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")

# Z-Image-Turbo workflow template (国产优先)
T2I_WORKFLOW = json.loads(Path("workflows/Z-Image-Turbo 文生图.json").read_text(encoding="utf-8"))


def load_batch():
    """Load batch prompts from the manifest."""
    if not BATCH_FILE.exists():
        print(f"❌ {BATCH_FILE} not found. Run extract_character_prompts.py first.")
        sys.exit(1)
    return json.loads(BATCH_FILE.read_text(encoding="utf-8"))


def load_status():
    """Load or initialize generation status."""
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    return {"generations": {}, "summary": {}}


def save_status(status):
    STATUS_FILE.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")


def filter_jobs(jobs, priority=None, character=None):
    """Filter jobs by priority and/or character name."""
    filtered = jobs
    if priority:
        filtered = [j for j in filtered if j['priority'] == priority]
    if character:
        filtered = [j for j in filtered if j['character'] == character]
    return filtered


def get_pending_jobs(jobs, status):
    """Return jobs that haven't been generated yet."""
    pending = []
    for j in jobs:
        key = f"{j['character']}/{j['shot_title']}"
        if key not in status['generations'] or status['generations'][key]['status'] != 'done':
            pending.append(j)
    return pending


def build_workflow_prompt(job):
    """Modify the Z-Image-Turbo workflow template with the character prompt."""
    wf = json.loads(json.dumps(T2I_WORKFLOW))  # deep copy

    # Find the CLIPTextEncode node with the positive prompt
    clip_node = None
    for node_id, node_data in wf.items():
        if node_data.get("class_type") == "CLIPTextEncode":
            # Check if this is a positive conditioning node (not zeroed out)
            inputs = node_data.get("inputs", {})
            text_val = inputs.get("text", "")
            if text_val and len(text_val) > 10:
                clip_node = node_id
                break

    if not clip_node:
        # Can't find the right node—just pick the first CLIPTextEncode
        for node_id, node_data in wf.items():
            if node_data.get("class_type") == "CLIPTextEncode":
                clip_node = node_id
                break

    if clip_node:
        # Set positive prompt
        full_prompt = job['positive_prompt']
        wf[clip_node]["inputs"]["text"] = full_prompt

    # Set dimensions
    for node_id, node_data in wf.items():
        if node_data.get("class_type") in ("EmptySD3LatentImage", "EmptyLatentImage"):
            wf[node_id]["inputs"]["width"] = job.get("width", 1280)
            wf[node_id]["inputs"]["height"] = job.get("height", 720)
            wf[node_id]["inputs"]["batch_size"] = 1

    # Set seed
    seed = job.get("seed", -1)
    if seed == -1:
        seed = int.from_bytes(os.urandom(8), "big") % (2**63)
    for node_id, node_data in wf.items():
        if node_data.get("class_type") == "KSampler":
            wf[node_id]["inputs"]["seed"] = seed
    job["seed"] = seed

    return wf, seed


def submit_to_comfyui(workflow, job):
    """Submit a workflow to ComfyUI API. Returns prompt_id."""
    import urllib.request

    payload = {"prompt": workflow, "client_id": f"char_gen_{uuid.uuid4().hex[:8]}"}
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        return result.get("prompt_id")
    except Exception as e:
        print(f"  ❌ ComfyUI API error: {e}")
        return None


def wait_for_result(prompt_id, timeout=300):
    """Poll ComfyUI for generation result."""
    import urllib.request

    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"{COMFYUI_URL}/history/{prompt_id}")
            resp = urllib.request.urlopen(req, timeout=5)
            history = json.loads(resp.read())
            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                for node_id, output_data in outputs.items():
                    images = output_data.get("images", [])
                    if images:
                        return images[0]
            time.sleep(2)
        except Exception:
            time.sleep(2)
    return None


def download_image(image_info, output_path):
    """Download generated image from ComfyUI."""
    import urllib.request

    filename = image_info.get("filename")
    subfolder = image_info.get("subfolder", "")
    img_type = image_info.get("type", "output")

    url = f"{COMFYUI_URL}/view"
    params = f"?filename={filename}&type={img_type}"
    if subfolder:
        params += f"&subfolder={subfolder}"

    try:
        req = urllib.request.Request(url + params)
        data = urllib.request.urlopen(req, timeout=30).read()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(data)
        return True
    except Exception as e:
        print(f"  ❌ Download error: {e}")
        return False


def generate_job(job, status, dry_run=False):
    """Generate one character image."""
    key = f"{job['character']}/{job['shot_title']}"
    output_path = job["output_rel_path"]

    print(f"\n🎨 {job['priority']} | {job['character']} | {job['shot_title']}")

    if dry_run:
        print(f"  📝 DRY RUN: Would generate → {output_path}")
        print(f"  📝 Prompt: {job['positive_prompt'][:120]}...")
        return

    # Build workflow
    workflow, seed = build_workflow_prompt(job)
    print(f"  🌱 Seed: {seed}")
    print(f"  📐 Size: {job['width']}×{job['height']}")

    # Submit
    prompt_id = submit_to_comfyui(workflow, job)
    if not prompt_id:
        status['generations'][key] = {
            "status": "failed",
            "error": "API submission failed",
            "timestamp": datetime.now().isoformat()
        }
        save_status(status)
        return

    print(f"  📤 Submitted: {prompt_id}")
    status['generations'][key] = {
        "status": "submitted",
        "prompt_id": prompt_id,
        "seed": seed,
        "timestamp": datetime.now().isoformat()
    }
    save_status(status)

    # Wait
    print(f"  ⏳ Waiting for generation...")
    result = wait_for_result(prompt_id)
    if not result:
        status['generations'][key]['status'] = 'timeout'
        save_status(status)
        print(f"  ⏰ Timeout after 5min")
        return

    # Download
    ok = download_image(result, output_path)
    if ok:
        status['generations'][key]['status'] = 'done'
        status['generations'][key]['output'] = output_path
        print(f"  ✅ Saved to {output_path}")
    else:
        status['generations'][key]['status'] = 'download_failed'
        print(f"  ❌ Download failed")

    save_status(status)


def show_status(jobs, status):
    """Display generation progress."""
    total = len(jobs)
    done = sum(1 for j in jobs
               if f"{j['character']}/{j['shot_title']}" in status.get('generations', {})
               and status['generations'][f"{j['character']}/{j['shot_title']}"].get('status') == 'done')
    pending = total - done

    print(f"\n{'='*60}")
    print(f"📊 Generation Progress: {done}/{total} ({100*done//total if total else 0}%)")
    print(f"{'='*60}")

    for p in ["P0", "P1", "P2", "P3"]:
        p_jobs = [j for j in jobs if j['priority'] == p]
        p_done = sum(1 for j in p_jobs
                    if f"{j['character']}/{j['shot_title']}" in status.get('generations', {})
                    and status['generations'][f"{j['character']}/{j['shot_title']}"].get('status') == 'done')
        bar = "▓" * (10 * p_done // len(p_jobs)) + "░" * (10 - 10 * p_done // len(p_jobs)) if p_jobs else "░" * 10
        print(f"  {p}: [{bar}] {p_done}/{len(p_jobs)}")

    # Show individual character progress
    print(f"\n{'─'*60}")
    chars = {}
    for j in jobs:
        chars.setdefault(j['character'], {"total": 0, "done": 0})
        chars[j['character']]['total'] += 1
        key = f"{j['character']}/{j['shot_title']}"
        if key in status.get('generations', {}) and status['generations'][key].get('status') == 'done':
            chars[j['character']]['done'] += 1

    for name in sorted(chars.keys()):
        c = chars[name]
        icon = "✅" if c['done'] == c['total'] else ("🔄" if c['done'] > 0 else "⏳")
        print(f"  {icon} {name}: {c['done']}/{c['total']}")


def main():
    parser = argparse.ArgumentParser(description="Batch character image generator")
    parser.add_argument("--priority", choices=["P0", "P1", "P2", "P3"], help="Generate by priority")
    parser.add_argument("--character", help="Generate single character")
    parser.add_argument("--all", action="store_true", help="Generate all characters")
    parser.add_argument("--dry-run", action="store_true", help="Preview without generating")
    parser.add_argument("--status", action="store_true", help="Show progress only")
    parser.add_argument("--retry-failed", action="store_true", help="Retry failed generations")
    parser.add_argument("--limit", type=int, default=0, help="Max images to generate in this run")
    args = parser.parse_args()

    jobs = load_batch()
    status = load_status()

    if args.status:
        show_status(jobs, status)
        return

    # Filter jobs
    if args.all:
        target = jobs
    elif args.character:
        target = filter_jobs(jobs, character=args.character)
    elif args.priority:
        target = filter_jobs(jobs, priority=args.priority)
    else:
        # Default: show status and ask
        show_status(jobs, status)
        print("\n💡 Usage: --priority P0 | --character 林薇 | --all | --status")
        return

    if not target:
        print("❌ No jobs matching criteria.")
        return

    # Get pending/retry jobs
    if args.retry_failed:
        work_jobs = [j for j in target
                     if f"{j['character']}/{j['shot_title']}" in status.get('generations', {})
                     and status['generations'][f"{j['character']}/{j['shot_title']}"].get('status') != 'done']
    else:
        work_jobs = get_pending_jobs(target, status)

    print(f"\n🎯 Target: {len(target)} jobs → {len(work_jobs)} pending")
    if args.dry_run:
        print("🔍 DRY RUN MODE — no images will be generated\n")

    generated = 0
    for job in work_jobs:
        generate_job(job, status, dry_run=args.dry_run)
        generated += 1
        if args.limit and generated >= args.limit:
            print(f"\n⏹️ Reached limit of {args.limit} images")
            break
        if not args.dry_run:
            time.sleep(1)  # short gap between submissions

    print(f"\n{'='*60}")
    print(f"🏁 Done: {generated} jobs processed")
    show_status(jobs, status)


if __name__ == "__main__":
    main()