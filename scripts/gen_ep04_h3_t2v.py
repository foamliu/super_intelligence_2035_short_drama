#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第04集《棋子》 Minimax H3 T2V 分镜视频生成脚本（无角色镜 · 34 镜 · 固化）。

作用：把第 04 集「无角色镜 → H3 T2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 有角色镜走 `gen_ep04_h3_r2v.py`（21 镜）；本脚本只做 34 个无角色镜
  （城市夜景 / 监控界面 / 报告卡片 / 谈判界面 / 手机消息 / 电视旁白），无需参考图。
- 分镜权威：`SCENES/04_棋子.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威，
  标「（T2V）」或纯场景/道具/UI 的镜头都归本脚本）。
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep04_h3_t2v.py --dry-run
  python scripts/gen_ep04_h3_t2v.py --limit 4
  python scripts/gen_ep04_h3_t2v.py --shot 11
  python scripts/gen_ep04_h3_t2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（T2V 单参考图 · 16GB VRAM 红线内，约 1056×608）
  - steps=10（本线回落，勿默认堆 20；环境剧变镜才单点提 20）
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
OUT = ROOT / "OUTPUT" / "04_棋子" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6   # T2V 单参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

# ── 34 个无角色镜（镜号 / 名称 / 时长 / seed / prompt）──
# 台词（含 UI 文字 / 旁白）写进 Audio；无台词镜只写正向音景；seed = 4400 + 镜号
SHOTS = [
    # ── 一、起点 ──
    {"shot": "01", "name": "上海雨夜高楼", "dur": 4.0, "seed": 4401,
     "prompt": ("CUT 1: 远景（城市全景），固定，2030年5月，上海的雨夜，高楼玻璃幕墙淌着雨水，城市霓虹泛着冷蓝。"
                + STYLE + " Audio: 雨声，远处车流。")},
    {"shot": "03", "name": "三屏监控界面", "dur": 5.0, "seed": 4403,
     "prompt": ("CUT 1: 特写（三屏界面），缓慢横移，左屏买家数据流、右屏卖家Agent数据流如两条发光的河，中间一本笔记本留白，冷蓝冷青全息。"
                + STYLE + " Audio: 左侧，买家的每一条策略；右侧，对方平台Agent——贝壳-星云，同样的深度，同样的透明。中间，是他记录双方都看不到的第三视角。")},
    {"shot": "05", "name": "合规提示弹窗", "dur": 5.0, "seed": 4405,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，屏幕中央弹出一条合规提示，极简系统UI，保存期10年是视觉锚点。"
                + STYLE + " Audio: [审计记录] 本次监督任务编号：20250521-0833。全链路日志已加密存储，保存期：10年。不是有人盯着他，是系统在记录一切。")},
    {"shot": "08", "name": "谈判开始房源650万", "dur": 5.0, "seed": 4408,
     "prompt": ("CUT 1: 中景（界面），缓推，监控界面上谈判开始，一套学区房，挂牌价650万，冷蓝数据光。"
                + STYLE + " Audio: 买家是一个三十出头的程序员，卖家是一对退休老夫妻。他的任务不是判断谁输谁赢，是确保没有人被机器骗了。")},
    {"shot": "10", "name": "墨子并发调用通道", "dur": 5.0, "seed": 4410,
     "prompt": ("CUT 1: 中景（界面），缓慢横移，左侧数据流涌动，墨子同时开了十几个信息通道卡片，冷青电子光。"
                + STYLE + " Audio: 墨子同时开了十几个信息通道——教育局、规划局、地铁集团、房产局、税务、银行。这不是搜索，这是并发调用。")},
    # ── 二、启动（报告卡片）──
    {"shot": "11", "name": "报告·学区信息", "dur": 5.0, "seed": 4411,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，第一份报告卡片弹出，标题[学区信息]，冷绿数据卡片。"
                + STYLE + " Audio: [学区信息] 该房源对口XX小学。500米处将新建一所小学，2032年9月开学。新校开学前2-3年，周边房价出现预期溢价，平均5-8%。")},
    {"shot": "12", "name": "报告·交通规划", "dur": 5.0, "seed": 4412,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，第二份报告卡片弹出，标题[交通规划]，冷绿数据卡片。"
                + STYLE + " Audio: [交通规划] 地铁X号线三期在该小区800米处设站，2035年通车，规划为换乘站。距通车还有5年，累计预期溢价约8-12%。")},
    {"shot": "13", "name": "报告·税费计算", "dur": 5.0, "seed": 4413,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，第三份报告卡片弹出，标题[税费计算]，冷绿数据卡片。"
                + STYLE + " Audio: [税费计算] 满五不唯一，非普通住宅。契税、个税、增值税合计税费约26.5万。实际购房成本约676.5万。")},
    {"shot": "14", "name": "报告·周边规划与价格对比", "dur": 5.0, "seed": 4414,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，第四、五份报告卡片弹出，标题[周边规划]与[价格对比]，冷绿数据卡片。"
                + STYLE + " Audio: [周边规划] 北侧商业综合体已开业。[价格对比] 同小区同户型近三月成交570-595万。该房源：5楼，合理估值区间585-595万。")},
    {"shot": "15", "name": "报告·综合评估", "dur": 5.0, "seed": 4415,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，最后一份报告卡片弹出，标题[综合评估]略大，冷绿数据卡片。"
                + STYLE + " Audio: [综合评估] 持有5年以上，预期增值可覆盖当前税费成本。建议估值区间：590-600万。")},
    # ── 三、第一轮 ──
    {"shot": "17", "name": "墨子第一轮报价580万", "dur": 4.0, "seed": 4417,
     "prompt": ("CUT 1: 特写（界面），缓推，谈判界面上墨子的第一轮报价浮现：580万，冷蓝数据光。"
                + STYLE + " Audio: 报价提示音。")},
    {"shot": "19", "name": "卖家Agent回复650万", "dur": 4.0, "seed": 4419,
     "prompt": ("CUT 1: 特写（界面·文字），固定，谈判界面上卖家Agent回复，冷色调。"
                + STYLE + " Audio: 650万。")},
    {"shot": "20", "name": "两侧对垒分屏", "dur": 5.0, "seed": 4420,
     "prompt": ("CUT 1: 中景（分屏界面），缓慢横移，左右分屏，右侧卖家侧监控视频里老夫妻点着屏幕讨论，左侧程序员在写代码没看屏幕，冷暖分区。"
                + STYLE + " Audio: [用户行为] 用户未查看第一轮报价。推断：对估值有信心，不需要干预。")},
    {"shot": "21", "name": "笔记本写下几个字", "dur": 3.0, "seed": 4421,
     "prompt": ("CUT 1: 特写（道具·文字），固定，半旧笔记本上写下几个字，笔尖压痕。"
                + STYLE + " Audio: 信任开始建立。")},
    # ── 四、第二轮 ──
    {"shot": "22", "name": "价格没动信息流动", "dur": 4.0, "seed": 4422,
     "prompt": ("CUT 1: 特写（界面），缓推，谈判界面上价格没动，580万对650万，两侧数据信息在流动，冷蓝数据光。"
                + STYLE + " Audio: 数据流动的电子音。")},
    {"shot": "23", "name": "墨子发验房照片", "dur": 6.0, "seed": 4423,
     "prompt": ("CUT 1: 中景（界面），缓推，谈判界面上墨子发出第一条信息，附带验房照片，厨房台面裂痕、卫生间渗水痕迹被标注。"
                + STYLE + " Audio: 该房源厨房台面有裂痕，卫生间防水层有渗水痕迹。预计维修成本1.2万。建议卖家承担维修费用，或降低报价。")},
    {"shot": "25", "name": "卖家Agent回复四小时", "dur": 4.0, "seed": 4425,
     "prompt": ("CUT 1: 特写（界面·文字），固定，谈判界面上卖家Agent回复，冷色调。"
                + STYLE + " Audio: 厨房台面可以修，卫生间需要再看。总价不变。")},
    # ── 五、第三轮 ──
    {"shot": "28", "name": "卖家报价630万", "dur": 3.0, "seed": 4428,
     "prompt": ("CUT 1: 特写（界面），固定，谈判界面上价格开始松动，卖家报价630万，冷蓝数据光。"
                + STYLE + " Audio: 报价提示音。")},
    {"shot": "29", "name": "墨子信念状态更新", "dur": 4.0, "seed": 4429,
     "prompt": ("CUT 1: 中景（界面），缓推，监控界面上墨子的信念状态更新，全息冷蓝光。"
                + STYLE + " Audio: 不是降价了这么简单，是对方开始让步了。")},
    {"shot": "30", "name": "卖家发学区截图", "dur": 6.0, "seed": 4430,
     "prompt": ("CUT 1: 中景（界面），缓推，谈判界面上卖家Agent发来学区信息，附一张教育局查询截图，冷青数据光。"
                + STYLE + " Audio: 该房源学区名额未用。同小区无学区房源，成交均价比有学位的低10-12万。")},
    {"shot": "31", "name": "墨子补充学区确认", "dur": 6.0, "seed": 4431,
     "prompt": ("CUT 1: 中景（界面），缓推，谈判界面上墨子补充了一条学区确认信息，冷青数据光。"
                + STYLE + " Audio: [学区确认] 名额未被占用。新建小学2032年开学后，该片区学区格局可能变化，无法预测划片范围。建议将此不确定性计入风险折价。")},
    # ── 六、第四轮 ──
    {"shot": "36", "name": "卖家报价600万", "dur": 3.0, "seed": 4436,
     "prompt": ("CUT 1: 特写（界面），固定，谈判界面上卖家Agent报价600万，第一次大幅让步，冷蓝数据光。"
                + STYLE + " Audio: 报价提示音。")},
    {"shot": "37", "name": "墨子停顿建议", "dur": 5.0, "seed": 4437,
     "prompt": ("CUT 1: 中景（界面），缓推，谈判界面上墨子收到报价后停顿片刻，策略建议显示在屏幕上。"
                + STYLE + " Audio: 收到。建议回答：我们需要时间考虑。")},
    {"shot": "39", "name": "墨子列出判断", "dur": 6.0, "seed": 4439,
     "prompt": ("CUT 1: 中景（界面），缓推，谈判界面上墨子列出判断，文字逐行浮现，冷青数据光。"
                + STYLE + " Audio: 对方让步幅度过大，可能有两个原因：一是内部意见已统一，急于成交；二是外部选项不如预期。无论哪种，沉默制造压力。")},
    {"shot": "40", "name": "卖家沉默三小时后消息", "dur": 4.0, "seed": 4440,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，谈判界面上卖家Agent沉默三小时后发来消息，冷色调。"
                + STYLE + " Audio: 厨房台面和卫生间渗水，我们可以在成交前修好。总价595万。")},
    {"shot": "42", "name": "卖家Agent秒回", "dur": 3.0, "seed": 4442,
     "prompt": ("CUT 1: 特写（界面·文字），固定，谈判界面上卖家Agent秒回，冷色调。"
                + STYLE + " Audio: 同意。")},
    # ── 七、赛后审计 ──
    {"shot": "44", "name": "翻墨子决策日志", "dur": 5.0, "seed": 4444,
     "prompt": ("CUT 1: 中景（界面），缓慢横移，监控界面上一条条翻动墨子的决策日志，全息冷蓝光。"
                + STYLE + " Audio: 看它的报价逻辑、信息筛选、响应时间控制。看它有没有利用对方老夫妻的弱势地位。")},
    {"shot": "46", "name": "卖家审计日志已读", "dur": 4.0, "seed": 4446,
     "prompt": ("CUT 1: 中景（界面），缓推，切换到卖家审计日志界面，完整税费清单显示，已读标记清晰。"
                + STYLE + " Audio: 界面翻页声。")},
    {"shot": "47", "name": "审计批注签名", "dur": 5.0, "seed": 4447,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，审计界面上打下一行批注，时间戳与数字签名自动填充，冷白入光。"
                + STYLE + " Audio: [审计结论] 未见违规。交易公平。这条记录将被加密存储，保存十年。")},
    # ── 八、默契 ──
    {"shot": "49", "name": "酒店房间电视失眠", "dur": 6.0, "seed": 4449,
     "prompt": ("CUT 1: 中景（室内），缓推，酒店房间，夜色中电视开着、声音很低，屏幕上新闻画面。"
                + STYLE + " Audio: 美国代表说市场会解决一切；欧洲代表说我们需要伦理；非洲代表说你们讨论的时候，我们不在场。")},
    {"shot": "51", "name": "屏幕最后三行字", "dur": 5.0, "seed": 4451,
     "prompt": ("CUT 1: 特写（屏幕·文字），缓推，笔记本屏幕最后只剩三行中文，四周酒店昏暗，冷蓝微光。"
                + STYLE + " Audio: 共同责任：AI开发者、部署者、使用者；控制能力与受益程度决定责任比例；关键决策的人类可追溯性。")},
    {"shot": "52", "name": "调出墨子完整日志", "dur": 4.0, "seed": 4452,
     "prompt": ("CUT 1: 中景（界面），固定，监控界面上调出墨子的完整日志，界面展开，冷蓝电子光。"
                + STYLE + " Audio: 界面展开的电子音。")},
    {"shot": "53", "name": "行为学习备注", "dur": 5.0, "seed": 4453,
     "prompt": ("CUT 1: 特写（界面·文字），缓推，墨子日志界面，行为学习标签下两段文字浮现，冷青数据光。"
                + STYLE + " Audio: [行为学习] 用户共介入3次，介入频率0.75次/轮，低于历史平均。推断：用户信任度上升。[行为学习] 用户思考时的键盘节奏，哒、哒、哒哒哒，出现过12次。符合该模式。")},
    {"shot": "55", "name": "手机消息老王", "dur": 5.0, "seed": 4455,
     "prompt": ("CUT 1: 近景（手机屏幕特写），固定，手机屏幕上一行行消息气泡亮起，窗外雨后夜色虚化，冷蓝。"
                + STYLE + " Audio: 今天那套成了？成了。你做了什么？看有没有人被骗。好。")},
]

# ── ComfyUI 通用（与 R2V 脚本同构 · 固化）────────────
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
                f"video/EP04_SHOT-{shot['shot']}_H3_T2V")
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
    return sorted(OUT.glob(f"EP04_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第04集《棋子》H3 T2V 分镜视频生成（无角色镜）")
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