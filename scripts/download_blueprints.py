"""Download P0 ComfyUI blueprints from GitHub."""
import urllib.request
import os
import json

BASE = "https://raw.githubusercontent.com/comfyanonymous/ComfyUI/refs/heads/master/web/blueprints"
OUT = os.path.join(os.path.dirname(__file__), "..", "workflows")

# GitHub raw URLs: spaces must be %20-encoded, but the filename in repo uses literal spaces
TARGETS = [
    "Remove%20Background%20(BiRefNet).json",
    "Image%20Upscale(Z-image-Turbo).json",
    "Merge%20Videos.json",
    "Color%20Balance.json",
    "Color%20Curves.json",
]

os.makedirs(OUT, exist_ok=True)

for fn_encoded in TARGETS:
    url = f"{BASE}/{fn_encoded}"
    # decode for local filename
    local_name = urllib.request.unquote(fn_encoded)
    path = os.path.join(OUT, local_name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        json.loads(data)  # validate
        with open(path, "wb") as f:
            f.write(data)
        print(f"OK: {local_name}")
    except Exception as e:
        print(f"FAIL: {local_name} — {e}")