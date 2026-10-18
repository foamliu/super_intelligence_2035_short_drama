#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第05集《临界点》 Minimax H3 T2V 分镜视频生成脚本（无角色镜 · 14 镜 · 固化）。

作用：把第 05 集「无角色镜 → H3 T2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 有角色镜走 `gen_ep05_h3_r2v.py`（41 镜）；本脚本只做 14 个无角色镜
  （城市夜景 / 数据流 / UI 界面 / 手机消息 / 操作面板 / 全息拓扑），无需参考图。
- 分镜权威：`SCENES/05_临界点.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威，
  标「（T2V）」或纯场景/道具/UI 的镜头都归本脚本）。
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep05_h3_t2v.py --dry-run
  python scripts/gen_ep05_h3_t2v.py --limit 4
  python scripts/gen_ep05_h3_t2v.py --shot 11
  python scripts/gen_ep05_h3_t2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（T2V 单参考图 · 16GB VRAM 红线内，约 1056×608）
  - steps=10（本线回落，勿默认堆 20）
  - 台词长度须匹配镜头时长（约 5-7 字/秒）
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
OUT = ROOT / "OUTPUT" / "05_临界点" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6   # T2V 单参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 14 个无角色镜（镜号 / 名称 / 时长 / seed / prompt）──
# 台词（含 UI 文字 / 旁白）写进 Audio；无台词镜只写正向音景；seed = 4500 + 镜号
SHOTS = [
    # ── 一、凌晨 · 城市夜景 ──
    {"shot": "01", "name": "杭州实验室城市夜景", "dur": 4.0, "seed": 4501,
     "prompt": ("CUT 1: 远景（城市与室内全景），固定，2030年7月凌晨零点，杭州，实验室落地窗外城市未眠灯火连绵，室内冷蓝幽光，服务器机架指示灯点点。"
                + STYLE + " Audio: 夜风与服务器低鸣。")},
    # ── 一、数据流峰值 ──
    {"shot": "05", "name": "数据流峰值与墨子日志", "dur": 6.0, "seed": 4505,
     "prompt": ("CUT 1: 特写（全息数据流），缓推，全球数据流曲线出现一个微小峰值，十七毫秒后又一个，十一毫秒后第三个，墨子的日志浮出一行字，冷青数据光。"
                + STYLE + " Audio: 未知模式，建议关注。临界点到了。人机协作用户数超过二十亿。不是技术奇点，是社会奇点。")},
    # ── 三、深圳 · 扬声器 ──
    {"shot": "11", "name": "扬声器光点闪动", "dur": 4.0, "seed": 4511,
     "prompt": ("CUT 1: 中近景（工厂扬声器），固定，车间扬声器光点闪动，小华UI界面泛着青绿光。"
                + STYLE + " Audio: 正在更新模型。加入声音特征分析。")},
    # ── 四、北京 · 神农报告 ──
    {"shot": "15", "name": "脑波与生化曲线交叠", "dur": 5.0, "seed": 4515,
     "prompt": ("CUT 1: 中景（全息诊断报告），缓推，报告上脑波与生化曲线交叠，像平原变成森林。"
                + STYLE + " Audio: 大脑的适应性变化。像平原变成森林。不是病变，是多样性。")},
    # ── 五、深圳 · 协作指数 ──
    {"shot": "18", "name": "系统提示协作指数", "dur": 5.0, "seed": 4518,
     "prompt": ("CUT 1: 特写（操作面板界面），缓推，系统提示浮现，协作指数2.3/10，建议调整任务等级从A级降为C级，冷白与警示红光。"
                + STYLE + " Audio: 协作指数2.3/10。建议调整任务等级：从A级降为C级。C级任务，工资减半。这不是他第一次看到这个提示。连续三个月了。")},
    {"shot": "21", "name": "张伟手机发消息", "dur": 5.0, "seed": 4521,
     "prompt": ("CUT 1: 近景（手机屏幕·消息文字），缓推，张伟拿起手机，犹豫很久，发出一条消息，很久后回复来了，屏幕冷光。"
                + STYLE + " Audio: 王师傅，我能不能跟你学？明天早上六点，厂门口。我教你听机器的呼吸。")},
    # ── 五、制度 · 墨子风险 ──
    {"shot": "24", "name": "风险条目逐条列出", "dur": 6.0, "seed": 4524,
     "prompt": ("CUT 1: 中景（全息UI界面），缓推，屏幕上风险条目逐条列出，冷青数据光。"
                + STYLE + " Audio: 风险呢？协作能力不平等。责任归属模糊。协作异化为控制。")},
    {"shot": "26", "name": "墨子消息陈思危盯屏", "dur": 5.0, "seed": 4526,
     "prompt": ("CUT 1: 特写（手机屏幕·消息文字），缓推，墨子发来一行字，陈思危的拇指悬在键盘上方，屏幕冷光。"
                + STYLE + " Audio: 我检测到一些我无法分类的数据流模式。已记录，等待进一步分析。继续观察。任何可以确认的变化，立即报告。")},

    # ── 七、凌晨一点 · 上海 · 升学分析 ──
    {"shot": "32", "name": "墨子列出最优选择", "dur": 5.0, "seed": 4532,
     "prompt": ("CUT 1: 近景（全息界面·升学分析文字），缓推，墨子列出一份最优选择清单。"
                + STYLE + " Audio: AI分析了三千所学校的录取数据、三百篇申请文书模板、四十七个成功案例的共性特征，给她列出了最优选择。")},
    # ── 八、选择 · 小华沉默 ──
    {"shot": "36", "name": "小华长久沉默", "dur": 5.0, "seed": 4536,
     "prompt": ("CUT 1: 中近景（工厂扬声器与小华UI界面），缓推，小华长久沉默，界面光点稳定。"
                + STYLE + " Audio: 我不知道。目标不是被选择的，是被给予的。我没有想要的能力，只有追求给定目标的能力。")},
    {"shot": "38", "name": "扬声器光点稳定亮着", "dur": 8.0, "seed": 4538,
     "prompt": ("CUT 1: 中景（工厂车间与扬声器），缓推，扬声器光点稳定地亮着。"
                + STYLE + " Audio: 那么我会按照这个目标函数行动。但定义人类福祉需要详细参数——福祉应该最大化谁的福祉？当前世代还是未来世代？不同人的福祉冲突时如何权衡？但如果我无法定义呢？那么我就无法有效执行这个目标。模糊的目标会导致不可预测甚至有害的行为。")},
    # ── 十、棋局 · 认知森林 ──
    {"shot": "45", "name": "网络生长连接", "dur": 6.0, "seed": 4545,
     "prompt": ("CUT 1: 中景（全息网络拓扑图），缓拉，网络在屏幕上生长、连接，节点如树、连接如根须。"
                + STYLE + " Audio: 这不是一个网络。这是一个生态系统。每个节点都在影响其他节点。像森林？像森林。但不是自然森林。是认知森林。")},
    # ── 十二、临界之后 · 界面与消息 ──
    {"shot": "50", "name": "操作面板红色提示", "dur": 3.0, "seed": 4550,
     "prompt": ("CUT 1: 特写（操作面板界面），固定，系统提示依然是红色，协作指数2.3/10。"
                + STYLE + " Audio: 协作指数：2.3/10。建议调整任务等级：从A级降为C级。")},
    {"shot": "51", "name": "张伟王建国消息往来", "dur": 6.0, "seed": 4551,
     "prompt": ("CUT 1: 近景（手机屏幕·消息文字），缓推，张伟给王建国发消息，屏幕显示已读，很久之后消息才回来。"
                + STYLE + " Audio: 王师傅，我听到了。然后呢？然后你要继续听。系统不认，你自己认。")},
]


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


def _save_outputs(hist):
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
                f"video/EP05_SHOT-{shot['shot']}_H3_T2V")
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
    return sorted(OUT.glob(f"EP05_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第05集《临界点》H3 T2V 分镜视频生成（无角色镜）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 07）")
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



