"""Probe the correct GitHub URL for ComfyUI blueprints."""
import urllib.request
import json

urls = [
    "https://api.github.com/repos/comfyanonymous/ComfyUI/contents/web/blueprints",
    "https://api.github.com/repos/Comfy-Org/ComfyUI/contents/web/blueprints",
    "https://api.github.com/repos/Comfy-Org/ComfyUI_frontend/contents/src/blueprints/built-in",
    "https://api.github.com/repos/Comfy-Org/ComfyUI_frontend/contents/public/blueprints",
]

for url in urls:
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        if isinstance(data, list):
            print(f"FOUND: {url} ({len(data)} entries)")
            for f in data[:10]:
                print(f"  {f['name']}")
        else:
            print(f"{url}: {data.get('message', 'not a list')}")
    except Exception as e:
        print(f"{url}: {e}")