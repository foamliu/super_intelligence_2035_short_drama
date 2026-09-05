#!/usr/bin/env python3
"""Episode 13 TTS generation: Sarah Zhao + 师兄 via ComfyUI Qwen3-TTS API"""
import json, time, uuid, urllib.request
from pathlib import Path

COMFYUI = "http://127.0.0.1:8188"
WF = Path("E:/code/super_intelligence_2035_short_drama/workflows/Qwen3-TTS 语音合成.json")
OUT = Path("E:/code/super_intelligence_2035_short_drama/OUTPUT/13_外骨骼/audio")
OUT.mkdir(parents=True, exist_ok=True)

# ── Sarah lines (seed=1301, speaker seed locks voice consistency) ──
SARAH_LINES = [
    ("13_tts_sarah_01_backstage.flac", "明天那个模型的上线评审，你准备一下。", 1301),
    ("13_tts_sarah_02_desk.flac",
     "你知道外骨骼的定义是什么吗？不是让你变得更强——是帮你做你做不了的事。我训练了一个AI来看观众的表情、微动作、笑声强度。它帮我优化段子——实时分析哪里该停顿、哪里该加速。我管它叫外骨骼——帮我在台上站住。",
     1301),
    ("13_tts_sarah_03_openmic.flac",
     "我今天想聊聊外骨骼。不是工厂里的那种——是你的手机、你的推荐算法、你的自动驾驶。这些东西都在帮你——就像外骨骼帮焊工举起更重的东西。但问题不是它们能不能帮你。问题是——当它们帮到你习惯了之后，你还能自己走吗？",
     1301),
    ("13_tts_sarah_04_bar.flac",
     "他说你今晚讲的不像脱口秀。像你在公司没说完的话。我说对。脱口秀本来就是把公司里不能说的话，换个地方说出来。",
     1301),
    ("13_tts_sarah_05_hao.flac", "好", 1301),
]

SARAH_INSTRUCT = (
    "一位28岁中国女性，北京口音，有自嘲的节奏感。声音特质：聪明、清醒、"
    "不是愤世嫉俗——是\"我知道这个系统怎么运作，但我还是想说点什么\"。"
    "说话时有自然停顿，段子手节奏——该快的地方快，该停两秒的时候停。"
)

# ── 师兄 lines (seed=1303) ──
SHIXIONG_LINES = [
    ("13_tts_shixiong_01_hefa.flac", "合法吗？", 1303),
    ("13_tts_shixiong_02_code.flac", "你别把我的代码写进段子里。", 1303),
    ("13_tts_shixiong_03_bracket.flac", "第147行，括号错了。那是真的。真的才好笑。", 1303),
]

SHIXIONG_INSTRUCT = (
    "一位31岁中国男性，技术出身的管理者。声音不多话但有重量。"
    "认识你十年——从硕士面试到现在。说话慢，每个字都经过计算但不刻意。"
)

ALL_LINES = [
    ("莎拉", SARAH_LINES, SARAH_INSTRUCT, "Vivian", ""),
    ("师兄", SHIXIONG_LINES, SHIXIONG_INSTRUCT, "Dylan", ""),
]

def load_wf(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def queue(wf):
    data = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(f"{COMFYUI}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("prompt_id", "")

def wait(pid, timeout=300):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = urllib.request.urlopen(f"{COMFYUI}/history/{pid}", timeout=10)
            d = json.loads(r.read())
            h = d.get(pid, {})
            st = h.get("status", {}).get("status_str", "")
            if st == "success" and h.get("outputs"):
                return h
            elif st == "error":
                raise RuntimeError(f"Prompt failed: {h}")
        except: pass
        time.sleep(2)
    raise TimeoutError(f"Timeout: {pid}")

def get_outputs(hist):
    for nid, node in hist.get("outputs", {}).items():
        for img in node.get("images", []):
            yield img
        for aud in node.get("audio", []):
            yield aud

def download(item, dst):
    fn = item["filename"]; sub = item.get("subfolder", "")
    typ = item.get("type", "output")
    url = f"{COMFYUI}/view?filename={fn}&subfolder={sub}&type={typ}"
    try:
        urllib.request.urlretrieve(url, str(dst))
        return True
    except Exception as e:
        print(f"    download failed: {e}")
        return False

print("=" * 60)
print(" Episode 13 TTS - Sarah Zhao & 师兄")
print(f" Output: {OUT}")
print("=" * 60)

total_ok = 0
total = sum(len(lines) for _, lines, _, _, _ in ALL_LINES)

for role_name, lines, instruct, speaker, speaker_name in ALL_LINES:
    print(f"\n{'─'*50}")
    print(f" {role_name} ({len(lines)} lines) | speaker={speaker} ({speaker_name})")
    for i, (fn, text, seed) in enumerate(lines, 1):
        print(f"\n[{i}/{len(lines)}] {fn}")
        print(f"    text: {text[:80]}...")
        print(f"    seed: {seed}")

        wf = load_wf(WF)
        for nid, node in wf.items():
            ct = node.get("class_type", "")
            if ct == "Qwen3CustomVoice":
                node["inputs"]["text"] = text
                node["inputs"]["speaker"] = speaker
                node["inputs"]["seed"] = seed
                node["inputs"]["instruct"] = instruct
                node["inputs"]["custom_speaker_name"] = speaker_name
            elif ct == "SaveAudioAdvanced":
                # Use unique prefix per file so we can identify output later
                node["inputs"]["filename_prefix"] = f"audio/ep13_{fn.replace('.flac','')}"

        try:
            pid = queue(wf)
            print(f"    submitted {pid[:8]}..., waiting...")
            hist = wait(pid, timeout=300)
            items = list(get_outputs(hist))
            if items:
                dst = OUT / fn
                if download(items[0], dst):
                    kb = dst.stat().st_size // 1024
                    print(f"    OK: {dst} ({kb}KB)")
                    total_ok += 1
                else:
                    print(f"    FAIL: download")
            else:
                print(f"    ERROR: no audio output")
        except Exception as e:
            print(f"    ERROR: {e}")
            import traceback; traceback.print_exc()

        time.sleep(2)

print(f"\n{'='*60}")
print(f" TTS Done: {total_ok}/{total}")
print(f" Output: {OUT}")
