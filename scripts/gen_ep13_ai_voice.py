#!/usr/bin/env python3
"""Generate AI Exoskeleton voice lines (Serena) for Episode 13"""
import json, time, uuid, urllib.request
from pathlib import Path

COMFYUI = "http://127.0.0.1:8188"
WF = Path("E:/code/super_intelligence_2035_short_drama/workflows/Qwen3-TTS 语音合成.json")
OUT = Path("E:/code/super_intelligence_2035_short_drama/OUTPUT/13_外骨骼/audio")

LINES = [
    ("13_tts_ai_01_spine.flac", "老刘，今天你的腰椎负荷比平时高12%。建议把焊枪再抬高一些。"),
    ("13_tts_ai_02_rest.flac", "很好了。注意——下午三点左右需要休息15分钟。你的竖脊肌会在那个时间出现疲劳峰值。"),
    ("13_tts_ai_03_shrug.flac", "老刘——你的颈夹肌开始紧张。建议做一次耸肩——三秒后。"),
]

INSTRUCT = ("一位温柔但有距离感的AI女声，经设计的语音界面。"
            "语气柔和、清晰、不带感情但有关怀感。"
            "像是系统提示音+私人健康助理的结合——"
            "每一个字都经过语音合成优化，但保留自然节奏。")

OUT.mkdir(parents=True, exist_ok=True)

def load_wf(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFYUI}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")

def wait(pid, timeout=300):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = urllib.request.urlopen(f"{COMFYUI}/history/{pid}", timeout=10)
            d = json.loads(r.read())
            h = d.get(pid, {})
            st = h.get("status", {}).get("status_str", "")
            if st == "success" and h.get("outputs"):
                return h
            elif st == "error":
                raise RuntimeError(f"Failed: {h}")
        except: pass
        time.sleep(3)
    raise TimeoutError(pid)

def get_outputs(hist):
    for nid, node in hist.get("outputs", {}).items():
        for aud in node.get("audio", []):
            yield aud

def download(item, dst):
    fn = item["filename"]; sub = item.get("subfolder", "")
    typ = item.get("type", "output")
    url = f"{COMFYUI}/view?filename={fn}&subfolder={sub}&type={typ}"
    urllib.request.urlretrieve(url, str(dst))
    return True

print("=" * 50)
print(" Episode 13 AI Exoskeleton Voice - Serena")
print("=" * 50)

ok = 0
for i, (fn, text) in enumerate(LINES, 1):
    print(f"\n[{i}/{len(LINES)}] {fn}")
    print(f"    text: {text[:60]}...")

    wf = load_wf(WF)
    for nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "Qwen3CustomVoice":
            node["inputs"]["text"] = text
            node["inputs"]["speaker"] = "Serena"
            node["inputs"]["custom_speaker_name"] = ""
            node["inputs"]["instruct"] = INSTRUCT
            node["inputs"]["seed"] = 1401
        elif ct == "SaveAudioAdvanced":
            node["inputs"]["filename_prefix"] = f"audio/ep13_{fn.replace('.flac','')}"

    try:
        pid = queue(wf)
        print(f"    submitted {pid[:8]}..., waiting...")
        hist = wait(pid, timeout=300)
        items = list(get_outputs(hist))
        if items:
            dst = OUT / fn
            download(items[0], dst)
            kb = dst.stat().st_size // 1024
            print(f"    OK: {dst} ({kb}KB)")
            ok += 1
        else:
            print("    ERROR: no audio output")
    except Exception as e:
        print(f"    ERROR: {e}")
    time.sleep(2)

print(f"\n{'='*50}")
print(f" AI Voice Done: {ok}/{len(LINES)}")
