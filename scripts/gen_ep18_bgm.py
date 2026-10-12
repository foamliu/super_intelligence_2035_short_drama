#!/usr/bin/env python3
"""第18集《暖阳》 BGM 生成脚本（固化 · S3 放量 · ACE-Step 1.5 文生音频）。

作用：为第 18 集生成**跨镜 BGM**（后期整体铺底），遵循 `ASSETS/配乐提示词规格.md`
的「Caption（氛围总谱）+ Lyrics（分镜脚本）双管齐下」法则。

- 情绪基调（SCENES/18_暖阳.md）：夜晚城市冷蓝与车内暖橙交织；低饱和写实电影质感；
  核心主题 = 明知「被在乎」是算法算出来的，仍选择不去知道——克制、孤独、轻微窒息。
- 🚫 本线禁用 TTS（任务书 §4.5 / 运维指令区 ⑦）：人声已由 H3 随视频生成，
  **BGM 全部为纯器乐**（lyrics 只写结构标签，不写可唱词句）。
- 电平纪律（§4.5）：BGM 与成片音轨直接相加必爆 ⇒ 合成时 BGM 降 level + 侧链闪避 +
  总线 alimiter 守 −1 dBFS（母带 ≈ −23 LUFS），见 synth/mix 步骤，本脚本只负责**生成素材**。

用法:
  python scripts/gen_ep18_bgm.py --dry-run      # 仅打印计划（核曲目/时长/seed）
  python scripts/gen_ep18_bgm.py --track 01     # 只跑某曲
  python scripts/gen_ep18_bgm.py --skip-existing  # 跳过已出片的曲目（续跑用）

参数纪律：ACE-Step 用工作流默认（steps=8 / cfg=1.0 / Turbo 配方）；时长 45–60s；
固定 seed 可复现。
"""
import argparse
import json
import time
import urllib.request
import uuid
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "workflows" / "ACE-Step 1.5 文生音频.json"
OUT = ROOT / "OUTPUT" / "18_暖阳" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

# ── 曲目（3 首 · 跨镜 BGM · 纯器乐）────────────────────
# 01 倾诉/陪伴主题（大提琴）—— 贯穿「倾诉 / 陪伴 / 依赖」段落（配乐规格·示例2）
# 02 数据流主题（冷电子）—— 切入「数据流 / 系统」段落（配乐规格·示例4 范式）
# 03 尾声主题（钢琴）—— 尾声「选择 / 按下购买」收束
BGMS = [
    {
        "file": "18_bgm_01_cello_imagination.mp3",
        "tags": (
            "minimalist cello, long bow strokes, deeply intimate and heartbreaking, "
            "single notes that hang in the air then fade, no accompaniment, no rhythm "
            "section, quiet grief, sparse, slow tempo 50 BPM, minor key, cinematic, "
            "ambient reverb, restrained, cold night loneliness"
        ),
        "lyrics": (
            "[Intro - Cello, single low note, long bow]\n"
            "[Verse 1 - Sparse, one note every few seconds]\n"
            "(The note sustains, then fades)\n"
            "[Verse 2 - Slightly higher, still single notes]\n"
            "(Each note shorter, like catching breath)\n"
            "[Bridge - Silence, almost nothing]\n"
            "[Outro - Return to low note, fade out]"
        ),
        "seconds": 60, "seed": 4801,
    },
    {
        "file": "18_bgm_02_datastream_electronic.mp3",
        "tags": (
            "minimal electronic ambient, cool blue tones, subtle pulses mimicking data "
            "streams, quiet electronic texture that builds slowly, invisible wrongness, "
            "detached and analytical, no melody, 45 BPM, cold cyan glow, cinematic sound design"
        ),
        "lyrics": (
            "[Intro - Subtle electronic pulse, very quiet]\n"
            "[Verse 1 - Single synth tone, sustained]\n"
            "[Verse 2 - Second layer enters, slightly dissonant]\n"
            "(The two tones don't quite align)\n"
            "[Bridge - Almost silence, just pulse]\n"
            "[Outro - All tones fade, pulse continues]"
        ),
        "seconds": 45, "seed": 4802,
    },
    {
        "file": "18_bgm_03_finale_piano.mp3",
        "tags": (
            "solo piano, contemplative, sparse notes, minor key, warm but restrained, "
            "late-night isolation, slow tempo 55 BPM, pauses between notes, cinematic, "
            "ambient reverb, gentle, a decision made in silence"
        ),
        "lyrics": (
            "[Intro - Solo piano, single note]\n"
            "[Verse 1 - Sparse arpeggio, slowly]\n"
            "[Verse 2 - Same pace, slightly fuller]\n"
            "[Bridge - Single low note, held]\n"
            "[Outro - Last note sustains, fade out]"
        ),
        "seconds": 45, "seed": 4803,
    },
]


# ── API Helpers（同 gen_ep13_bgm.py 范式）──────────────
def load_wf(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")


def wait(pid, timeout=600):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = urllib.request.urlopen(f"{COMFY}/history/{pid}", timeout=10)
            d = json.loads(r.read())
            h = d.get(pid, {})
            st = h.get("status", {}).get("status_str", "")
            if st == "success" and h.get("outputs"):
                return h
            if st == "error":
                raise RuntimeError(f"ComfyUI error: {h.get('status', {}).get('messages', '')}")
        except RuntimeError:
            raise
        except Exception:
            pass
        time.sleep(3)
    raise TimeoutError(f"Timeout: {pid}")


def get_outputs(hist):
    for _nid, node in hist.get("outputs", {}).items():
        for aud in node.get("audio", []):
            yield aud


def download(item, dst):
    fn = item["filename"]
    sub = item.get("subfolder", "")
    typ = item.get("type", "output")
    url = f"{COMFY}/view?filename={fn}&subfolder={sub}&type={typ}"
    urllib.request.urlretrieve(url, str(dst))
    return True


def build_workflow(bgm, idx):
    wf = load_wf(WF)
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "TextEncodeAceStepAudio1.5":
            node["inputs"]["tags"] = bgm["tags"]
            node["inputs"]["lyrics"] = bgm["lyrics"]
        elif ct == "PrimitiveFloat":
            node["inputs"]["value"] = bgm["seconds"]
        elif ct == "KSampler":
            node["inputs"]["seed"] = bgm["seed"]
        elif ct == "SaveAudioAdvanced":
            node["inputs"]["filename_prefix"] = f"audio/ep18_bgm_{idx:02d}"
    return wf


def run_one(idx, bgm):
    print(f"\n── BGM-{idx:02d}: {bgm['file']} ({bgm['seconds']}s · seed={bgm['seed']})")
    wf = build_workflow(bgm, idx)
    pid = queue(wf)
    print(f"    submitted {pid[:8]}... waiting...")
    t0 = time.time()
    hist = wait(pid)
    items = list(get_outputs(hist))
    if not items:
        print("    ❌ 无音频输出")
        return False
    dst = OUT / bgm["file"]
    download(items[0], dst)
    kb = dst.stat().st_size // 1024
    print(f"    ✅ {dst.name} ({kb}KB · {int(time.time() - t0)}s)")
    return True


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》BGM 生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--track", type=str, help="按曲目号筛选（01/02/03）")
    ap.add_argument("--skip-existing", action="store_true", help="跳过已出片的曲目")
    args = ap.parse_args()

    sel = BGMS
    if args.track:
        idx = int(args.track)
        sel = [b for b in BGMS if BGMS.index(b) + 1 == idx]
    if args.skip_existing:
        sel = [b for b in sel if not (OUT / b["file"]).exists()]

    print("=" * 66)
    print(f" EP18《暖阳》BGM  |  {len(sel)}/{len(BGMS)} 曲  |  输出: {OUT}")
    print("=" * 66)
    for i, b in enumerate(sel, 1):
        print(f"  - {b['file']}  {b['seconds']}s  seed={b['seed']}")
    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    ok = 0
    for b in sel:
        idx = BGMS.index(b) + 1
        try:
            if run_one(idx, b):
                ok += 1
        except Exception as e:
            print(f"    ❌ {e}")
        time.sleep(2)
    print(f"\n{'=' * 66}\n BGM 完成: {ok}/{len(sel)}  输出: {OUT}")


if __name__ == "__main__":
    main()
