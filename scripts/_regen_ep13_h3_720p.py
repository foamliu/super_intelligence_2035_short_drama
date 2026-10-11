#!/usr/bin/env python3
"""EP13 Minimax H3 重制 (1280x720 16:9)。

工作流 video_minimax_h3_i2v.json 已改为 16:9 Widescreen + 0.92MP(≈1280x720)。
按镜头重新生成，输出文件名带 _720p 标记，与旧的 640x640 版本区分。

用法:
  python scripts/_regen_ep13_h3_720p.py            # 全部 4 个镜头
  python scripts/_regen_ep13_h3_720p.py --shot 01  # 仅 SHOT-01 (验证用)
"""
import json, time, uuid, urllib.request, argparse, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "workflows" / "video_minimax_h3_i2v.json"
OUT = ROOT / "OUTPUT" / "13_外骨骼" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

SHOTS = [
    {
        "shot": "01", "name": "莎拉解释外骨骼",
        "img": "13_sarah_01_desk_explaining.png",
        "out": "EP13_SHOT-01_H3_720p_sarah_desk_explaining.mp4",
        "dur": 10.0, "seed": 8001,
        "prompt": (
            "Cinematic real-life footage, 28yo Chinese woman at tech office desk. "
            "Phone to right ear, lips moving in natural conversation. "
            "Free hand gestures from chest toward monitors — 'my tool not my replacement'. "
            "Points at virtual-audience heatmap on right screen: red zone labeled '0.52'. "
            "Earnest eyes, not showing off. Dual monitor cold blue + afternoon sun on face. "
            "Subtle ink-wash bleed from monitor bezels. "
            "Natural micro-expressions, blinking, hand gestures. Cinematic lighting. "
            "Audio: office ambience, distant keyboard clicks, phone call murmur, monitor hum."
        ),
    },
    {
        "shot": "03", "name": "师兄·合法吗",
        "img": "13_shixiong_01_coffee.png",
        "out": "EP13_SHOT-03_H3_720p_shixiong_coffee_legal.mp4",
        "dur": 7.0, "seed": 8003,
        "prompt": (
            "Cinematic real-life, 31yo Chinese male tech worker in open-plan office. "
            "Holds company-logo coffee cup, dark circles under eyes — lab veteran look. "
            "Turns head slightly off-screen, lips move asking a question, neutral expression. "
            "After speaking, corner of mouth barely lifts — half-mm micro-smile, "
            "not approval or disapproval, just recognition. Then sips coffee, covering it. "
            "Cold fluorescent light, visible pores and fine lines. Semi-realistic. "
            "Medium shot, subtle handheld drift. "
            "Audio: office hum, distant typing, coffee cup set down."
        ),
    },
    {
        "shot": "06", "name": "莎拉地铁观察",
        "img": "13_sarah_02_subway_observing.png",
        "out": "EP13_SHOT-06_H3_720p_sarah_subway_observing.mp4",
        "dur": 8.0, "seed": 8006,
        "prompt": (
            "Cinematic real-life, 28yo Chinese woman in crowded Shanghai morning subway. "
            "Grips overhead strap. Does NOT look at phone — everyone else staring at screens. "
            "Head turns very slowly, gaze sweeping: grocery-bag woman, leaky-headphone student, "
            "dozing old man. Not staring — taking it in. Eyes pause on old man's face. "
            "Train sways, hand adjusts grip. Harsh fluorescent + tunnel lights sweep. "
            "Ink-wash only on window glass behind her — she observes, wash stays off her. "
            "Extremely quiet — motion is 'almost looking'. "
            "Audio: subway rumble, distant announcement echo, phone pings, wheels on track."
        ),
    },
    {
        "shot": "11", "name": "吧台散场·0.52",
        "img": "13_sarah_03_bar_aftermath.png",
        "out": "EP13_SHOT-11_H3_720p_sarah_bar_052.mp4",
        "dur": 10.0, "seed": 8011,
        "prompt": (
            "Cinematic real-life, 28yo Chinese woman sitting sideways at closed comedy-club bar. "
            "Warm dim lighting. Stage mic stand empty. Phone screen lights cold white: "
            "WeChat message 'That ending tonight, 0.52?'. Cold screen on lower half of face. "
            "Thumb hovers — reply typed but not sent. Lips barely move — silently mouthing '0.52'? "
            "No smile. Taps send. Exhales — not heavy, just an exhale. "
            "Dark wine-red + warm amber + cold phone white on face. "
            "Outside window: distant Shenzhen data-center constant-blue through glass. "
            "Cold blue vs warm amber — subtle battle on her profile. "
            "Semi-realistic with ink-wash bleeding from window. Extremely quiet. "
            "Audio: bar after-hours silence, glass clink, phone tap, distant city hum."
        ),
    },
]


def load_wf(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")


def wait(pid, timeout=2400):
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
                raise RuntimeError(
                    f"ComfyUI 执行出错: {json.dumps(h.get('status', {}), ensure_ascii=False)}")
        except RuntimeError:
            raise
        except Exception:
            pass
        time.sleep(5)
    raise TimeoutError(f"Timeout: {pid}")


def download(hist, out_dir):
    saved = []
    for nid, node in hist.get("outputs", {}).items():
        for key in ("gifs", "audio", "images"):
            for item in node.get(key, []):
                fn = item["filename"]
                sub = item.get("subfolder", "")
                typ = item.get("type", "output")
                url = f"{COMFY}/view?filename={fn}&subfolder={sub}&type={typ}"
                dst = out_dir / fn
                urllib.request.urlretrieve(url, str(dst))
                saved.append(fn)
    return saved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", type=str, help="镜头编号, 逗号分隔, e.g. 01 或 03,06,11")
    args = ap.parse_args()

    shots = ([s for s in SHOTS if s["shot"] in args.shot.split(",")]
             if args.shot else SHOTS)
    print("=" * 60)
    print(f" EP13 H3 重制 (1280x720 16:9)  |  目标镜头: "
          f"{', '.join(s['shot'] for s in shots)}")
    print("=" * 60)

    for i, shot in enumerate(shots, 1):
        sid = shot["shot"]
        print(f"\n── [{i}/{len(shots)}] SHOT-{sid}: {shot['name']} ({shot['dur']}s)")

        wf = load_wf(WF)
        for nid, node in wf.items():
            ct = node.get("class_type", "")
            if ct == "LoadImage":
                node["inputs"]["image"] = shot["img"]
            elif ct == "MiniMaxH3ImageToVideo":
                node["inputs"]["prompt"] = shot["prompt"]
            elif ct == "PrimitiveFloat":
                node["inputs"]["value"] = shot["dur"]
            elif ct == "RandomNoise":
                node["inputs"]["noise_seed"] = shot["seed"]
            elif ct == "SaveVideo":
                node["inputs"]["filename_prefix"] = f"video/EP13_SHOT-{sid}_H3_720p"

        try:
            pid = queue(wf)
            print(f"    submitted {pid[:8]}... waiting (可能 10-30 min)...")
            t0 = time.time()
            hist = wait(pid, timeout=2400)
            print(f"    done in {int(time.time()-t0)}s")

            saved = download(hist, OUT)
            for fn in saved:
                mb = (OUT / fn).stat().st_size / (1024 * 1024)
                print(f"    [OK] {fn} ({mb:.1f}MB)")
            if len(saved) == 1:
                src = OUT / saved[0]
                dst = OUT / shot["out"]
                if src.suffix != dst.suffix:
                    dst = dst.with_suffix(src.suffix)
                if src != dst:
                    src.rename(dst)
                    print(f"    -> renamed {dst.name}")
        except Exception as e:
            print(f"    [ERROR] {e}")

    print(f"\n{'='*60}")
    print(" 完成。检查:", OUT)


if __name__ == "__main__":
    main()


