#!/usr/bin/env python3
"""EP13 LTX169 恢复下载：从 ComfyUI history 批量下载所有已生成的镜头。

批量重做脚本的 wait() 因队列延迟超时，导致部分镜头已生成但未下载。
本脚本扫描 ComfyUI /history，找出文件名含 "LTX169" 的已完成任务并下载。

用法:
  python scripts/recover_ep13_ltx169.py
"""
import json, urllib.request, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "OUTPUT" / "13_外骨骼" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

# shot -> 期望输出名（按 LTX169 前缀推断）
SHOT_OUT = {
    "07": "EP13_SHOT-07_LTX169_virtual_face.mp4",
    "08": "EP13_SHOT-08_LTX169_render_vs_real.mp4",
    "10": "EP13_SHOT-10_LTX169_wechat_silence.mp4",
    "02": "EP13_SHOT-02_LTX169_exoskeleton_ui.mp4",
    "04": "EP13_SHOT-04_LTX169_lab_2017.mp4",
    "05": "EP13_SHOT-05_LTX169_subway_crowd.mp4",
    "12": "EP13_SHOT-12_LTX169_ui_double.mp4",
    "09": "EP13_SHOT-09_LTX169_notebook.mp4",
}


def get_history(max_items=200):
    r = urllib.request.urlopen(f"{COMFY}/history?max_items={max_items}", timeout=30)
    return json.loads(r.read())


def download(hist, shot, out_name):
    for pid, entry in hist.items():
        if entry.get("status", {}).get("status_str") != "success":
            continue
        # 找 SaveVideo 输出
        for nid, node in entry.get("outputs", {}).items():
            for key in ("gifs", "images", "audio"):
                for item in node.get(key, []):
                    fn = item["filename"]
                    if f"SHOT-{shot}_LTX169" in fn:
                        sub = item.get("subfolder", "")
                        typ = item.get("type", "output")
                        url = f"{COMFY}/view?filename={fn}&subfolder={sub}&type={typ}"
                        dst = OUT / out_name
                        urllib.request.urlretrieve(url, str(dst))
                        mb = dst.stat().st_size / (1024*1024)
                        print(f"    [OK] {out_name} ({mb:.1f}MB) <- {fn}")
                        return True
    return False


def main():
    print("=" * 60)
    print(" EP13 LTX169 恢复下载")
    print("=" * 60)
    hist = get_history()
    print(f" history 任务数: {len(hist)}")

    for shot, out_name in SHOT_OUT.items():
        if (OUT / out_name).exists():
            print(f"  [已有] {out_name}")
            continue
        print(f"  尝试下载 SHOT-{shot} -> {out_name}")
        if not download(hist, shot, out_name):
            print(f"  [未找到] SHOT-{shot} 未完成或未生成")

    print("\n完成")


if __name__ == "__main__":
    main()
