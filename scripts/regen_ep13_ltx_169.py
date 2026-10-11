#!/usr/bin/env python3
"""EP13 LTX-2.3 I2V 重做：16:9 1024x576 + 修复 prompt/duration 未生效的 bug。

原 gen_ep13_ltx_i2v.py 致命 bug：
  1. prompt 节点是 PrimitiveStringMultiline(320:319)，脚本却匹配 "LTXVImgToVideo"/"LTXV"
     → 实际是 LTXVImgToVideoInplace，prompt 从未写入，8 镜全用默认"琵琶女"文本
  2. duration 节点是 PrimitiveInt(320:301)，脚本却匹配 "PrimitiveFloat" → 时长未写入
  3. 分辨率固定 640x640（width/height 源都是 1280）

用法:
  python scripts/regen_ep13_ltx_169.py --shot 07
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
WF = ROOT / "workflows" / "Image to Video (LTX-2.3).json"
OUT = ROOT / "OUTPUT" / "13_外骨骼" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

W_SRC = 2048  # -> width  1024
H_SRC = 1152  # -> height 576

S = [
    {"shot":"07","name":"虚拟脸在笑","pri":"P0","img":"13_virtual_audience_01_imaginary_face.png",
     "out":"EP13_SHOT-07_LTX169_virtual_face.mp4","dur":6.0,"seed":9107,
     "prompt":("Cinematic video, glowing translucent AI-generated audience face on dark screen. "
               "Synthetic face, pixel-level micro-expressions ripple: mouth corner curls, eye crinkles laughing. "
               "Genuine infectious laugh, expression shifts fluidly, semi-transparent blue-white with pink warmth. "
               "Light particles drift, ultra-slow push in, 16:9 widescreen.")},
    {"shot":"08","name":"渲染vs真实","pri":"P0","img":"13_virtual_audience_02_render_vs_real.png",
     "out":"EP13_SHOT-08_LTX169_render_vs_real.mp4","dur":8.0,"seed":9108,
     "prompt":("Cinematic video, split-screen: top half rendered AI face synthetic smooth. "
               "Bottom half real audience face with pores, asymmetrical smile, warmth. "
               "Two halves slowly merge at center via soft wipe, thin glowing seam at boundary. "
               "Cold blue above, warm amber below, seam dissolves as crossfade completes, 16:9 widescreen.")},
    {"shot":"10","name":"微信十秒沉默","pri":"P1","img":"13_prop_02_wechat_hao.png",
     "out":"EP13_SHOT-10_LTX169_wechat_silence.mp4","dur":10.0,"seed":9110,
     "prompt":("Cinematic video, phone screen close-up: WeChat chat interface, last message 'hao'. "
               "Typing indicator three dots appears then gone, appears again then gone. "
               "Ten seconds pass, nothing, screen dims slightly, minimalist tense silence, phone screen glow, 16:9.")},
    {"shot":"02","name":"外骨骼UI","pri":"P2","img":"13_office_01_exoskeleton_ui.png",
     "out":"EP13_SHOT-02_LTX169_exoskeleton_ui.mp4","dur":8.0,"seed":9102,
     "prompt":("Cinematic video, dual monitors showing exoskeleton wireframe rotating, heatmaps updating. "
               "Slow push-in on monitors, monitor glow on desk, coffee cup in foreground slightly out of focus. "
               "Professional tech atmosphere, subtle blue LED ambience, 16:9 widescreen.")},
    {"shot":"04","name":"2017实验室","pri":"P2","img":"13_lab_01_2017_night.png",
     "out":"EP13_SHOT-04_LTX169_lab_2017.mp4","dur":8.0,"seed":9104,
     "prompt":("Cinematic video, warm nostalgic memory, small university lab at night 2017. "
               "Steam rising from coffee mug on cluttered desk, old CRT monitor blue-green glow. "
               "Two young researchers silhouetted backlit by screens, soft warm golden haze of memory. "
               "Slow dolly left, steam curls up from coffee, 16:9 widescreen.")},
    {"shot":"05","name":"地铁群像","pri":"P2","img":"13_subway_01_rush_hour.png",
     "out":"EP13_SHOT-05_LTX169_subway_crowd.mp4","dur":8.0,"seed":9105,
     "prompt":("Cinematic video, Shanghai morning rush subway, crowded carriage everyone on phones. "
               "Sea of glowing screens, no one talks, train sways gently, tunnel lights flicker past windows. "
               "Harsh fluorescent, medium-wide slow pan, middle-aged woman with bags, student with headphones, "
               "old man dozing, subtle natural movements, 16:9 widescreen.")},
    {"shot":"12","name":"双标注UI","pri":"P3","img":"13_ui_02_double_annotation_xiaozhou.png",
     "out":"EP13_SHOT-12_LTX169_ui_double.mp4","dur":8.0,"seed":9112,
     "prompt":("Cinematic video, futuristic UI concept on monitor, split-screen annotation. "
               "Left: video frame with bounding boxes appearing. Right: text analysis, phrases highlighting. "
               "UI elements pulse, data flowing, AI annotation layers fade in/out, dark mode cyan amber accents, "
               "slow zoom toward center, 16:9 widescreen.")},
    {"shot":"09","name":"笔记本慢推","pri":"P3","img":"13_prop_01_notebook_label.png",
     "out":"EP13_SHOT-09_LTX169_notebook.mp4","dur":7.0,"seed":9109,
     "prompt":("Cinematic video, extreme close-up old lab notebook, handwritten Chinese notes yellowed pages. "
               "Chipped coffee mug beside, slow push-in toward circled annotation. "
               "Shadow of someone leaning over drifts across, warm tungsten lamp, dust motes in light beam, "
               "nostalgic, 16:9 widescreen.")},
]


def lwf(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def q(wf):
    d = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    r = urllib.request.Request(f"{COMFY}/prompt", data=d,
                               headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read()).get("prompt_id", "")


def w(pid, timeout=1200):
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
                raise RuntimeError(f"ComfyUI 出错: {json.dumps(h.get('status',{}), ensure_ascii=False)}")
        except RuntimeError:
            raise
        except Exception:
            pass
        time.sleep(5)
    raise TimeoutError(pid)


def dl(hist, out_dir):
    saved = []
    for nid, node in hist.get("outputs", {}).items():
        for key in ("gifs", "images", "audio"):
            for item in node.get(key, []):
                fn = item["filename"]; sub = item.get("subfolder", "")
                typ = item.get("type", "output")
                urllib.request.urlretrieve(
                    f"{COMFY}/view?filename={fn}&subfolder={sub}&type={typ}",
                    str(out_dir / fn))
                saved.append(fn)
    return saved


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", type=str, help="镜头编号, 逗号分隔")
    args = ap.parse_args()
    shots = ([s for s in S if s["shot"] in args.shot.split(",")]
             if args.shot else S)
    print("=" * 60)
    print(f" EP13 LTX 重做 (16:9 {W_SRC//2}x{H_SRC//2}) | 目标: "
          f"{', '.join(s['shot'] for s in shots)}")
    print("=" * 60)

    for i, s in enumerate(shots, 1):
        print(f"\n-- [{i}/{len(shots)}] SHOT-{s['shot']} [{s['pri']}]: {s['name']} ({s['dur']}s)")
        wf = lwf(WF)
        for nid, node in wf.items():
            ct = node.get("class_type", "")
            if ct == "LoadImage":
                node["inputs"]["image"] = s["img"]
            elif ct == "PrimitiveStringMultiline":
                node["inputs"]["value"] = s["prompt"]
            elif ct == "RandomNoise":
                node["inputs"]["noise_seed"] = s["seed"]
            elif ct == "SaveVideo":
                node["inputs"]["filename_prefix"] = f"video/EP13_SHOT-{s['shot']}_LTX169"
        wf["320:312"]["inputs"]["value"] = W_SRC
        wf["320:299"]["inputs"]["value"] = H_SRC
        wf["320:301"]["inputs"]["value"] = int(round(s["dur"]))
        try:
            pid = q(wf)
            print(f"    submitted {pid[:8]}... waiting (4-15 min)...")
            t0 = time.time(); hist = w(pid); print(f"    done in {int(time.time()-t0)}s")
            saved = dl(hist, OUT)
            for fn in saved:
                mb = (OUT / fn).stat().st_size / (1024*1024)
                print(f"    ok {fn} ({mb:.1f}MB)")
            if len(saved) == 1:
                src = OUT / saved[0]; dst = OUT / s["out"]
                if src.suffix != dst.suffix:
                    dst = dst.with_suffix(src.suffix)
                if src != dst:
                    src.rename(dst); print(f"    -> {dst.name}")
        except Exception as e:
            print(f"    ERR {e}")

    print(f"\n{'='*60}\n Done:", OUT)


if __name__ == "__main__":
    main()

