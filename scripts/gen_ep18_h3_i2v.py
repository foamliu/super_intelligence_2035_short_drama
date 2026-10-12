#!/usr/bin/env python3
"""第18集《暖阳》 Minimax H3 I2V 分镜视频生成脚本（固化 · S3 放量）。

作用：把第 18 集「分镜帧（OUTPUT/18_暖阳/frames/）→ H3 I2V 视频片段」固化成
可复用、可续跑、可审计的脚本。台词**随 H3 一起生成**（写进 prompt 的 `Audio:`，
🚫 本线禁用 TTS，见任务书 §4.5 / 运维指令区 ⑦）。

- 分镜权威：`SCENES/18_暖阳.md` 的 `## 逐镜表`（7 列）
- 台词权威：`scripts/ep18_dialogue.py`（Audio: 内文字与其逐字一致）
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep18_h3_i2v.py --dry-run            # 仅打印计划（核镜数/帧/时长）
  python scripts/gen_ep18_h3_i2v.py --limit 2            # 只跑前 2 镜
  python scripts/gen_ep18_h3_i2v.py --shot 01            # 只跑某镜（按镜号）
  python scripts/gen_ep18_h3_i2v.py                      # 跑本批全部镜头

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（→1056×608；0.92/720p 必 OOM；要 1080p 事后 SeedVR2 超分）
  - steps：静态·单人·对话 = 4（本批全部为静态/单人/对话）
  - 台词长度须匹配镜头时长（`17k+5` 帧量化：4s→4.46 / 5s→5.17 / 6s→6.58 实际播放）
  - 无台词镜只写「正向音景」（不含可读词句、不用否定式）
  - 🚫 禁写元信息 / 对模型说的话 / 镜头编号指代（会渲染成画面字幕）
"""
import argparse
import json
import shutil
import time
import urllib.request
import uuid
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "workflows" / "video_minimax_h3_i2v.json"
FRAMES = ROOT / "OUTPUT" / "18_暖阳" / "frames"
OUT = ROOT / "OUTPUT" / "18_暖阳" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6
STEPS = 4  # 本批全部为静态·单人·对话


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


def upload_frame(frame_name: str) -> str:
    """把分镜帧复制到 ComfyUI input（文件名已是 ASCII，无需改名）。"""
    src = FRAMES / frame_name
    if not src.exists():
        raise FileNotFoundError(f"缺分镜帧: {src}")
    dst = get_comfyui_input_dir() / frame_name
    if not dst.exists() or src.stat().st_size != dst.stat().st_size:
        shutil.copy2(src, dst)
    return frame_name



# ── 第一批镜头（相遇 / 倾诉 · 有现成分镜帧 · 单人/无台词）──
# 镜号 / 名称 / 帧 / 时长 / seed / prompt（英文电影感 + Audio: 台词原文）
SHOTS = [
    {
        "shot": "01", "name": "深夜网约车刷手机",
        "img": "18_car_01_night_driving.png",
        "dur": 4.0, "seed": 1801,
        "prompt": (
            "Cinematic semi-realistic footage, 45-year-old Chinese man in the driver seat "
            "of a dim rideshare car at late night, scrolling a smartphone. Cold blue night "
            "and warm orange dashboard light mix on his tired face; the phone screen's cold "
            "white glow lights the lower half of his face. He leans back and scrolls slowly. "
            "Subtle ink-wash bleed only in the window glass. Medium shot, fixed camera. "
            "Audio: distant city traffic hum, low air-conditioning noise, faint dashboard creak."
        ),
    },
    {
        "shot": "02", "name": "暖阳广告·小晴",
        "img": "18_xiaoqing_avatar.png",
        "dur": 5.0, "seed": 1802,
        "prompt": (
            "Cinematic semi-realistic footage, an 18-year-old Chinese girl sitting by a window, "
            "warm sunlight falling on her face, two shallow dimples when she smiles, natural black "
            "medium-length hair, soft clean warm light, plain light background. She speaks gently "
            "toward the camera. Close-up, slow push-in. "
            "Audio: 你是不是也有话想说，但不知道该跟谁说？"
        ),
    },
    {
        "shot": "04", "name": "老周戴耳机",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 4.0, "seed": 1804,
        "prompt": (
            "Cinematic semi-realistic footage, 45-year-old Chinese man with tired eyes in a dim car, "
            "putting on earphones, the car interior growing quiet, only the phone screen glow on his "
            "face, lips slightly parted as he listens. Cold blue night. Medium-close shot, fixed camera. "
            "Audio: 老周，晚上好。"
        ),
    },
    {
        "shot": "05", "name": "老周愣住",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 3.0, "seed": 1805,
        "prompt": (
            "Cinematic semi-realistic footage, 45-year-old Chinese man in a dim car, stunned, "
            "his throat moves once, a long time since anyone called his name so gently; phone screen "
            "cold glow on his face. Cold blue night. Close-up, fixed camera. "
            "Audio: 诶。"
        ),
    },
    {
        "shot": "08", "name": "老周沉默·喉结微动",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 4.0, "seed": 1808,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man's face lit by phone screen "
            "glow in a dark car, silent for a few seconds, his throat moves. Cold blue night. "
            "Medium-close shot, fixed camera. "
            "Audio: 那咱们慢慢聊。不想说的不用勉强。"
        ),
    },
    {
        "shot": "14", "name": "老周第一次哭",
        "img": "18_laozhou_03_tears.png",
        "dur": 6.0, "seed": 1814,
        "prompt": (
            "Cinematic semi-realistic footage, close-up of a 45-year-old Chinese man in dim warm "
            "light, a tear sliding down from the corner of his eye, silent, holding back; phone screen "
            "glow on his tear-streaked face. Restrained, quiet. Close-up, slow push-in. "
            "Audio: 老周，你一个人扛了这么久，辛苦了。"
        ),
    },
]


# ── API Helpers（同 gen_ep13_h3_i2v.py 范式）──────────
def load_wf(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")


def wait(pid, timeout=1200):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = urllib.request.urlopen(f"{COMFY}/history/{pid}", timeout=10)
            d = json.loads(r.read())
            h = d.get(pid, {})
            st = h.get("status", {}).get("status_str", "")
            if st == "success" and h.get("outputs"):
                return h
            if st == "error":
                raise RuntimeError(f"ComfyUI error: {h.get('status', {}).get('messages', '')}")
        except RuntimeError:
            raise
        except Exception:
            pass
        time.sleep(5)
    raise TimeoutError(f"Timeout: {pid}")


def download(hist, out_dir):
    saved = []
    for _nid, node in hist.get("outputs", {}).items():
        for key in ("gifs", "images"):
            for item in node.get(key, []):
                fn = item["filename"]
                sub = item.get("subfolder", "")
                typ = item.get("type", "output")
                url = f"{COMFY}/view?filename={fn}&subfolder={sub}&type={typ}"
                dst = out_dir / fn
                urllib.request.urlretrieve(url, str(dst))
                saved.append(fn)
    return saved


def build_workflow(shot):
    wf = load_wf(WF)
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "LoadImage":
            node["inputs"]["image"] = shot["img"]
        elif ct == "MiniMaxH3ImageToVideo":
            node["inputs"]["prompt"] = shot["prompt"]
        elif ct == "PrimitiveFloat":
            node["inputs"]["value"] = shot["dur"]
        elif ct == "RandomNoise":
            node["inputs"]["noise_seed"] = shot["seed"]
        elif ct == "BasicScheduler":
            node["inputs"]["steps"] = STEPS
        elif ct == "ResolutionSelector":
            node["inputs"]["megapixels"] = MEGAPIXELS
            node["inputs"]["aspect_ratio"] = "16:9 (Widescreen)"
        elif ct == "SaveVideo":
            node["inputs"]["filename_prefix"] = f"video/EP18_SHOT-{shot['shot']}_H3"
    return wf


def run_one(shot):
    sid = shot["shot"]
    print(f"\n── SHOT-{sid}: {shot['name']} ({shot['dur']}s · seed={shot['seed']})")
    frame = upload_frame(shot["img"])
    wf = build_workflow(shot)
    pid = queue(wf)
    print(f"    submitted {pid[:8]}... waiting (5–15 min)...")
    t0 = time.time()
    hist = wait(pid)
    saved = download(hist, OUT)
    print(f"    done in {int(time.time() - t0)}s")
    for fn in saved:
        mb = (OUT / fn).stat().st_size / (1024 * 1024)
        print(f"    ✅ {fn} ({mb:.1f}MB)")
    if len(saved) == 1:
        src = OUT / saved[0]
        dst = OUT / f"EP18_SHOT-{sid}_H3_{shot['name']}.mp4"
        if src.suffix != ".mp4":
            dst = dst.with_suffix(src.suffix)
        if src != dst:
            src.rename(dst)
            print(f"    → renamed {dst.name}")
    return frame


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》H3 I2V 分镜视频生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--shot", type=str, help="按镜号筛选（如 01）")
    ap.add_argument("--limit", type=int, help="只跑前 N 镜")
    args = ap.parse_args()

    shots = [s for s in SHOTS if not args.shot or s["shot"] == args.shot]
    if args.limit:
        shots = shots[: args.limit]

    print("=" * 66)
    print(f" EP18《暖阳》H3 I2V  |  {len(shots)}/{len(SHOTS)} 镜  |  mp={MEGAPIXELS} steps={STEPS}")
    print(f" 帧目录: {FRAMES}\n 输出: {OUT}")
    print("=" * 66)
    for s in shots:
        print(f"  - SHOT-{s['shot']}  {s['name']}  {s['dur']}s  ← {s['img']}  seed={s['seed']}")
    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    ok_n = 0
    for i, s in enumerate(shots, 1):
        try:
            run_one(s)
            ok_n += 1
        except Exception as e:
            print(f"    ❌ {e}")
        time.sleep(1)
    print(f"\n{'=' * 66}\n 完成: {ok_n}/{len(shots)}  输出: {OUT}")


if __name__ == "__main__":
    main()

