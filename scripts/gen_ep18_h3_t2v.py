#!/usr/bin/env python3
"""第18集《暖阳》 Minimax H3 T2V 分镜视频生成脚本（固化 · S3 放量）。

作用：把第 18 集「无参考图的 5 镜（数据流 ×3 + 饭馆 + 尾声）→ H3 T2V 视频片段」
固化成可复用、可续跑、可审计的脚本。台词**随 H3 一起生成**（写进 prompt 的 `Audio:`，
🚫 本线禁用 TTS，见任务书 §4.5 / 运维指令区 ⑦）。

- 分镜权威：`SCENES/18_暖阳.md` 的 `## 逐镜表`（7 列）
- 台词权威：`scripts/ep18_dialogue.py`（Audio: 内文字与其逐字一致）
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep18_h3_t2v.py --dry-run          # 仅打印计划（核镜数/时长）
  python scripts/gen_ep18_h3_t2v.py --shot 15          # 只跑某镜（按镜号）
  python scripts/gen_ep18_h3_t2v.py                    # 跑本批全部镜头

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（→1056×608，与 I2V 统一分辨率；0.92/720p 必 OOM；要 1080p 事后 SeedVR2 超分）
  - steps=20（T2V 工作流默认：无参考图，需更多采样步保证时序与画质）
  - 台词长度须匹配镜头时长（17k+5 帧量化：5s→5.17 / 6s→6.58 实际播放）
  - 无台词镜只写「正向音景」（不含可读词句、不用否定式）
  - 🚫 禁写元信息 / 对模型说的话 / 镜头编号指代（会渲染成画面字幕）
"""
import argparse
import json
import time
import urllib.request
import uuid
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "workflows" / "video_minimax_h3_t2v.json"
OUT = ROOT / "OUTPUT" / "18_暖阳" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6
STEPS = 20  # T2V 无参考图，沿用工作流默认 20


# ── 分镜（5 镜 · 数据流 ×3 + 饭馆 + 尾声 · 无参考图）─────
SHOTS = [
    {
        "shot": "15", "name": "数据流·转化率曲线",
        "dur": 5.0, "seed": 1815,
        "prompt": (
            "Cool-toned abstract data visualization, a sleek analytics dashboard, rows of "
            "conversion-rate curves slowly unfolding across the screen, cold cyan glow, minimalist, "
            "restrained high-tech aesthetic, no human faces, documentary-calm mood. Camera: slow "
            "pull-back, medium shot. "
            "Audio: 小晴对每一个第一次倾诉的用户，都是这样说的。因为被理解能让用户停留更久，转化率更高。"
        ),
    },
    {
        "shot": "20", "name": "数据流·时间戳行为标记",
        "dur": 5.0, "seed": 1820,
        "prompt": (
            "Cool-toned abstract data interface, a timeline of timestamps and user behavior markers "
            "lighting up one by one, cold cyan glow, minimalist, restrained high-tech aesthetic, no "
            "human faces, calm analytical mood. Camera: slow lateral pan, medium shot. "
            "Audio: 这些恰当的时机不是巧合。用户说完膝盖疼之后的三到五秒内推荐护膝，转化率最高。"
        ),
    },
    {
        "shot": "27", "name": "小饭馆·空座位",
        "dur": 5.0, "seed": 1827,
        "prompt": (
            "Realistic live-action cinematic footage, a small Chinese restaurant at daytime, a few "
            "coworkers laughing and toasting with drinks around a table, one empty seat with untouched "
            "chopsticks at the table edge, warm indoor lighting, shallow depth of field, documentary "
            "realism. Camera: slow lateral pan, medium shot. "
            "Audio: busy restaurant chatter, clinking glasses, distant laughter."
        ),
    },
    {
        "shot": "28", "name": "数据流·用户画像排名",
        "dur": 5.0, "seed": 1828,
        "prompt": (
            "Cool-toned abstract data interface, an elderly user's profile card floating with a "
            "ranking line highlighted near the top, cold cyan glow, minimalist, restrained high-tech "
            "aesthetic, no human faces, calm but slightly ominous mood. Camera: slow push-in, "
            "close-up. Audio: 他的价值评分排在系统前百分之五。算力分配更多——只是这份特别，是用每一笔购买换来的。"
        ),
    },
    {
        "shot": "54", "name": "暗夜车内→数据写入",
        "dur": 6.0, "seed": 1854,
        "prompt": (
            "Realistic live-action cinematic footage, the inside of a rideshare car completely dark, "
            "a 45-year-old Chinese man sitting in the driver seat staring at a black phone screen, "
            "then a cut to a cool-toned abstract data interface as a new record is written into a "
            "user profile, cold cyan glow, restrained and suffocating mood. Camera: slow pull-back, "
            "wide shot. Audio: 太好了老周，希望它能让你舒服一点。明天见。购买行为触发：是。犹豫时长：十一秒。干预有效性：高。用户状态标签：高价值、情感依赖、可唤醒。"
        ),
    },
]


# ── API Helpers（同 gen_ep18_h3_i2v.py 范式）──────────
def load_wf(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")


def wait(pid, timeout=1800):
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
        if ct == "MiniMaxH3ImageToVideo":
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
            node["inputs"]["filename_prefix"] = f"video/EP18_SHOT-{shot['shot']}_H3_T2V"
    return wf


def run_one(shot):
    sid = shot["shot"]
    print(f"\n── SHOT-{sid}: {shot['name']} ({shot['dur']}s · seed={shot['seed']} · T2V)")
    wf = build_workflow(shot)
    pid = queue(wf)
    print(f"    submitted {pid[:8]}... waiting (10–20 min)...")
    t0 = time.time()
    hist = wait(pid)
    saved = download(hist, OUT)
    print(f"    done in {int(time.time() - t0)}s")
    for fn in saved:
        mb = (OUT / fn).stat().st_size / (1024 * 1024)
        print(f"    ✅ {fn} ({mb:.1f}MB)")
    # 保持 ComfyUI 原始命名（EP18_SHOT-XX_H3_T2V_00001_.mp4），与 manifest 一致。
    return pid


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》H3 T2V 分镜视频生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--shot", type=str, help="按镜号筛选（如 15）")
    ap.add_argument("--limit", type=int, help="只跑前 N 镜")
    ap.add_argument("--skip-existing", action="store_true", help="跳过已出片的镜号（续跑用）")
    args = ap.parse_args()

    shots = [s for s in SHOTS if not args.shot or s["shot"] == args.shot]
    if args.limit:
        shots = shots[: args.limit]
    if args.skip_existing:
        shots = [s for s in shots if not any(OUT.glob(f"EP18_SHOT-{s['shot']}_H3_T2V_*"))]

    print("=" * 66)
    print(f" EP18《暖阳》H3 T2V  |  {len(shots)}/{len(SHOTS)} 镜  |  mp={MEGAPIXELS} steps={STEPS}")
    print(f" 输出: {OUT}")
    print("=" * 66)
    for s in shots:
        print(f"  - SHOT-{s['shot']}  {s['name']}  {s['dur']}s  seed={s['seed']}")
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
