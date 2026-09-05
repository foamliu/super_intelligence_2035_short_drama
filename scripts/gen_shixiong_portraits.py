#!/usr/bin/env python3
"""Generate 3 师兄 portraits via ComfyUI Z-Image-Turbo API"""
import json, time, uuid, urllib.request
from pathlib import Path

COMFYUI = "http://127.0.0.1:8188"
WF = Path("E:/code/super_intelligence_2035_short_drama/workflows/Z-Image-Turbo 文生图.json")
OUT = Path("E:/code/super_intelligence_2035_short_drama/OUTPUT/13_外骨骼/frames")
OUT.mkdir(parents=True, exist_ok=True)

NEG = ("smile, laughing, happy, cheerful, young, handsome, energetic, "
       "suit, tie, CEO, luxury, warm lighting, golden hour, "
       "anime, cartoon, illustration, 3D render, oversaturated, plastic skin")

P1 = ("31-year-old Chinese male, thin and tall, slightly hunched shoulders, "
      "black-framed glasses, tousled short dark hair, deep-set tired eyes with dark circles, "
      "holding white ceramic coffee mug with company logo, dark grey hoodie over black t-shirt, "
      "cold white fluorescent office lighting from above, sharp shadows, "
      "slight micro-expression at corner of mouth - not smiling, just knowing, "
      "visible pores, eye lines, doesn't sleep enough, "
      "semi-realistic Chinese ink wash aesthetic, ink bleeding from edges, "
      "cinematic photorealistic, 8K detail, shallow depth of field")

P2 = ("Profile close-up, 31-year-old Chinese male, black-framed glasses reflecting blue screen glow, "
      "raising white ceramic coffee mug to lips, thin face, visible pores, eye lines, dark circles, "
      "tousled short dark hair, dark grey hoodie collar, cold white and blue screen light on face, "
      "subtle micro-expression, semi-realistic ink wash style, ink bleeding from edges, "
      "cinematic, 8K detail, shallow depth of field")

P3 = ("27-year-old Chinese male, younger version of same person, black-framed glasses, short dark hair, "
      "faded grey t-shirt, tired from three-day coding sprint but no dark circles yet, "
      "sitting at old LCD monitor with warm blue CRT glow, coffee mug on desk with steam, "
      "2017-era Chinese university lab, dated tech, whiteboard with formulas in background, "
      "warm tungsten desk lamp + blue screen light on face, semi-realistic ink wash style, "
      "nostalgic warm tones, ink bleeding from edges, cinematic, 8K detail")

IMAGES = [
    ("13_shixiong_01_coffee.png", P1, 1920, 1920, 200),
    ("13_shixiong_02_coffee_side.png", P2, 1920, 1920, 201),
    ("13_shixiong_03_lab2017.png", P3, 1920, 1920, 202),
]

def load_wf(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFYUI}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")

def wait(pid, timeout=600):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = urllib.request.urlopen(f"{COMFYUI}/history/{pid}", timeout=10)
            d = json.loads(r.read())
            if pid in d:
                return d[pid]
        except: pass
        time.sleep(2)
    raise TimeoutError(f"Timeout: {pid}")

def outputs(hist):
    for nid, node in hist.get("outputs", {}).items():
        for img in node.get("images", []):
            yield img

def download(img, dst):
    fn = img["filename"]; sub = img.get("subfolder", ""); typ = img.get("type", "output")
    url = f"{COMFYUI}/view?filename={fn}&subfolder={sub}&type={typ}"
    try:
        urllib.request.urlretrieve(url, str(dst))
        return True
    except Exception as e:
        print(f"    download failed: {e}")
        return False

print("=" * 50)
print(" 师兄 3 Portraits - Z-Image-Turbo")
print("=" * 50)

ok = 0
for i, (fn, prompt, w, h, seed) in enumerate(IMAGES, 1):
    print(f"\n[{i}/3] {fn}  ({w}x{h}, seed={seed})")
    wf = load_wf(WF)
    for nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "CLIPTextEncode":
            node["inputs"]["text"] = f"{prompt}\n\nDo NOT include: {NEG}"
        elif ct == "EmptySD3LatentImage":
            node["inputs"]["width"] = w; node["inputs"]["height"] = h
        elif ct == "KSampler":
            node["inputs"]["seed"] = seed

    try:
        pid = queue(wf)
        print(f"    submitted {pid}, waiting...")
        hist = wait(pid)
        out_imgs = list(outputs(hist))
        if out_imgs:
            dst = OUT / fn
            if download(out_imgs[0], dst):
                kb = dst.stat().st_size // 1024
                print(f"    OK: {dst} ({kb}KB)")
                ok += 1
            else:
                print(f"    FAIL: download")
        else:
            print(f"    ERROR: no output")
    except Exception as e:
        print(f"    ERROR: {e}")

    time.sleep(1)

print(f"\n{'='*50}")
print(f"Done: {ok}/3  saved to {OUT}")
