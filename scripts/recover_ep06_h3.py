#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第06集《情绪》 H3 出片回收脚本（把 ComfyUI /history 里已完成的镜头拉回仓库）。

背景：`gen_ep06_h3_r2v.py` / `gen_ep06_h3_t2v.py` 默认是「只提交」（不 --wait），
视频先落到 ComfyUI 自身 output 目录；本脚本轮询 `/history`，把文件名前缀为
`EP06_SHOT-` 的成品 mp4 下载到 `OUTPUT/06_情绪/videos/`，并打印 29 个有角色镜 +
25 个无角色镜的「已到 / 缺失」清单，供持续监控与续跑。

用法:
  python scripts/recover_ep06_h3.py            # 下载已完成的 + 打印清单
  python scripts/recover_ep06_h3.py --loop 300 # 每 300s 轮询一次，直到 54 镜齐
"""
import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "OUTPUT" / "06_情绪" / "videos"
OUT.mkdir(parents=True, exist_ok=True)
PREFIX = "EP06_SHOT-"

# 期望镜头号（从两个固化脚本的 SHOTS 导入，避免手抄漂移）
_R2V_SHOTS = None
_T2V_SHOTS = None


def _load_expected():
    global _R2V_SHOTS, _T2V_SHOTS
    if _R2V_SHOTS is not None:
        return
    import importlib.util
    r2v = ROOT / "scripts" / "gen_ep06_h3_r2v.py"
    t2v = ROOT / "scripts" / "gen_ep06_h3_t2v.py"
    _R2V_SHOTS = set()
    _T2V_SHOTS = set()
    for path, bucket in ((r2v, _R2V_SHOTS), (t2v, _T2V_SHOTS)):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for s in mod.SHOTS:
            bucket.add(s["shot"])


def _history():
    with urllib.request.urlopen(f"{COMFY}/history?max_items=200", timeout=60) as r:
        return json.loads(r.read())


def _download(filename, subfolder, typ, dest):
    qs = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": typ})
    with urllib.request.urlopen(f"{COMFY}/view?{qs}", timeout=600) as r, \
            open(dest, "wb") as f:
        f.write(r.read())
    return dest


def _parse_shot(fname):
    """EP06_SHOT-02_H3_R2V_00001.mp4 -> (shot, mode)。失败返回 (None, None)。"""
    if not fname.startswith(PREFIX) or not fname.endswith(".mp4"):
        return None, None
    parts = fname.split("_")
    # ['EP06', 'SHOT-02', 'H3', 'R2V', '00001.mp4']
    if len(parts) < 4:
        return None, None
    shot = parts[1].replace("SHOT-", "")
    mode = parts[3]  # R2V / T2V
    return shot, mode


def pull_once():
    _load_expected()
    hist = _history()
    present = {}
    for _pid, entry in hist.items():
        st = entry.get("status", {})
        if st.get("status_str") != "success" and not st.get("completed"):
            continue
        for _nid, node in entry.get("outputs", {}).items():
            if not isinstance(node, dict):
                continue
            for key in ("videos", "images", "gifs"):
                for item in node.get(key) or []:
                    if not isinstance(item, dict):
                        continue
                    fname = item.get("filename") or ""
                    shot, mode = _parse_shot(fname)
                    if shot is None:
                        continue
                    dst = OUT / fname
                    if dst.exists() and dst.stat().st_size > 0:
                        present[(shot, mode)] = dst
                        continue
                    try:
                        _download(fname, item.get("subfolder", ""), item.get("type", ""), dst)
                        present[(shot, mode)] = dst
                    except Exception as e:  # noqa: BLE001
                        print(f"  ⚠ 下载失败 {fname}: {e}")
    return present


def report(present):
    _load_expected()
    r2v_done = sorted(s for (s, m) in present if m == "R2V" and s in _R2V_SHOTS)
    t2v_done = sorted(s for (s, m) in present if m == "T2V" and s in _T2V_SHOTS)
    r2v_missing = sorted(_R2V_SHOTS - set(r2v_done))
    t2v_missing = sorted(_T2V_SHOTS - set(t2v_done))
    total_done = len(r2v_done) + len(t2v_done)
    total = len(_R2V_SHOTS) + len(_T2V_SHOTS)
    print(f"\n已回收 {total_done}/{total} 镜（R2V {len(r2v_done)}/{len(_R2V_SHOTS)} · "
          f"T2V {len(t2v_done)}/{len(_T2V_SHOTS)}）")
    if r2v_missing:
        print(f"  缺 R2V: {', '.join(r2v_missing)}")
    if t2v_missing:
        print(f"  缺 T2V: {', '.join(t2v_missing)}")
    return total_done >= total


def main():
    ap = argparse.ArgumentParser(description="第06集 H3 出片回收")
    ap.add_argument("--loop", type=int, default=0, help="轮询间隔秒（0=只跑一次）")
    args = ap.parse_args()

    while True:
        present = pull_once()
        done = report(present)
        if done:
            print("✅ 第06集 54 镜已全部回收。")
            return
        if not args.loop:
            print("（仍缺镜，稍后再跑本脚本续收）")
            return
        print(f"⏳ {args.loop}s 后再轮询…")
        time.sleep(args.loop)


if __name__ == "__main__":
    main()
