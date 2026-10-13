#!/usr/bin/env python3
"""第13集《外骨骼》 Minimax H3 I2V 分镜视频生成脚本（固化 · S3 重做 · 去 TTS）。

作用：把第 13 集「分镜帧（OUTPUT/13_外骨骼/frames/）→ H3 I2V 视频片段」固化成
可复用、可续跑、可审计的脚本。台词/人声**随 H3 一起生成**（写进 prompt 的 `Audio:`，
🚫 本线禁用 TTS，见任务书 §4.5 / 运维指令区 ⑦）。

- 分镜权威：`SCENES/13_外骨骼.md` 的 `## 逐镜表`（7 列）
- 帧权威：`OUTPUT/13_外骨骼/frames/`（14 帧，`generate_ep13_t2i.py` 产出）
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep13_h3_i2v.py --dry-run             # 仅打印计划
  python scripts/gen_ep13_h3_i2v.py --limit 4             # 只跑前 N 镜
  python scripts/gen_ep13_h3_i2v.py --shot 01             # 只跑某镜（按镜号）
  python scripts/gen_ep13_h3_i2v.py --skip-existing       # 跳过已出片镜（续跑）
  python scripts/gen_ep13_h3_i2v.py                       # 跑本批全部镜头

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（→1056×608；0.92/720p 必 OOM；要 1080p 事后 SeedVR2 超分）
  - steps=4（本批全部为静态/单人/对话/慢推，无环境剧变镜）
  - 台词长度须匹配镜头时长（`17k+5` 帧量化：4s→4.46 / 5s→5.17 / 6s→6.58）
  - 无台词镜只写「正向音景」（不含可读词句、不用否定式）
  - 🚫 禁写元信息 / 对模型说的话 / 镜头编号指代（会渲染成画面字幕）
"""
import argparse
import json
import shutil
import time
import urllib.request
import uuid
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "workflows" / "video_minimax_h3_i2v.json"
FRAMES = ROOT / "OUTPUT" / "13_外骨骼" / "frames"
OUT = ROOT / "OUTPUT" / "13_外骨骼" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6
STEPS = 4  # 本批全部为静态·单人·对话·慢推


def _detect_comfyui_base() -> Path:
    for c in [Path("E:/code/ComfyUI"),
              Path("E:/ComfyUI"),
              Path("E:/ComfyUI_windows_portable/ComfyUI"),
              Path.home() / "ComfyUI"]:
        if c.exists():
            return c
    return Path("E:/code/ComfyUI")


def get_comfyui_input_dir() -> Path:
    d = _detect_comfyui_base() / "input"
    d.mkdir(parents=True, exist_ok=True)
    return d


def upload_frame(frame_name: str) -> str:
    """把分镜帧复制到 ComfyUI input（文件名已是 ASCII，无需改名）。"""
    src = FRAMES / frame_name
    if not src.exists():
        raise FileNotFoundError(f"缺分镜帧: {src}")
    dst = get_comfyui_input_dir() / frame_name
    if not dst.exists() or src.stat().st_size != dst.stat().st_size:
        shutil.copy2(src, dst)
    return frame_name


# ── 14 镜（核心镜头 · 与 14 帧一一对应 · 台词随 H3 生成）──
SHOTS = [
    # —— 人物镜头（image_edit 定妆照帧）——
    {
        "shot": "01", "name": "莎拉·工位解释外骨骼",
        "img": "13_sarah_01_desk_explaining.png",
        "dur": 6.0, "seed": 1301,
        "prompt": (
            "Cinematic semi-realistic footage, 28-year-old Chinese woman at a tech company desk "
            "with dual monitors glowing. She gestures from her chest toward the right screen "
            "showing an AI world-model interface with rows of rendered virtual audience faces and "
            "a green/yellow/red laugh-intensity heat map. She speaks earnestly, not showing off, "
            "eyes steady; natural micro-expressions and small hand gestures. Afternoon light mixes "
            "with cold screen glow; subtle ink-wash bleeds from the monitor bezels. Medium shot, "
            "fixed camera. Audio: 意味着它在想象观众。它不是在分析我的文本，是在看，我讲。"
        ),
    },
    {
        "shot": "02", "name": "莎拉·地铁观察",
        "img": "13_sarah_02_subway_observing.png",
        "dur": 5.0, "seed": 1302,
        "prompt": (
            "Cinematic semi-realistic footage, 28-year-old Chinese woman in a crowded Shanghai "
            "morning subway car, gripping an overhead strap. She does not look at her phone; her "
            "gaze sweeps slowly across the other passengers — a woman with groceries, a student "
            "with leaky headphones, a dozing old man — taking them in without staring. The train "
            "sways, she adjusts her grip. Harsh fluorescent light and tunnel lights sweep past; "
            "ink-wash only on the window glass behind her. Extremely quiet, almost looking. "
            "Medium shot, slow lateral drift. Audio: 她想起地铁。明天早上，她不开车，坐地铁上班。是为了看看那些人，那些不在训练数据里的人。"
        ),
    },
    {
        "shot": "03", "name": "莎拉·吧台散场·0.52",
        "img": "13_sarah_03_bar_aftermath.png",
        "dur": 5.0, "seed": 1303,
        "prompt": (
            "Cinematic semi-realistic footage, 28-year-old Chinese woman sitting sideways at a "
            "closed comedy-club bar after the show, checking her phone. Warm amber bar light on "
            "one side of her face, cold blue from the window on the other. She reads a message, "
            "lips moving a brief answer, expression calm. Ink-wash bleeds from the dark window. "
            "Extremely quiet. Medium shot, slow push-in. Audio: 今天那个结尾，零点五二？是。"
        ),
    },
    {
        "shot": "04", "name": "师兄·咖啡·别用来赚钱",
        "img": "13_shixiong_01_coffee.png",
        "dur": 5.0, "seed": 1304,
        "prompt": (
            "Cinematic semi-realistic footage, 31-year-old Chinese male tech worker in an "
            "open-plan office, holding a company-logo coffee cup, dark circles under his eyes. "
            "He pauses, then speaks a short reply with a neutral expression; after speaking the "
            "corner of his mouth barely lifts — a half-mm micro-smile, not approval or "
            "disapproval, just recognition — then he covers it with a sip of coffee. Cold "
            "fluorescent light, visible pores and fine lines. Medium shot, subtle handheld drift. "
            "Audio: 那你别用来赚钱。我不赚。我只是用来筛段子。"
        ),
    },
    # —— 非人物镜头（场景 / UI / 道具 / 虚拟观众 · zimage 帧）——
    {
        "shot": "05", "name": "工位·外骨骼UI",
        "img": "13_office_01_exoskeleton_ui.png",
        "dur": 6.0, "seed": 1305,
        "prompt": (
            "Cinematic semi-realistic footage, close on a computer screen showing a clean "
            "world-model tuning interface; on one side a video window of a woman on a comedy "
            "stage, on the other rows of rendered virtual audience faces with laugh-intensity "
            "labels. Cold white and cool cyan data color, restrained clean interface. Ink-wash "
            "bleeds from the screen edges. Slow push-in, fixed camera. "
            "Audio: 基座是一个世界模型。她只是在教模型，莎拉·赵的观众为什么笑。"
        ),
    },
    {
        "shot": "06", "name": "地铁·早高峰·街头",
        "img": "13_subway_01_rush_hour.png",
        "dur": 5.0, "seed": 1306,
        "prompt": (
            "Cinematic semi-realistic footage, a crowded Shanghai rush-hour subway platform and "
            "car, anonymous commuters moving past each other, faces turned to phones; the cold "
            "fluorescent light and tunnel glow sweep across the crowd. Ink-wash bleeds only in "
            "the window reflections. Slow lateral drift, medium shot. "
            "Audio: 身体会告诉我，一个词从别人嘴里说出来的时候，是冒犯还是玩笑。模型看不到那个。"
        ),
    },
    {
        "shot": "07", "name": "实验室·2017深夜",
        "img": "13_lab_01_2017_night.png",
        "dur": 6.0, "seed": 1307,
        "prompt": (
            "Cinematic semi-realistic footage, a 2017-era Chinese lab at night, a desk lamp "
            "lighting only the work area with warm amber, old LCD monitors with CRT-blue glow "
            "behind, dust floating in the light. The camera holds on the quiet workspace as two "
            "voices exchange a short tired exchange off-screen. Nostalgic warm-amber and CRT-blue "
            "mix, ink-wash seeping from the frame edges. Slow push-in, medium shot. "
            "Audio: 你去睡。我不困。你眼睛红了。那是屏幕反光。"
        ),
    },
    {
        "shot": "08", "name": "酒吧·散场吧台",
        "img": "13_bar_01_aftermath.png",
        "dur": 6.0, "seed": 1308,
        "prompt": (
            "Cinematic semi-realistic footage, the empty bar of a small comedy club after the "
            "show, glasses on the counter, warm amber stage light fading at the edges, cold "
            "window light on the other side. Ink-wash bleeds from the dark corners. The camera "
            "drifts slowly across the quiet room. "
            "Audio: 不是零点五二。是没想到。模型知道小周会笑，但不知道为什么。莎拉知道。这就是区别。"
        ),
    },
    {
        "shot": "09", "name": "虚拟观众·想象的脸",
        "img": "13_virtual_audience_01_imaginary_face.png",
        "dur": 6.0, "seed": 1309,
        "prompt": (
            "Cinematic semi-realistic footage, an AI-rendered human face that is not real, "
            "laughing with mouth open but the laugh not reaching the eyes — skin texture too "
            "uniform, a barely perceptible delay between emotion and expression. A green AI "
            "annotation box reads a laugh-intensity value. Green, yellow and red heat-map zones "
            "faintly overlay the seats. Gray-blue render tint, clearly not a photograph. Ink-wash "
            "bleeds through the skin texture — the face dissolving at the edges. Slow push-in, "
            "close-up. Audio: 不存在的观众，在想象中笑着。绿色是安全，黄色是可能响，红色是大概率会响。"
        ),
    },
    {
        "shot": "10", "name": "虚拟观众·渲染vs真实",
        "img": "13_virtual_audience_02_render_vs_real.png",
        "dur": 6.0, "seed": 1310,
        "prompt": (
            "Cinematic semi-realistic footage, a split screen: above, an AI-rendered crowd of "
            "faces with the same too-perfect skin and delayed expressions; below, a real dimly "
            "lit audience. The rendered faces cannot produce the instant of surprise followed by "
            "a sudden laugh. Gray-blue render tint on the synthetic half, warm stage light on the "
            "real half. Ink-wash bleeds through the synthetic faces. Slow push-in. "
            "Audio: 模型不知道意外。它只知道概率。它渲染不出一个，因为没想到而愣住然后突然笑出来的脸。"
        ),
    },
    {
        "shot": "11", "name": "道具·笔记本标签",
        "img": "13_prop_01_notebook_label.png",
        "dur": 5.0, "seed": 1311,
        "prompt": (
            "Cinematic semi-realistic footage, a close-up of a notebook cover with a handwritten "
            "label, warm light on the paper texture and the edge of a desk. The camera pushes in "
            "slowly over the worn cover. Ink-wash bleeds softly from the frame edges. "
            "Audio: 她想起林薇说过，有些东西可以备份，有些东西不能。不能备份的那些，才是你。"
        ),
    },
    {
        "shot": "12", "name": "道具·微信对话·好",
        "img": "13_prop_02_wechat_hao.png",
        "dur": 5.0, "seed": 1312,
        "prompt": (
            "Cinematic semi-realistic footage, a close-up of a phone screen showing a chat "
            "thread with short message bubbles; a message appears, pauses, then a reply. Cold "
            "screen glow on a dark surface. Ink-wash bleeds faintly from the screen edges. "
            "Fixed camera, close-up. Audio: 你的车呢？在车库。我想看看那些人。好。"
        ),
    },
    {
        "shot": "13", "name": "UI·外骨骼主界面",
        "img": "13_ui_01_exoskeleton_clean.png",
        "dur": 5.0, "seed": 1313,
        "prompt": (
            "Cinematic semi-realistic footage, a clean software interface slowly reveals its "
            "name in the center of the screen while rendered audience faces and a heat map stay "
            "softly in the background. Cold white and cool cyan data color, restrained. Ink-wash "
            "bleeds from the screen edges. Slow push-in, close-up. "
            "Audio: 不是大脑，不是心脏。是骨架。撑着她，让她不会散架。但走路，还是她自己走。"
        ),
    },
    {
        "shot": "14", "name": "UI·双标注小周",
        "img": "13_ui_02_double_annotation_xiaozhou.png",
        "dur": 5.0, "seed": 1314,
        "prompt": (
            "Cinematic semi-realistic footage, a screen interface annotating a seat in the third "
            "row left with a high predicted laugh intensity; a small caption sits beside it. Cold "
            "white interface light, restrained and clean. Ink-wash bleeds from the edges. "
            "Slow push-in, close-up. Audio: 模型学到的是一个模式，认为这个位置应该响。但那两个人笑，不是因为段子好。"
        ),
    },
]
# ── API helpers ────────────────────────────────────────
def load_wf(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")


def wait(pid, timeout=1800):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = urllib.request.urlopen(f"{COMFY}/history/{pid}", timeout=10)
            d = json.loads(r.read())
            h = d.get(pid, {})
            st = h.get("status", {}).get("status_str", "")
            if st == "success" and h.get("outputs"):
                return h
        except Exception:
            pass
        time.sleep(5)
    raise TimeoutError(f"Timeout: {pid}")


def download(hist, out_dir):
    saved = []
    for _nid, node in hist.get("outputs", {}).items():
        for key in ("gifs", "images"):
            for item in node.get(key, []):
                fn = item["filename"]
                sub = item.get("subfolder", "")
                typ = item.get("type", "output")
                url = f"{COMFY}/view?filename={fn}&subfolder={sub}&type={typ}"
                dst = out_dir / fn
                urllib.request.urlretrieve(url, str(dst))
                saved.append(fn)
    return saved


def build_workflow(shot):
    wf = load_wf(WF)
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "LoadImage":
            node["inputs"]["image"] = shot["img"]
        elif ct == "MiniMaxH3ImageToVideo":
            node["inputs"]["prompt"] = shot["prompt"]
        elif ct == "PrimitiveFloat":
            node["inputs"]["value"] = shot["dur"]
        elif ct == "RandomNoise":
            node["inputs"]["noise_seed"] = shot["seed"]
        elif ct == "BasicScheduler":
            node["inputs"]["steps"] = STEPS
        elif ct == "ResolutionSelector":
            node["inputs"]["megapixels"] = MEGAPIXELS
            node["inputs"]["aspect_ratio"] = "16:9 (Widescreen)"
        elif ct == "SaveVideo":
            node["inputs"]["filename_prefix"] = f"video/EP13_SHOT-{shot['shot']}_H3"
    return wf


def run_one(shot):
    sid = shot["shot"]
    print(f"\n── SHOT-{sid}: {shot['name']} ({shot['dur']}s · seed={shot['seed']})")
    frame = upload_frame(shot["img"])
    wf = build_workflow(shot)
    pid = queue(wf)
    print(f"    submitted {pid[:8]}... waiting (5–15 min)...")
    t0 = time.time()
    hist = wait(pid)
    saved = download(hist, OUT)
    print(f"    done in {int(time.time() - t0)}s")
    for fn in saved:
        mb = (OUT / fn).stat().st_size / (1024 * 1024)
        print(f"    ✅ {fn} ({mb:.1f}MB)")
    return frame


def main():
    ap = argparse.ArgumentParser(description="第13集《外骨骼》H3 I2V 分镜视频生成（去 TTS）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--shot", type=str, help="按镜号筛选（如 01）")
    ap.add_argument("--limit", type=int, help="只跑前 N 镜")
    ap.add_argument("--skip-existing", action="store_true", help="跳过已出片的镜号（续跑用）")
    args = ap.parse_args()

    shots = [s for s in SHOTS if not args.shot or s["shot"] == args.shot]
    if args.limit:
        shots = shots[: args.limit]
    if args.skip_existing:
        shots = [s for s in shots if not any(OUT.glob(f"EP13_SHOT-{s['shot']}_H3_*"))]

    print("=" * 66)
    print(f" EP13《外骨骼》H3 I2V  |  {len(shots)}/{len(SHOTS)} 镜  |  mp={MEGAPIXELS} steps={STEPS}")
    print(f" 帧目录: {FRAMES}\n 输出: {OUT}")
    print("=" * 66)
    for s in shots:
        print(f"  - SHOT-{s['shot']}  {s['name']}  {s['dur']}s  ← {s['img']}  seed={s['seed']}")
    if args.dry_run:
        print("\n[Dry-run] 未实际提交。")
        return

    ok_n = 0
    for i, s in enumerate(shots, 1):
        try:
            run_one(s)
            ok_n += 1
        except Exception as e:
            print(f"    ❌ {e}")
        time.sleep(1)
    print(f"\n{'=' * 66}\n 完成: {ok_n}/{len(shots)}  输出: {OUT}")


if __name__ == "__main__":
    main()

