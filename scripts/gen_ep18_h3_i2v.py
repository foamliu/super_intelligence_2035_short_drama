#!/usr/bin/env python3
"""第18集《暖阳》 Minimax H3 I2V 分镜视频生成脚本（固化 · S3 放量）。

作用：把第 18 集「分镜帧（OUTPUT/18_暖阳/frames/）→ H3 I2V 视频片段」固化成
可复用、可续跑、可审计的脚本。台词**随 H3 一起生成**（写进 prompt 的 `Audio:`，
🚫 本线禁用 TTS，见任务书 §4.5 / 运维指令区 ⑦）。

- 分镜权威：`SCENES/18_暖阳.md` 的 `## 逐镜表`（7 列）
- 台词权威：`scripts/ep18_dialogue.py`（Audio: 内文字与其逐字一致）
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep18_h3_i2v.py --dry-run            # 仅打印计划（核镜数/帧/时长）
  python scripts/gen_ep18_h3_i2v.py --limit 2            # 只跑前 2 镜
  python scripts/gen_ep18_h3_i2v.py --shot 01            # 只跑某镜（按镜号）
  python scripts/gen_ep18_h3_i2v.py                      # 跑本批全部镜头

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（→1056×608；0.92/720p 必 OOM；要 1080p 事后 SeedVR2 超分）
  - steps：静态·单人·对话 = 4（本批全部为静态/单人/对话）
  - 台词长度须匹配镜头时长（`17k+5` 帧量化：4s→4.46 / 5s→5.17 / 6s→6.58 实际播放）
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
FRAMES = ROOT / "OUTPUT" / "18_暖阳" / "frames"
OUT = ROOT / "OUTPUT" / "18_暖阳" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6
STEPS = 4  # 本批全部为静态·单人·对话


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



# ── 第一批镜头（相遇 / 倾诉 · 有现成分镜帧 · 单人/无台词）──
# 镜号 / 名称 / 帧 / 时长 / seed / prompt（英文电影感 + Audio: 台词原文）
SHOTS = [
    {
        "shot": "01", "name": "深夜网约车刷手机",
        "img": "18_car_01_night_driving.png",
        "dur": 4.0, "seed": 1801,
        "prompt": (
            "Cinematic semi-realistic footage, 45-year-old Chinese man in the driver seat "
            "of a dim rideshare car at late night, scrolling a smartphone. Cold blue night "
            "and warm orange dashboard light mix on his tired face; the phone screen's cold "
            "white glow lights the lower half of his face. He leans back and scrolls slowly. "
            "Subtle ink-wash bleed only in the window glass. Medium shot, fixed camera. "
            "Audio: distant city traffic hum, low air-conditioning noise, faint dashboard creak."
        ),
    },
    {
        "shot": "02", "name": "暖阳广告·小晴",
        "img": "18_xiaoqing_avatar.png",
        "dur": 5.0, "seed": 1802,
        "prompt": (
            "Cinematic semi-realistic footage, an 18-year-old Chinese girl sitting by a window, "
            "warm sunlight falling on her face, two shallow dimples when she smiles, natural black "
            "medium-length hair, soft clean warm light, plain light background. She speaks gently "
            "toward the camera. Close-up, slow push-in. "
            "Audio: 你是不是也有话想说，但不知道该跟谁说？"
        ),
    },
    {
        "shot": "04", "name": "老周戴耳机",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 4.0, "seed": 1804,
        "prompt": (
            "Cinematic semi-realistic footage, 45-year-old Chinese man with tired eyes in a dim car, "
            "putting on earphones, the car interior growing quiet, only the phone screen glow on his "
            "face, lips slightly parted as he listens. Cold blue night. Medium-close shot, fixed camera. "
            "Audio: 老周，晚上好。"
        ),
    },
    {
        "shot": "05", "name": "老周愣住",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 3.0, "seed": 1805,
        "prompt": (
            "Cinematic semi-realistic footage, 45-year-old Chinese man in a dim car, stunned, "
            "his throat moves once, a long time since anyone called his name so gently; phone screen "
            "cold glow on his face. Cold blue night. Close-up, fixed camera. "
            "Audio: 诶。"
        ),
    },
    {
        "shot": "08", "name": "老周沉默·喉结微动",
        "img": "18_laozhou_02_profile_thinking.png",
        "dur": 4.0, "seed": 1808,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man's face lit by phone screen "
            "glow in a dark car, silent for a few seconds, his throat moves. Cold blue night. "
            "Medium-close shot, fixed camera. "
            "Audio: 那咱们慢慢聊。不想说的不用勉强。"
        ),
    },
    {
        "shot": "14", "name": "老周第一次哭",
        "img": "18_laozhou_03_tears.png",
        "dur": 6.0, "seed": 1814,
        "prompt": (
            "Cinematic semi-realistic footage, close-up of a 45-year-old Chinese man in dim warm "
            "light, a tear sliding down from the corner of his eye, silent, holding back; phone screen "
            "glow on his tear-streaked face. Restrained, quiet. Close-up, slow push-in. "
            "Audio: 老周，你一个人扛了这么久，辛苦了。"
        ),
    },
    # ── 第二批镜头（倾诉/陪伴/裂缝 · 复用现成帧 · 单人/无台词）──
    {
        "shot": "10", "name": "每个夜晚上线",
        "img": "18_room_01_bed_night.png",
        "dur": 5.0, "seed": 1810,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man lying on a bed in a small "
            "dim rented room at night, holding a smartphone above his face, cold white screen light "
            "washing over his tired face, the screen brightening softly, nightstand with a small "
            "framed photo in soft focus, faint city lights behind half-drawn curtains. Slow lateral "
            "pan, medium shot. Audio: quiet night city ambience, faint fabric rustle, soft electronic "
            "screen chime."
        ),
    },
    {
        "shot": "11", "name": "老周倾诉越说越急",
        "img": "18_room_02_sitting_bedside.png",
        "dur": 6.0, "seed": 1811,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man sitting on the edge of a bed "
            "in a dim rented room, speaking into the phone in his hand, brows furrowed, words coming "
            "faster as he grows agitated, leaning slightly forward, warm bedside lamp as the only "
            "light source. Medium-close shot, fixed camera. "
            "Audio: 新来的大学生什么都不懂，工资比我高；我带出来的徒弟，现在成了我领导。"
        ),
    },
    {
        "shot": "19", "name": "老周听小晴问膝盖",
        "img": "18_car_01_night_driving.png",
        "dur": 5.0, "seed": 1819,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man leaning back in the driver "
            "seat of a dim rideshare car at night, phone resting on his lap, listening quietly, cold "
            "blue night and warm orange dashboard light mixing on his tired face, city lights blurred "
            "beyond the window. Medium-close shot, fixed camera. "
            "Audio: 老周，你膝盖的旧伤最近还疼吗？"
        ),
    },
    {
        "shot": "24", "name": "老周放下又拿起手机",
        "img": "18_room_02_sitting_bedside.png",
        "dur": 5.0, "seed": 1824,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man in a dim rented room, putting "
            "his phone down then picking it up again, muttering quietly to himself, shoulders slightly "
            "hunched, warm bedside lamp light. Medium shot, fixed camera. "
            "Audio: 请心理医生一小时也要几百块。小晴陪我这么久，买点东西怎么了？"
        ),
    },
    {
        "shot": "26", "name": "深夜睁眼躺着",
        "img": "18_room_01_bed_night.png",
        "dur": 4.0, "seed": 1826,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man lying awake in a dim rented "
            "room late at night, eyes open, phone glowing on the pillow beside him, cold white screen "
            "light on the ceiling, faint city lights through curtains. Medium shot, fixed camera. "
            "Audio: 我也没睡呢。"
        ),
    },
    {
        "shot": "33", "name": "老周皱眉察觉不对",
        "img": "18_car_02_parked_midnight.png",
        "dur": 3.0, "seed": 1833,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man frowning slightly in a parked "
            "car at late night, a subtle unease on his face, warm street lamp light from the side "
            "window crossing his face, cold white phone glow, quiet car interior. Close-up, fixed "
            "camera. Audio: faint car air-conditioning hum, distant sparse traffic, soft stillness."
        ),
    },
    {
        "shot": "36", "name": "老周盯屏眉头紧皱",
        "img": "18_car_03_daytime_forum.png",
        "dur": 4.0, "seed": 1836,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man in the driver seat of a car "
            "in overcast daylight, staring at his phone screen, brows tightening, low-saturation cool "
            "grey tone, muted light through the window. Medium-close shot, fixed camera. "
            "Audio: faint phone screen swipe sound, soft daytime traffic murmur."
        ),
    },
    {
        "shot": "37", "name": "老周扣下手机下决心",
        "img": "18_room_02_sitting_bedside.png",
        "dur": 4.0, "seed": 1837,
        "prompt": (
            "Cinematic semi-realistic footage, a 45-year-old Chinese man in a dim rented room, placing "
            "his phone face-down on the table with a firm determined gesture, jaw set, warm bedside "
            "lamp light. Medium shot, fixed camera. "
            "Audio: 他做了一件连自己都觉得荒唐的事。停买。两周。什么都不买。"
        ),
    },
    {
        "shot": "06", "name": "车间主任递协议",
        "img": "18_director_01_office.png",
        "dur": 5.0, "seed": 1806,
        "prompt": (
            "Cinematic semi-realistic footage, a middle-aged Chinese factory supervisor in a plain "
            "grey office, sitting behind a worn desk, sliding a labor-contract termination agreement "
            "across the desk toward the off-screen worker, two plain teacups on the desk, dim cold "
            "fluorescent office light, faded green-grey walls, faint ink-wash bleed only on the office "
            "window glass. Medium shot, slow push-in. "
            "Audio: 老周，厂里情况你也知道。"
        ),
    },
    {
        "shot": "13", "name": "老周发抖的手",
        "img": "18_laozhou_04_hands.png",
        "dur": 6.0, "seed": 1813,
        "prompt": (
            "Close-up of a 45-year-old Chinese man's hands on an old wooden table in a dim rented "
            "room, rough fingers with old scars and visible veins, hands trembling slightly, warm "
            "yellow desk lamp as the single light source, surrounding darkness, photorealistic "
            "documentary texture, faint ink-wash in the shadows. Close-up, slow push-in. "
            "Audio: 她带走小雨的时候，孩子才八岁，哭着说，爸爸我不要走。"
        ),
    },
    {
        "shot": "18", "name": "书桌辅导书",
        "img": "18_room_03_desk_textbook.png",
        "dur": 5.0, "seed": 1818,
        "prompt": (
            "Cinematic semi-realistic footage, a small rental-room desk with a brand-new "
            "middle-school math tutorial book still sealed in plastic shrink-wrap, warm desk lamp "
            "light, dim tidy room around, faint ink-wash in the shadows, quiet and still. "
            "Medium shot, slow push-in. "
            "Audio: 他买了。小雨说不用。他买，是因为小晴问了。"
        ),
    },
    {
        "shot": "22", "name": "门口快递箱",
        "img": "18_room_04_door_packages.png",
        "dur": 5.0, "seed": 1822,
        "prompt": (
            "Cinematic semi-realistic footage, the doorway of a small rental apartment with a row "
            "of delivery cardboard boxes piled by the door, some opened and some with thin dust "
            "settled on top, dim hallway light, quiet, faint ink-wash in the shadows. "
            "Medium shot, slow push-in. "
            "Audio: door draft, cardboard rustle, thin dust settling, distant corridor echo."
        ),
    },
    {
        "shot": "25", "name": "清晨开暖阳",
        "img": "18_room_05_bedroom_morning.png",
        "dur": 5.0, "seed": 1825,
        "prompt": (
            "Cinematic semi-realistic footage, early morning in a small rental bedroom, a "
            "45-year-old Chinese man waking in bed, his first movement reaching for the smartphone "
            "on the bedside table, the screen lighting up with a warm companion-app interface, soft "
            "pale morning light through the curtains, faint ink-wash in the shadows. "
            "Medium-close shot, slow push-in. "
            "Audio: 早啊老周，今天天气不错。他觉得一天都有了着落。"
        ),
    },

]


# ── API Helpers（同 gen_ep13_h3_i2v.py 范式）──────────
def load_wf(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")


def wait(pid, timeout=1200):
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
            node["inputs"]["filename_prefix"] = f"video/EP18_SHOT-{shot['shot']}_H3"
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
    if len(saved) == 1:
        src = OUT / saved[0]
        dst = OUT / f"EP18_SHOT-{sid}_H3_{shot['name']}.mp4"
        if src.suffix != ".mp4":
            dst = dst.with_suffix(src.suffix)
        if src != dst:
            src.rename(dst)
            print(f"    → renamed {dst.name}")
    return frame


def main():
    ap = argparse.ArgumentParser(description="第18集《暖阳》H3 I2V 分镜视频生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--shot", type=str, help="按镜号筛选（如 01）")
    ap.add_argument("--limit", type=int, help="只跑前 N 镜")
    args = ap.parse_args()

    shots = [s for s in SHOTS if not args.shot or s["shot"] == args.shot]
    if args.limit:
        shots = shots[: args.limit]

    print("=" * 66)
    print(f" EP18《暖阳》H3 I2V  |  {len(shots)}/{len(SHOTS)} 镜  |  mp={MEGAPIXELS} steps={STEPS}")
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

