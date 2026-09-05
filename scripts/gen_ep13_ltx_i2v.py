#!/usr/bin/env python3
"""Episode 13: LTX-2.3 I2V batch — 8 shots (P0→P3)."""
import json, time, uuid, urllib.request
from pathlib import Path

COMFY = "http://127.0.0.1:8188"
WF = Path("E:/code/super_intelligence_2035_short_drama/workflows/Image to Video (LTX-2.3).json")
OUT = Path("E:/code/super_intelligence_2035_short_drama/OUTPUT/13_外骨骼/videos")
OUT.mkdir(parents=True, exist_ok=True)

S = [
    {"shot":"07","name":"虚拟脸在笑","pri":"P0","img":"13_virtual_audience_01_imaginary_face.png","out":"EP13_SHOT-07_LTX_virtual_face.mp4","dur":6.0,"seed":9007,
     "prompt":("Cinematic video, glowing translucent AI-generated audience face on dark screen. "
               "Synthetic face, pixel-level micro-expressions ripple: mouth corner curls, eye crinkles — laughing. "
               "Genuine infectious laugh. Expression shifts fluidly. Semi-transparent blue-white with pink warmth. "
               "Light particles drift. Ultra-slow push in.")},
    {"shot":"08","name":"渲染vs真实","pri":"P0","img":"13_virtual_audience_02_render_vs_real.png","out":"EP13_SHOT-08_LTX_render_vs_real.mp4","dur":8.0,"seed":9008,
     "prompt":("Cinematic video, split-screen: top half rendered AI face — synthetic, smooth. "
               "Bottom half real audience face — pores, asymmetrical smile, warmth. "
               "Two halves slowly merge at center via soft wipe. Thin glowing seam at boundary. "
               "Cold blue above, warm amber below. Seam dissolves as crossfade completes.")},
    {"shot":"10","name":"微信十秒沉默","pri":"P1","img":"13_prop_02_wechat_hao.png","out":"EP13_SHOT-10_LTX_wechat_silence.mp4","dur":10.0,"seed":9010,
     "prompt":("Cinematic video, phone screen close-up: WeChat chat interface. Last message: '好的'. "
               "Typing indicator — three dots — appears 2s then gone. Appears again 2s then gone. "
               "Ten seconds pass, nothing. Screen dims slightly. Minimalist, tense silence. Phone screen glow.")},
    {"shot":"02","name":"外骨骼UI","pri":"P2","img":"13_office_01_exoskeleton_ui.png","out":"EP13_SHOT-02_LTX_exoskeleton_ui.mp4","dur":8.0,"seed":9002,
     "prompt":("Cinematic video, dual monitors showing exoskeleton wireframe rotating, heatmaps updating. "
               "Slow push-in on monitors. Monitor glow on desk. Coffee cup in foreground, slightly out of focus. "
               "Professional tech atmosphere, subtle blue LED ambience.")},
    {"shot":"04","name":"2017实验室","pri":"P2","img":"13_lab_01_2017_night.png","out":"EP13_SHOT-04_LTX_lab_2017.mp4","dur":8.0,"seed":9004,
     "prompt":("Cinematic video, warm nostalgic memory. Small university lab at night 2017. "
               "Steam rising from coffee mug on cluttered desk. Old CRT monitor blue-green glow. "
               "Two young researchers silhouetted, backlit by screens. Soft warm filter — golden haze of memory. "
               "Slow dolly left. Steam curls up from coffee.")},
    {"shot":"05","name":"地铁群像","pri":"P2","img":"13_subway_01_rush_hour.png","out":"EP13_SHOT-05_LTX_subway_crowd.mp4","dur":8.0,"seed":9005,
     "prompt":("Cinematic video, Shanghai morning rush subway. Crowded carriage, everyone on phones — sea of glowing screens. "
               "No one talks. Train sways gently. Tunnel lights flicker past windows. Harsh fluorescent. "
               "Medium-wide, slow pan across carriage. Middle-aged woman with bags, student with headphones, "
               "old man dozing — all subtle natural movements.")},
    {"shot":"12","name":"双标注UI","pri":"P3","img":"13_ui_02_double_annotation_xiaozhou.png","out":"EP13_SHOT-12_LTX_ui_double.mp4","dur":8.0,"seed":9012,
     "prompt":("Cinematic video, futuristic UI concept on monitor. Split-screen annotation: left — video frame with "
               "bounding boxes appearing. Right — text analysis, phrases highlighting. "
               "UI elements pulse — data flowing. AI annotation layers fade in/out. "
               "Dark mode, cyan + amber accents. Slow zoom toward center.")},
    {"shot":"09","name":"笔记本慢推","pri":"P3","img":"13_prop_01_notebook_label.png","out":"EP13_SHOT-09_LTX_notebook.mp4","dur":7.0,"seed":9009,
     "prompt":("Cinematic video, extreme close-up old lab notebook. Handwritten Chinese notes, yellowed pages. "
               "Chipped coffee mug beside. Slow push-in toward circled annotation. "
               "Shadow of someone leaning over drifts across. Warm tungsten lamp. Dust motes in light beam. Nostalgic.")},
]

# ── API ──
def lwf(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def q(wf):
    d = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    r = urllib.request.Request(f"{COMFY}/prompt", data=d,
                               headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read()).get("prompt_id", "")
def w(pid, timeout=600):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = urllib.request.urlopen(f"{COMFY}/history/{pid}", timeout=10)
            d = json.loads(r.read())
            h = d.get(pid, {})
            if h.get("status", {}).get("status_str") == "success" and h.get("outputs"):
                return h
        except: pass
        time.sleep(5)
    raise TimeoutError(pid)
def dl(hist, out_dir):
    saved = []
    for nid, node in hist.get("outputs", {}).items():
        for key in ("gifs", "images", "audio"):
            for item in node.get(key, []):
                fn = item["filename"]; sub = item.get("subfolder", "")
                typ = item.get("type", "output")
                urllib.request.urlretrieve(f"{COMFY}/view?filename={fn}&subfolder={sub}&type={typ}",
                                           str(out_dir / fn))
                saved.append(fn)
    return saved

# ── Main ──
print("=" * 60)
print(" EP13 I2V · LTX-2.3  |  Output:", OUT)
print("=" * 60)
for i, s in enumerate(S, 1):
    sid, name, prio = s["shot"], s["name"], s["pri"]
    print(f"\n-- [{i}/{len(S)}] SHOT-{sid} [{prio}]: {name} ({s['dur']}s)")
    wf = lwf(WF)
    for nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "LoadImage": node["inputs"]["image"] = s["img"]
        elif ct in ("LTXVImgToVideo", "LTXV"): node["inputs"]["prompt"] = s["prompt"]
        elif ct == "PrimitiveFloat": node["inputs"]["value"] = s["dur"]
        elif ct in ("RandomNoise", "KSampler"): node["inputs"]["noise_seed"] = s["seed"]
        elif ct == "SaveVideo": node["inputs"]["filename_prefix"] = f"video/EP13_SHOT-{sid}_LTX"
    try:
        pid = q(wf)
        print(f"    submitted {pid[:8]}... waiting (4-10 min)...")
        t0 = time.time(); hist = w(pid); print(f"    done in {int(time.time()-t0)}s")
        saved = dl(hist, OUT)
        for fn in saved:
            mb = (OUT / fn).stat().st_size / (1024*1024)
            print(f"    ok {fn} ({mb:.1f}MB)")
        if len(saved) == 1:
            src = OUT / saved[0]; dst = OUT / s["out"]
            if src.suffix != dst.suffix: dst = dst.with_suffix(src.suffix)
            if src != dst: src.rename(dst); print(f"    -> {dst.name}")
    except Exception as e: print(f"    ERR {e}")
print(f"\n{'='*60}\n Done:", OUT)
