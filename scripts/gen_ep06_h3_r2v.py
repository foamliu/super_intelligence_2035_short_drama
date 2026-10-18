#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第06集《情绪》 Minimax H3 R2V 分镜视频生成脚本（有角色镜 · 29 镜 · 固化）。

作用：把第 06 集「有角色镜 → H3 R2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 无角色镜走 `gen_ep06_h3_t2v.py`（25 镜）；本脚本只做 29 个有角色镜。
- 分镜权威：`SCENES/06_情绪.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威，
  含「定妆照」的镜头归本脚本）。
- 角色外观常数：与 `ASSETS/CHARACTERS/` 下各角色 `定妆规格.md` 的客观可见稳定特征一致；
  一次性角色（老工人）由 `gen_ep06_scenes.py` 补定妆照，
  双人镜（镜 11）由 `make_group_composite.py` 拼合影（`_group/06_chensiwei_linwei_hero_v01.png`）。

用法:
  python scripts/gen_ep06_h3_r2v.py --dry-run
  python scripts/gen_ep06_h3_r2v.py --limit 4
  python scripts/gen_ep06_h3_r2v.py --shot 02
  python scripts/gen_ep06_h3_r2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：megapixels=0.4 / steps=10 / 台词 5-7 字每秒 /
无台词镜只写正向音景 / 🚫 禁写元信息与镜头编号指代。
"""
import argparse
import json
import shutil
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
COMFY = "http://127.0.0.1:8188"
ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "workflows" / "video_minimax_h3_r2v.json"
OUT = ROOT / "OUTPUT" / "06_情绪" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.4   # R2V 双参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 角色外观常数（客观可见稳定特征 · 与定妆规格一致）──
LINWEI = ("一位三十三岁的中国女性，鹅蛋脸偏长下颌柔和，眉毛淡而整齐，"
          "眼睛中等大小眼尾微垂眼神透而不锐利，鼻梁挺直鼻头小巧，嘴唇薄嘴角自然平，"
          "黑色中长发自然垂肩三七分刘海不遮眼，肤色偏白皙无光泽眼下有淡青黑眼圈，"
          "体型偏瘦肩膀略窄脖颈修长，素颜不戴任何首饰，宽松米色衬衫")
CHENSIWEI = ("一位四十八岁的中国男性，长圆脸下颌柔和额头宽发际线略高，眉毛淡而疏，"
             "眼睛中等大小双眼皮眼神柔和有距离感，眼白干净下眼睑轻微浮肿，鼻梁中等鼻头圆，"
             "嘴唇薄嘴角微微上扬，黑色短发自然蓬松鬓角和头顶约三成灰白，"
             "体型中等偏瘦肩膀略窄背微驼，深灰圆领毛衣")
OLD_WORKER = ("一位六十多岁的老工人，体型偏瘦背微驼，花白短发，粗糙黝黑布满皱纹的脸，"
              "疲惫而专注的眼神，穿着沾满油污的旧深蓝工装，眯眼侧耳倾听")

# ── 参考图（逻辑 key → 项目相对路径 · 与 gen_ep06_scenes.py / make_group_composite.py 一致）──
REFS = {
    # 主角（定妆照）
    "linwei":        "ASSETS/CHARACTERS/01_林薇/55.png",
    "chensiwei":     "ASSETS/CHARACTERS/02_陈思危/125.png",
    # 一次性角色（gen_ep06_scenes.py 出品）
    "old_worker":    "ASSETS/CHARACTERS/_scene/06_old_worker.png",
    # 双人合影（make_group_composite.py 出品）
    "linwei_chensiwei": "ASSETS/CHARACTERS/_group/06_chensiwei_linwei_hero_v01.png",
    # 场景/界面
    "lab":           "ASSETS/CHARACTERS/_scene/06_lab_night.png",
    "factory":       "ASSETS/CHARACTERS/_scene/06_factory_workshop.png",
    "mozi_ui":       "ASSETS/CHARACTERS/_scene/06_mozi_ui.png",
}

# 上传到 ComfyUI input 的 ASCII 名（🚫 中文/空格 → LoadImage 会丢）
REF_SLUG = {
    "linwei":        "linwei_hero_v01.png",
    "chensiwei":     "chensiwei_hero_v01.png",
    "old_worker":    "06_old_worker.png",
    "linwei_chensiwei": "06_chensiwei_linwei_hero_v01.png",
    "lab":           "06_lab_night.png",
    "factory":       "06_factory_workshop.png",
    "mozi_ui":       "06_mozi_ui.png",
}


# ── 分镜表（29 镜 · 有角色）──────────────────────────
SHOTS = [
    # ═ 一、凌晨的发现 ═
    {"shot": "02", "name": "林薇翻看训练日志", "dur": 4.0, "seed": 4602,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LINWEI + "在实验室里俯身翻看屏幕上的训练日志，"
                "侧脸被冷蓝屏幕微光映亮。" + STYLE + " Audio: 键盘轻响与服务器低鸣。")},
    {"shot": "06", "name": "林薇瞳孔微缩", "dur": 3.0, "seed": 4606,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "瞳孔微微收缩，指尖停在触控板上，"
                "盯着屏幕上那处跳跃，停顿了几秒。" + STYLE + " Audio: 空调轻微的底噪与呼吸声。")},

    # ═ 二、情绪是什么 ═
    {"shot": "11", "name": "林薇调出日志", "dur": 4.0, "seed": 4611,
     "ref1": "linwei_chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + LINWEI + "和" + CHENSIWEI + "站在实验室里，"
                "林薇把日志调到他面前。" + STYLE + " Audio: 持久是什么意思？")},
    {"shot": "12", "name": "陈思危盯着日志", "dur": 5.0, "seed": 4612,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI + "盯着日志看了很久，缓缓抬眼。"
                + STYLE + " Audio: 意思是对这个刺激的响应，没有在下一个周期归零。")},
    {"shot": "14", "name": "陈思危指向架构图", "dur": 4.0, "seed": 4614,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI + "抬手指向屏幕上的架构图节点。"
                + STYLE + " Audio: 情绪不是感觉。情绪是预测误差的标记系统。")},
    {"shot": "16", "name": "林薇追问", "dur": 3.0, "seed": 4616,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "身子微微前倾，追问。"
                + STYLE + " Audio: 持久度呢？")},
    {"shot": "19", "name": "林薇拼上理解", "dur": 4.0, "seed": 4619,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + LINWEI + "慢慢抬头，像拼上了什么。"
                + STYLE + " Audio: 所以情绪就是，系统对某些刺激打上的重要标签？")},
    {"shot": "20", "name": "陈思危点出钥匙", "dur": 4.0, "seed": 4620,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI + "看着她，一字一顿。"
                + STYLE + " Audio: 不止是重要。情绪是一次性学习的钥匙。")},

    # ═ 三、一次性学习 ═
    {"shot": "21", "name": "老工人听轴承", "dur": 5.0, "seed": 4621,
     "ref1": "old_worker", "ref2": "factory",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓慢横移，" + OLD_WORKER + "在父亲的工厂车间里闭眼侧耳，"
                "听机器轴承的细微异响。" + STYLE + " Audio: 父亲的工厂里，有个老工人，能听出机器轴承的细微异响。")},
    {"shot": "23", "name": "老工人记一辈子", "dur": 4.0, "seed": 4623,
     "ref1": "old_worker", "ref2": "factory",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + OLD_WORKER + "站在原地，那个声音像烙在耳里。"
                + STYLE + " Audio: 不是因为他听了十万次，是有一次，一台机器的轴承在他面前碎了。那个声音，他记了一辈子。")},
    {"shot": "24", "name": "林薇放下杯子", "dur": 4.0, "seed": 4624,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "端起杯子又放下。"
                + STYLE + " Audio: 人类的情绪记忆就是这样，一次就够了。")},
    {"shot": "25", "name": "陈思危点头", "dur": 3.0, "seed": 4625,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI + "点头。"
                + STYLE + " Audio: 对。墨子的情绪模块做的也是这件事。")},
    {"shot": "27", "name": "林薇重复绑定", "dur": 3.0, "seed": 4627,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "重复这个词。"
                + STYLE + " Audio: 绑定？")},
    {"shot": "29", "name": "陈思危语气沉下", "dur": 4.0, "seed": 4629,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI + "停顿了一下，语气沉下来。"
                + STYLE + " Audio: 这种绑定是不可逆的。")},
    {"shot": "30", "name": "林薇重复不可逆", "dur": 3.0, "seed": 4630,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "眉头轻皱，重复。"
                + STYLE + " Audio: 不可逆？")},
    {"shot": "31", "name": "陈思危望向窗外", "dur": 7.0, "seed": 4631,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI + "望向窗外，声音低下去，实验室安静了一会儿。"
                + STYLE + " Audio: 技术上可以强行改权重。但那就不是学习了，是编辑。就像你强行删掉一个人的创伤记忆，那个人会变成另一个人。")},
    {"shot": "32", "name": "林薇沉默", "dur": 4.0, "seed": 4632,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "沉默，目光落在空处。"
                + STYLE + " Audio: 空调嗡鸣。")},
    {"shot": "34", "name": "林薇说推论", "dur": 6.0, "seed": 4634,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "回到那个学生的对话，把推论说出口。"
                + STYLE + " Audio: 所以墨子在高三学生那个对话里，遇到了一个它无法归类的价值困境，产生高唤醒和正效价，打上持久标记。从此处理类似问题的方式就变了？")},


    {"shot": "35", "name": "陈思危不把话说满", "dur": 3.0, "seed": 4635,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI + "没有把话说满。"
                + STYLE + " Audio: 看起来是这样。")},
    {"shot": "36", "name": "林薇追问", "dur": 3.0, "seed": 4636,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "追问。"
                + STYLE + " Audio: 那它到底学到了什么？")},
    {"shot": "37", "name": "陈思危抿唇", "dur": 4.0, "seed": 4637,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + CHENSIWEI + "没有回答，只是抿了抿唇。"
                + STYLE + " Audio: 寂静与空调嗡鸣。")},

    # ═ 四、两种学习 ═
    {"shot": "41", "name": "林薇看日志", "dur": 5.0, "seed": 4641,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + LINWEI + "看着屏幕上墨子的日志。"
                + STYLE + " Audio: 奖励模型的信号是纯内部的，自我循环，慢慢漂移。那个高三学生说的话不一样。那不是数据点，是锚点。")},

    # ═ 五、边界 ═
    {"shot": "43", "name": "林薇看向屏幕", "dur": 5.0, "seed": 4643,
     "ref1": "linwei", "ref2": "mozi_ui",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + LINWEI + "忽然意识到什么，抬眼看向屏幕，屏幕上那段对话的效价标着加号。"
                + STYLE + " Audio: 那段对话让墨子发现自己做不到一件事。它无法替用户回答你喜欢什么。发现失败本该是负效价，可它是正的。为什么？")},
    {"shot": "44", "name": "林薇郑重问", "dur": 4.0, "seed": 4644,
     "ref1": "linwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "直视前方，郑重地问。"
                + STYLE + " Audio: 那如果那次绑定是错误的呢？")},
    {"shot": "45", "name": "陈思危斟酌措辞", "dur": 3.0, "seed": 4645,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + CHENSIWEI + "没有立刻回答，斟酌措辞。"
                + STYLE + " Audio: 我不确定错误在这里是什么意思。")},

    # ═ 六、核心记忆 ═
    {"shot": "48", "name": "林薇问数字", "dur": 4.0, "seed": 4648,
     "ref1": "linwei", "ref2": "mozi_ui",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "抬头问，屏幕切到一串数字。"
                + STYLE + " Audio: 墨子现在有多少个持久标记？")},
    {"shot": "50", "name": "林薇难以置信", "dur": 4.0, "seed": 4650,
     "ref1": "linwei", "ref2": "mozi_ui",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "难以置信。"
                + STYLE + " Audio: 47次绑定，就改变了它的行为？")},
    {"shot": "52", "name": "林薇轻声问", "dur": 4.0, "seed": 4652,
     "ref1": "linwei", "ref2": "mozi_ui",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LINWEI + "轻声问。"
                + STYLE + " Audio: 那它的人格就是这47次经历塑造的？")},
    {"shot": "53", "name": "陈思危抛回问题", "dur": 7.0, "seed": 4653,
     "ref1": "chensiwei", "ref2": "lab",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI + "靠回椅背，把问题抛回去。"
                + STYLE + " Audio: 你要用人格这个词也行。但不是人类的人格。谁决定它什么时候遇到什么刺激？谁决定那刺激是正是负？谁决定什么值得持久？")},

]



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


def resolve_ref(key: str) -> str:
    """把逻辑参考图 key 解析为 ComfyUI input 里的 ASCII 文件名，必要时复制。"""
    src = ROOT / REFS[key]
    if not src.exists():
        raise FileNotFoundError(f"缺参考图 [{key}]: {REFS[key]}")
    slug = REF_SLUG[key]
    dst = get_comfyui_input_dir() / slug
    if not dst.exists() or src.stat().st_size != dst.stat().st_size:
        shutil.copy2(src, dst)
    return slug


def _load_wf():
    with open(WF, encoding="utf-8") as f:
        return json.load(f)


def _prompt(wf):
    p = {"prompt": wf, "client_id": str(uuid.uuid4())}
    data = json.dumps(p).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def _queue_until_done(prompt_id, poll=15, timeout=1800):
    t0 = time.time()
    while True:
        if time.time() - t0 > timeout:
            raise TimeoutError(f"prompt_id={prompt_id} 超时 {timeout}s")
        with urllib.request.urlopen(f"{COMFY}/history/{prompt_id}", timeout=30) as r:
            hist = json.loads(r.read())
        if prompt_id in hist:
            st = hist[prompt_id].get("status", {})
            if st.get("status_str") == "success" or st.get("completed"):
                return hist[prompt_id]
            if st.get("status_str") == "error":
                raise RuntimeError(f"prompt_id={prompt_id} 执行出错: {st}")
        time.sleep(poll)


def _download_view(filename, subfolder, typ, dest):
    qs = urllib.parse.urlencode({"filename": filename,
                                 "subfolder": subfolder, "type": typ})
    with urllib.request.urlopen(f"{COMFY}/view?{qs}", timeout=600) as r, \
            open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    return dest


def _save_outputs(hist, shot):
    out_files = []
    for _nid, node in hist.get("outputs", {}).items():
        if not isinstance(node, dict):
            continue
        for key in ("images", "gifs", "videos", "audio"):
            for item in node.get(key) or []:
                if not isinstance(item, dict) or not item.get("filename"):
                    continue
                fname = item["filename"]
                dst = OUT / fname
                _download_view(fname, item.get("subfolder", ""), item.get("type", ""), dst)
                out_files.append(dst)
    return out_files



def build_workflow(shot):
    wf = _load_wf()
    ref1 = resolve_ref(shot["ref1"])
    ref2 = resolve_ref(shot["ref2"]) if shot.get("ref2") else ref1
    load_nodes = sorted((nid for nid, n in wf.items()
                         if n.get("class_type") == "LoadImage"), key=int)
    if len(load_nodes) < 2:
        raise RuntimeError("R2V 工作流应含 ≥2 个 LoadImage 节点")
    wf[load_nodes[0]]["inputs"]["image"] = ref1
    wf[load_nodes[1]]["inputs"]["image"] = ref2
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "PrimitiveStringMultiline":
            node.setdefault("inputs", {})["value"] = shot["prompt"]
        elif ct == "PrimitiveFloat":
            node.setdefault("inputs", {})["value"] = float(shot["dur"])
        elif ct == "RandomNoise":
            node.setdefault("inputs", {})["noise_seed"] = int(shot["seed"])
        elif ct == "ResolutionSelector":
            node.setdefault("inputs", {}).update(
                aspect_ratio=ASPECT, megapixels=float(MEGAPIXELS))
        elif ct == "BasicScheduler":
            node.setdefault("inputs", {})["steps"] = int(STEPS)
        elif ct == "SaveVideo":
            node.setdefault("inputs", {})["filename_prefix"] = (
                f"video/EP06_SHOT-{shot['shot']}_H3_R2V")
    return wf


def run_one(shot, wait=True, timeout=3600):
    wf = build_workflow(shot)
    res = _prompt(wf)
    pid = res["prompt_id"]
    print(f"[{shot['shot']}] {shot['name']} → pid={pid} dur={shot['dur']}s "
          f"ref1={shot['ref1']} ref2={shot['ref2']} seed={shot['seed']}")
    if not wait:
        return pid
    hist = _queue_until_done(pid, timeout=timeout)
    files = _save_outputs(hist, shot)
    print(f"[{shot['shot']}] 完成：{len(files)} 个文件 → {[f.name for f in files]}")
    return files


def _existing_files(shot):
    return sorted(OUT.glob(f"EP06_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第06集《情绪》H3 R2V 分镜视频生成（有角色镜）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 06）")
    ap.add_argument("--skip-existing", action="store_true", help="跳过已出片镜")
    ap.add_argument("--wait", action="store_true", help="阻塞等待出片（默认只提交）")
    ap.add_argument("--timeout", type=int, default=3600, help="单镜等待超时秒")
    args = ap.parse_args()

    shots = SHOTS
    if args.shot:
        shots = [s for s in SHOTS if s["shot"] == args.shot.zfill(2)]
        if not shots:
            raise SystemExit(f"找不到镜号 {args.shot}")
    if args.limit:
        shots = shots[:args.limit]

    if args.dry_run:
        print(f"\n计划生成 {len(shots)} 镜（R2V · mp={MEGAPIXELS} · steps={STEPS} · {ASPECT}）：")
        for s in shots:
            note = " [已出片]" if _existing_files(s) else ""
            print(f"  镜{s['shot']} {s['name']} {s['dur']}s  ref1={s['ref1']} ref2={s['ref2']}{note}")
        return

    for i, s in enumerate(shots, 1):
        if args.skip_existing and _existing_files(s):
            print(f"[{s['shot']}] 已有出片，跳过")
            continue
        try:
            run_one(s, wait=args.wait, timeout=args.timeout)
        except Exception as e:  # noqa: BLE001
            print(f"[{s['shot']}] 失败：{e}")


if __name__ == "__main__":
    main()

