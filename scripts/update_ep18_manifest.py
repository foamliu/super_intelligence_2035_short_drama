#!/usr/bin/env python3
"""第18集《暖阳》 manifest.json 更新工具（固化）。

作用：扫描 `OUTPUT/18_暖阳/videos/*.mp4`，按文件名解析镜号，用 ffprobe 实测
时长/分辨率，回写 `manifest.json` 的 `verified` 列表。`dur_req_s` / `seed` /
镜头名与 `gen_ep18_h3_i2v.py` / `gen_ep18_h3_t2v.py` 的 SHOTS 对齐。

用法:
  python scripts/update_ep18_manifest.py --dry-run   # 仅打印将写入的列表，不改文件
  python scripts/update_ep18_manifest.py             # 实际回写 manifest.json
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "OUTPUT" / "18_暖阳" / "videos"
MANIFEST = OUT / "manifest.json"

# 复用两个生成脚本的 SHOTS（导入无副作用，仅定义常量 + mkdir）
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_ep18_h3_i2v import SHOTS as I2V_SHOTS  # noqa: E402
from gen_ep18_h3_t2v import SHOTS as T2V_SHOTS  # noqa: E402

ALL = {s["shot"]: s for s in I2V_SHOTS + T2V_SHOTS}

FILE_RE = re.compile(r"^EP18_SHOT-(\d+)_H3(?:_T2V)?_\d+_\.mp4$")


def probe(path: Path):
    """ffprobe 实测时长（秒）与分辨率。"""
    r = subprocess.run(
        ["ffprobe", "-v", "error",
         "-select_streams", "v:0",
         "-show_entries", "stream=width,height:format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    data = json.loads(r.stdout)
    dur = float(data["format"]["duration"])
    s = data["streams"][0]
    return dur, f"{s['width']}x{s['height']}"


def scan() -> list:
    entries = []
    missing = []
    for mp4 in sorted(OUT.glob("*.mp4")):
        m = FILE_RE.match(mp4.name)
        if not m:
            print(f"  [跳过] 非镜号命名: {mp4.name}")
            continue
        shot = f"{int(m.group(1)):02d}"
        meta = ALL.get(shot)
        if meta is None:
            print(f"  [跳过] 无分镜定义: {mp4.name}")
            continue
        dur, res = probe(mp4)
        entries.append({
            "shot": shot,
            "file": mp4.name,
            "seed": meta["seed"],
            "dur_req_s": meta["dur"],
            "dur_actual_s": round(dur, 3),
            "resolution": res,
            "codec": "h264+aac",
            "bytes": mp4.stat().st_size,
        })
    entries.sort(key=lambda e: int(e["shot"]))
    return entries, missing


def main():
    ap = argparse.ArgumentParser(description="更新第18集 manifest.json")
    ap.add_argument("--dry-run", action="store_true", help="仅打印，不回写")
    args = ap.parse_args()

    entries, _ = scan()
    print(f"共发现 {len(entries)} 个成片 mp4：")
    for e in entries:
        print(f"  SHOT-{e['shot']}  {e['file']}  dur={e['dur_actual_s']}s  {e['resolution']}  {e['bytes']}B")

    old = {}
    if MANIFEST.exists():
        old = json.loads(MANIFEST.read_text(encoding="utf-8"))

    new_doc = {
        "episode": old.get("episode", "18_暖阳"),
        "pipeline": old.get("pipeline", ""),
        "generated_at": old.get("generated_at", ""),
        "verified": entries,
        "verified_count": len(entries),
        "notes": old.get("notes", ""),
    }

    if args.dry_run:
        print(f"\n[Dry-run] 未回写。verified_count 将为 {len(entries)}。")
        return

    MANIFEST.write_text(
        json.dumps(new_doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\n✅ 已回写 {MANIFEST}（verified_count={len(entries)}）")


if __name__ == "__main__":
    main()
