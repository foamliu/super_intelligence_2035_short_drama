#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第02集《经验》 Minimax H3 T2V 分镜视频生成脚本（无角色镜 · 23 镜 · 固化）。

作用：把第 02 集「无角色镜 → H3 T2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 有角色镜走 `gen_ep02_h3_r2v.py`（32 镜）；本脚本只做 23 个无角色镜
  （小华 UI 界面 / 系统内部视角 / Fab 空镜 / 夜景 / 道具特写），无需参考图。
- 分镜权威：`SCENES/02_经验.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威，
  标「（T2V）」或纯场景/道具/UI 的镜头都归本脚本）。
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep02_h3_t2v.py --dry-run
  python scripts/gen_ep02_h3_t2v.py --limit 4
  python scripts/gen_ep02_h3_t2v.py --shot 09
  python scripts/gen_ep02_h3_t2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（T2V 单参考图 · 16GB VRAM 红线内，约 1056×608）
  - steps=10（本线回落，勿默认堆 20；环境剧变镜才单点提 20）
  - 台词长度须匹配镜头时长（4s→4.46 / 5s→5.17 / 6s→6.58）
  - 无台词镜只写「正向音景」（不含可读词句、不用否定式）
  - 🚫 禁写元信息 / 对模型说的话 / 镜头编号指代（会渲染成画面字幕）
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
WF = ROOT / "workflows" / "video_minimax_h3_t2v.json"
OUT = ROOT / "OUTPUT" / "02_经验" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6   # T2V 单参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 23 个无角色镜（镜号 / 名称 / 时长 / seed / prompt）──
# 台词（L1）写进 Audio；无台词镜只写正向音景；seed = 2000 + 镜号（与 R2V 不冲突）
SHOTS = [
    # ── 一、起点（夜景 / 闪回道具 / UI）──
    {"shot": "01", "name": "Fab厂区夜景", "dur": 4.0, "seed": 2001,
     "prompt": ("CUT 1: 远景（城市全景），固定，2030年的深圳，凌晨四点，Fab厂区在夜色里亮着一排冷白灯带，塔楼上的排风扇静静旋转。"
                + STYLE + " Audio: 夜风与厂区设备低频嗡鸣。")},
    {"shot": "04", "name": "等离子体点火", "dur": 5.0, "seed": 2004,
     "prompt": ("CUT 1: 近景（设备特写），缓推，闪回质感，刻蚀机腔体内等离子体点火，蓝色辉光在腔体里亮起，射频电源的嗡鸣从尖锐渐趋沉稳。"
                + STYLE + " Audio: 他学了一年，才听懂第一台刻蚀机的「呼吸」——从尖锐到沉稳。")},
    {"shot": "05", "name": "师傅的手贴反应腔", "dur": 4.0, "seed": 2005,
     "prompt": ("CUT 1: 特写（手部），固定，闪回质感，一只枯瘦苍老的手掌贴在反应腔外壁上，久久不动，暖黄旧色调，颗粒感胶片质感。"
                + STYLE + " Audio: 记住这个感觉。它会变的。他记了二十八年。")},
    {"shot": "09", "name": "扬声器光点", "dur": 4.0, "seed": 2009,
     "prompt": ("CUT 1: 中近景（界面），固定，头顶扬声器的光点闪动，声波光效在暗处微微亮起。"
                + STYLE + " Audio: 数据显示聚焦环温度偏移零点三度——")},
    # ── 二、说不清（黄光全景 / UI / 手掌）──
    {"shot": "14", "name": "黄光区光刻机", "dur": 4.0, "seed": 2014,
     "prompt": ("CUT 1: 全景（人物全身加环境），缓拉，上午，光刻机在运行，黄光照亮洁净室一角，离子注入机旁站着一个穿白色洁净服的工人。"
                + STYLE + " Audio: 光刻机运转声与洁净室通风底噪。")},
    {"shot": "16", "name": "光点起伏·复盘", "dur": 6.0, "seed": 2016,
     "prompt": ("CUT 1: 中近景（界面），固定，扬声器的光点缓慢起伏。"
                + STYLE + " Audio: 但我复盘了我的模型。我查不到这个结论。湿度到供电到等离子体稳定性，我的知识库里没有这条路径。")},
    {"shot": "18", "name": "你给我的", "dur": 4.0, "seed": 2018,
     "prompt": ("CUT 1: 中近景（界面），固定，扬声器的光点轻微闪动。"
                + STYLE + " Audio: 是你给我的。不是我自己发现的。")},
    {"shot": "20", "name": "文字滚动·区别", "dur": 8.0, "seed": 2020,
     "prompt": ("CUT 1: 中近景（界面），缓推，屏幕上的文字一行行滚动。"
                + STYLE + " Audio: 区别是——我不知道你是怎么发现的。你给了一个结论，我存下来了。但下次遇到类似的情况，变量变化了，我可能还是连不上。")},
    {"shot": "23", "name": "我的平路", "dur": 4.0, "seed": 2023,
     "prompt": ("CUT 1: 中近景（界面），固定，扬声器的光点微微亮起。"
                + STYLE + " Audio: 我也有「平路」。我的模型里有数千万个数据点，建立了「正常」的统计分布。")},
    {"shot": "24", "name": "掌心压机台", "dur": 6.0, "seed": 2024,
     "prompt": ("CUT 1: 特写（手掌与机台），缓推，一只粗糙的手把掌心按在离子注入机外壳上，让震动传过掌心，背景黄光虚焦。"
                + STYLE + " Audio: 那不一样。你的平路是算出来的。我的平路是长出来的。")},
    {"shot": "25", "name": "向量落入待定区", "dur": 5.0, "seed": 2025,
     "prompt": ("CUT 1: 特写（界面），缓推，系统内部视角，一段对话被压缩成一个向量，落进标记为「待定」的存储区，幽蓝光晕。"
                + STYLE + " Audio: 小华把这段对话压缩成一个向量，存入标签为「待定」的存储区。它不知道里面装的是什么，但它决定不压缩、不汇总、不删除。")},
    # ── 三、不同（休息室 / UI）──
    {"shot": "26", "name": "休息室午休", "dur": 4.0, "seed": 2026,
     "prompt": ("CUT 1: 全景（环境），固定，午休时分，工厂外的一间休息室，桌上摆着盒饭，隔着玻璃能看到洁净室里黄光区的灯光。"
                + STYLE + " Audio: 空调低鸣与远处机台运转的底噪。")},
    {"shot": "29", "name": "被训练·文字浮现", "dur": 6.0, "seed": 2029,
     "prompt": ("CUT 1: 中近景（界面），缓推，屏幕上文字浮现。"
                + STYLE + " Audio: 我是被训练的。第一次初始化的时候，我的权重是随机的，没有「以前」可以比较。")},
    {"shot": "32", "name": "一整块", "dur": 4.0, "seed": 2032,
     "prompt": ("CUT 1: 中近景（界面），固定，屏幕上文字滚动，停顿。"
                + STYLE + " Audio: 老王，我可能永远不会有你的那个「一整块」。")},
    # ── 四、脚印（UI / 存储区）──
    {"shot": "38", "name": "数据没有异常", "dur": 3.0, "seed": 2038,
     "prompt": ("CUT 1: 中近景（界面），固定，扬声器方向的光点回应。"
                + STYLE + " Audio: 数据没有异常。")},
    {"shot": "40", "name": "未归类记录", "dur": 5.0, "seed": 2040,
     "prompt": ("CUT 1: 特写（界面），缓推，系统内部视角，一条记录生成，标题「关注」，置信度「不明」，标签「未归类」。"
                + STYLE + " Audio: 它查了这台新机台的所有数据。一切正常，甚至优于规格。王建国的「太干净了」，不在任何可测量的维度上。但它把这个判断记录了下来。")},
    # ── 五、良率（夜景 / 静物）──
    {"shot": "41", "name": "日班交接·夜景", "dur": 4.0, "seed": 2041,
     "prompt": ("CUT 1: 全景（环境），缓拉，晚上，Fab日班交接完，黄光灯光昏黄，像一座沉默的城市。"
                + STYLE + " Audio: 机台低鸣与远处设备运转的底噪。")},
    {"shot": "50", "name": "静物画·两人", "dur": 4.0, "seed": 2050,
     "prompt": ("CUT 1: 全景（环境），固定，Fab的黄光灯光下，机台静静运行，两个人并肩站成剪影，像一幅沉默的静物画。"
                + STYLE + " Audio: 机台低鸣与洁净室通风底噪。")},
    # ── 六、四月（夜景 / 系统内部 / 收黑）──
    {"shot": "51", "name": "深夜夜班", "dur": 4.0, "seed": 2051,
     "prompt": ("CUT 1: 全景（环境），固定，深夜，Fab的夜班在运行，机台指示灯在暗处明灭。"
                + STYLE + " Audio: 夜班机台运转的底噪。")},
    {"shot": "52", "name": "回看全天判断", "dur": 5.0, "seed": 2052,
     "prompt": ("CUT 1: 中景（界面），缓推，系统内部视角，数据一条条流过。"
                + STYLE + " Audio: 它回看了王建国全天的判断。每一次，数据都没有异常。每一次，王建国都是对的。")},
    {"shot": "53", "name": "特征工程熄灭", "dur": 6.0, "seed": 2053,
     "prompt": ("CUT 1: 特写（界面），缓慢横移，系统内部，搜索、特征工程、分类器，一个个掠过又熄灭。"
                + STYLE + " Audio: 它检查了所有传感器，做遍了所有特征工程，试了所有分类器。找不到。")},
    {"shot": "54", "name": "日志那句话", "dur": 6.0, "seed": 2054,
     "prompt": ("CUT 1: 特写（界面），缓推，日志界面，一行字缓缓打出。"
                + STYLE + " Audio: 它在日志里写下一行：「我拥有这个Fab的所有数据。但我没有拥有这个Fab。」后来，它没有再删除它。")},
    {"shot": "55", "name": "等待下一个四月", "dur": 5.0, "seed": 2055,
     "prompt": ("CUT 1: 全景（环境），缓拉，Fab里，机台在运行，数据在流动，画面缓缓收黑。"
                + STYLE + " Audio: 不是因为数据不够。是因为有些东西不在数据里。小华继续工作，等待下一个四月。")},
]


# ── ComfyUI 通用（与 R2V 脚本同构 · 固化）────────────────
def _load_wf():
    with open(WF, encoding="utf-8") as f:
        return json.load(f)


def _prompt(wf):
    p = {"prompt": wf, "client_id": str(uuid.uuid4())}
    data = json.dumps(p).encode()
    req = urllib.request.Request(f"{COMFY}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def _queue_until_done(prompt_id, poll=10, timeout=3600):
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


def _save_outputs(hist):
    """从 history 抓视频产物落盘到 OUT（遍历 images/gifs/videos/audio 四键）。"""
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
    # 参数注入（对齐 MCP _apply_h3_common + PrimitiveStringMultiline=prompt）
    for _nid, node in wf.items():
        ct = node.get("class_type", "")
        if ct == "MiniMaxH3ImageToVideo":
            node.setdefault("inputs", {})["prompt"] = shot["prompt"]
        elif ct == "PrimitiveStringMultiline":
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
                f"video/EP02_SHOT-{shot['shot']}_H3_T2V")
    return wf


def run_one(shot, wait=True, timeout=3600):
    wf = build_workflow(shot)
    res = _prompt(wf)
    pid = res["prompt_id"]
    print(f"[{shot['shot']}] {shot['name']} → pid={pid} dur={shot['dur']}s "
          f"seed={shot['seed']}")
    if not wait:
        return pid
    hist = _queue_until_done(pid, timeout=timeout)
    files = _save_outputs(hist)
    print(f"[{shot['shot']}] 完成：{len(files)} 个文件 → {[f.name for f in files]}")
    return files


def _existing_files(shot):
    return sorted(OUT.glob(f"EP02_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第02集《经验》H3 T2V 分镜视频生成（无角色镜）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 09）")
    ap.add_argument("--skip-existing", action="store_true", help="跳过已出片镜")
    ap.add_argument("--wait", action="store_true", help="阻塞等待出片（默认只提交）")
    ap.add_argument("--timeout", type=int, default=3600, help="单镜等待超时秒")
    args = ap.parse_args()

    shots = SHOTS
    if args.shot:
        shots = [s for s in SHOTS if s["shot"] == args.shot]
        if not shots:
            raise SystemExit(f"找不到镜号 {args.shot}")
    if args.limit:
        shots = shots[:args.limit]

    if args.dry_run:
        print(f"\n计划生成 {len(shots)} 镜（T2V · mp={MEGAPIXELS} · steps={STEPS} · {ASPECT}）：")
        for s in shots:
            note = " [已出片]" if _existing_files(s) else ""
            print(f"  镜{s['shot']} {s['name']} {s['dur']}s{note}")
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
