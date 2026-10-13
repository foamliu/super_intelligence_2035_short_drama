#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""程序拼版合影参考图（R2V 多人镜专用 · 🚫 不走 image_edit）。

规则（运维指令区 ① · §4.2）：画面该出现几人，参考图就须含几张脸；
≥2 人的合影**必须程序拼版**（本脚本），严禁经 `image_edit_longcat` 转
（会漂脸 → 角色一致性崩）。

用法:
  python scripts/make_group_composite.py 08_莎拉·赵/主定妆照.png 师兄/主定妆照.png \
      ASSETS/CHARACTERS/_group/sarah_shixiong_hero_v01.png

默认：居中裁到 4:5 竖幅 → 等分左右两格拼到 16:9 画布（1920×1080）。
"""
import argparse
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def _center_crop_to_ratio(im, ratio):
    """居中裁成宽:高 = ratio 的竖幅，返回 (new_w, new_h)。"""
    w, h = im.size
    target_ratio = ratio  # width/height
    cur = w / h
    if cur > target_ratio:
        new_w = int(h * target_ratio)
        x = (w - new_w) // 2
        return im.crop((x, 0, x + new_w, h))
    else:
        new_h = int(w / target_ratio)
        y = (h - new_h) // 2
        return im.crop((0, y, w, y + new_h))


def compose(src_a, src_b, out, canvas=(1920, 1080), crop_ratio=0.8):
    """把 A、B 两张定妆照居中裁成 crop_ratio 竖幅后左右拼到 canvas 上。"""
    cw, ch = canvas
    slot_w, slot_h = cw // 2, ch
    canvas_im = Image.new("RGB", canvas, (18, 18, 18))
    for i, src in enumerate((src_a, src_b)):
        im = Image.open(src).convert("RGB")
        im = _center_crop_to_ratio(im, crop_ratio)
        im.thumbnail((slot_w, slot_h), Image.LANCZOS)
        x = i * slot_w + (slot_w - im.width) // 2
        y = (slot_h - im.height) // 2
        canvas_im.paste(im, (x, y))
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas_im.save(out, "PNG")
    return out


def main():
    ap = argparse.ArgumentParser(description="程序拼版合影参考图")
    ap.add_argument("src_a")
    ap.add_argument("src_b")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    args = ap.parse_args()

    a = ROOT / args.src_a
    b = ROOT / args.src_b
    if not a.exists() or not b.exists():
        raise SystemExit(f"源图缺失：{a} 或 {b}")
    out = compose(a, b, ROOT / args.out, canvas=(args.width, args.height))
    print(f"✅ 合影拼版完成 → {out}  {Image.open(out).size}")


if __name__ == "__main__":
    sys.exit(main())
