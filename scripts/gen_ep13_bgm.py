#!/usr/bin/env python3
"""Episode 13 BGM: ACE-Step 1.5 audio generation"""
import json, time, uuid, urllib.request
from pathlib import Path

COMFYUI = "http://127.0.0.1:8188"
WF = Path("E:/code/super_intelligence_2035_short_drama/workflows/ACE-Step 1.5 文生音频.json")
OUT = Path("E:/code/super_intelligence_2035_short_drama/OUTPUT/13_外骨骼/audio")
OUT.mkdir(parents=True, exist_ok=True)

BGMS = [
    {
        "file": "13_bgm_01_backstage_piano.mp3",
        "tags": "solo piano, contemplative, backstage quiet, sparse notes, "
                "empty comedy club after hours, amber light, slow tempo 60 BPM, "
                "minor key, cinematic, atmospheric, reverb tails",
        "lyrics": "",
        "seconds": 60, "seed": 4001,
    },
    {
        "file": "13_bgm_02_office_drone.mp3",
        "tags": "industrial ambient, low drone, cold fluorescent light, "
                "server room hum, subtle electronic texture, "
                "neutral and detached, no melody, sustained tones, "
                "sound design, atmospheric, 40Hz sub bass",
        "lyrics": "",
        "seconds": 60, "seed": 4002,
    },
    {
        "file": "13_bgm_03_lab_memory.mp3",
        "tags": "solo piano, nostalgic, memory fading, "
                "2017-era warmth, CRT blue glow, single low melody, "
                "very slow 50 BPM, pauses between notes, "
                "cinematic, ambient reverb, warm tones, "
                "dust floating in afternoon light",
        "lyrics": "",
        "seconds": 45, "seed": 4003,
    },
]

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
                raise RuntimeError(f"Prompt failed: {h}")
        except: pass
        time.sleep(2)
    raise TimeoutError(f"Timeout: {pid}")

def get_outputs(hist):
    for nid, node in hist.get("outputs", {}).items():
        for aud in node.get("audio", []):
            yield aud

def download(item, dst):
    fn = item["filename"]; sub = item.get("subfolder", "")
    typ = item.get("type", "output")
    url = f"{COMFYUI}/view?filename={fn}&subfolder={sub}&type={typ}"
    try:
        urllib.request.urlretrieve(url, str(dst))
        return True
    except Exception as e:
        print(f"    download failed: {e}")
        return False

print("=" * 50)
print(" Episode 13 BGM - ACE-Step 1.5")
print("=" * 50)

ok = 0
for i, bgm in enumerate(BGMS, 1):
    print(f"\n[{i}/{len(BGMS)}] {bgm['file']}")
    print(f"    tags: {bgm['tags'][:100]}...")
    print(f"    duration: {bgm['seconds']}s | seed: {bgm['seed']}")

    wf = load_wf(WF)
    for nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "TextEncodeAceStepAudio1.5":
            node["inputs"]["tags"] = bgm["tags"]
            node["inputs"]["lyrics"] = bgm["lyrics"]
        elif ct == "PrimitiveFloat":
            node["inputs"]["value"] = bgm["seconds"]
        elif ct == "KSampler":
            node["inputs"]["seed"] = bgm["seed"]
        elif ct == "SaveAudioAdvanced":
            node["inputs"]["filename_prefix"] = f"audio/ep13_bgm_{i:02d}"

    try:
        pid = queue(wf)
        print(f"    submitted {pid[:8]}..., waiting...")
        hist = wait(pid, timeout=300)
        items = list(get_outputs(hist))
        if items:
            dst = OUT / bgm["file"]
            if download(items[0], dst):
                kb = dst.stat().st_size // 1024
                print(f"    OK: {dst} ({kb}KB)")
                ok += 1
            else:
                print(f"    FAIL: download")
        else:
            print(f"    ERROR: no audio output")
    except Exception as e:
        print(f"    ERROR: {e}")

    time.sleep(2)

print(f"\n{'='*50}")
print(f" BGM Done: {ok}/{len(BGMS)}")
print(f" Output: {OUT}")
