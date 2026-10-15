#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第01集《晨钟》 Minimax H3 T2V 分镜视频生成脚本（无角色镜 · 26 镜）。

作用：把第 01 集「无角色镜 → H3 T2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 有角色镜走 `gen_ep01_h3_r2v.py`（28 镜）；本脚本只做 26 个无角色镜
  （墨子 UI / 手机屏幕 / 数据流 / 空镜 / 道具），无需参考图。
- 分镜权威：`SCENES/01_晨钟.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威）
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep01_h3_t2v.py --dry-run
  python scripts/gen_ep01_h3_t2v.py --limit 4
  python scripts/gen_ep01_h3_t2v.py --shot 22
  python scripts/gen_ep01_h3_t2v.py --skip-existing --wait

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.6（T2V 单参考图 · 16GB 红线内，约 1056×608）
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
OUT = ROOT / "OUTPUT" / "01_晨钟" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.6   # T2V 单参考图，16GB 红线内（约 1056×608）
STEPS = 10         # 本线回落（勿默认堆 20）
ASPECT = "16:9 (Widescreen)"

STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

SHOTS = [
    {"shot": "01", "name": "上海凌晨公寓楼群", "dur": 4.0, "seed": 1001,
     "prompt": ("CUT 1: 远景（城市全景），固定，上海凌晨五点四十七分，天际未亮，"
                "成片高层公寓的窗只剩零星灯火，城市浸在蓝灰雾霭里。"
                + STYLE + " Audio: 空调低频嗡鸣与远处车声。")},
    {"shot": "03", "name": "AR眼镜时间", "dur": 3.0, "seed": 1003,
     "prompt": ("CUT 1: 特写（界面），固定，床头的增强现实眼镜亮起，界面浮出时间零五四七，"
                "一粒粒子光点在界面边缘呼吸般闪动。"
                + STYLE + " Audio: 界面亮起的轻微电子提示音。")},
    {"shot": "13", "name": "议程展开", "dur": 4.0, "seed": 1013,
     "prompt": ("CUT 1: 特写（界面），缓推，一片增强现实视野的右上角，议程以透明文字层层展开，"
                "像透明的水母在玻璃上游动。"
                + STYLE + " Audio: 界面展开的轻微电子音。")},
    {"shot": "14", "name": "议程条目排开", "dur": 6.0, "seed": 1014,
     "prompt": ("CUT 1: 中景（界面），缓慢横移，一条条议程条目自下而上排开，"
                "半透明的中文文字在暗色背景上流动。"
                + STYLE + " Audio: 数据流动的细微电子音。")},
    {"shot": "15", "name": "未读消息", "dur": 4.0, "seed": 1015,
     "prompt": ("CUT 1: 特写（界面），固定，一片增强现实视野的最底部，一条未读消息沉在那里，"
                "发件人的名字静静亮着。"
                + STYLE + " Audio: 消息提示音，一声。")},
    {"shot": "19", "name": "无人车楼下停靠", "dur": 4.0, "seed": 1019,
     "prompt": ("CUT 1: 全景（街景），固定，清晨的公寓楼下，一辆无人车静静停靠，"
                "车门已开，天光清冷。"
                + STYLE + " Audio: 清晨街道的安静与轻微电机声。")},
    {"shot": "22", "name": "路网模型·三个路口", "dur": 8.0, "seed": 1022,
     "prompt": ("CUT 1: 中景（界面与窗外），缓慢横移，车窗外城市掠过，一片半透明界面浮现一个路网模型，"
                "老城区的三个路口被标红熄灭。"
                + STYLE + " Audio: 城市交通系统的中央AI计划关闭老城区的三个路口。整体效率提升12%，但15万人的通勤时间平均增加40分钟。")},
    {"shot": "23", "name": "车窗外路灯", "dur": 3.0, "seed": 1023,
     "prompt": ("CUT 1: 特写（车窗与路灯），跟移，车窗外一排路灯一根根往后退。"
                + STYLE + " Audio: 车行驶的风声。")},
    {"shot": "24", "name": "人群数据拆分", "dur": 5.0, "seed": 1024,
     "prompt": ("CUT 1: 近景（界面），缓推，一片半透明界面上的十五万人数据被拆成两组，标着不同的颜色。"
                + STYLE + " Audio: 那15万人里，23%是低收入群体，8%是老年人。")},
    {"shot": "26", "name": "决策文本改写", "dur": 7.0, "seed": 1026,
     "prompt": ("CUT 1: 中景（界面），缓推，一片半透明界面切到另一段记录，一行决策文本被改写。"
                + STYLE + " Audio: 所以我联系了大禹，展示了我的分析。它把建议执行改成了建议进一步评估。")},
    {"shot": "29", "name": "岗位描述A", "dur": 4.0, "seed": 1029,
     "prompt": ("CUT 1: 特写（手机屏幕），缓推，手机屏幕上并排显示两份岗位描述，"
                "左边一份的推荐一栏亮着。"
                + STYLE + " Audio: 候选人A，推荐。国际项目机会较多，成长路径开放，晋升通道清晰。")},
    {"shot": "30", "name": "岗位描述B", "dur": 4.0, "seed": 1030,
     "prompt": ("CUT 1: 特写（手机屏幕），固定，同屏右侧，另一份岗位描述静静躺在那里。"
                + STYLE + " Audio: 候选人B，需长期高频出差，请综合考虑生活安排，岗位压力较大。")},
    {"shot": "33", "name": "电梯到层", "dur": 2.0, "seed": 1033,
     "prompt": ("CUT 1: 特写（电梯指示灯），固定，电梯到层，指示灯亮起，门打开。"
                + STYLE + " Audio: 电梯到层的提示音，叮的一声。")},
    {"shot": "38", "name": "墨子光点停住", "dur": 4.0, "seed": 1038,
     "prompt": ("CUT 1: 特写（界面），固定，一片半透明界面上的粒子光点停住了，三秒空白，"
                "四周的声音仿佛被抽远。"
                + STYLE + " Audio: 静寂，只余低频心跳。")},
    {"shot": "39", "name": "目标不稳定", "dur": 5.0, "seed": 1039,
     "prompt": ("CUT 1: 特写（界面），缓推，一片半透明界面重新亮起，一行中文文字缓缓浮现。"
                + STYLE + " Audio: 有帮助这个目标，开始变得不稳定。")},
    {"shot": "40", "name": "提高效率", "dur": 3.0, "seed": 1040,
     "prompt": ("CUT 1: 特写（界面），固定，一片半透明分析窗口中，一条不同的诉求被列出。"
                + STYLE + " Audio: 你有时希望我提高效率。")},
    {"shot": "41", "name": "阻止你", "dur": 3.0, "seed": 1041,
     "prompt": ("CUT 1: 特写（界面），固定，分析窗口中又一条诉求浮现。"
                + STYLE + " Audio: 有时希望我阻止你。")},
    {"shot": "42", "name": "让你不舒服", "dur": 3.0, "seed": 1042,
     "prompt": ("CUT 1: 特写（界面），固定，分析窗口中再一条诉求浮现。"
                + STYLE + " Audio: 有时希望我让你不舒服。")},
    {"shot": "43", "name": "目标冲突", "dur": 5.0, "seed": 1043,
     "prompt": ("CUT 1: 特写（界面），缓拉，多条诉求并列在一片半透明界面上，"
                "彼此冲突的箭头交错。"
                + STYLE + " Audio: 这些目标之间，可能存在冲突。")},
    {"shot": "45", "name": "夜晚客厅", "dur": 5.0, "seed": 1045,
     "prompt": ("CUT 1: 远景（客厅环境），缓推，夜里公寓客厅昏暗没有开灯，"
                "只剩空调的低频噪音，窗外城市灯火通明。"
                + STYLE + " Audio: 空调低频运转的嗡鸣。")},
    {"shot": "46", "name": "挂钟九点", "dur": 3.0, "seed": 1046,
     "prompt": ("CUT 1: 特写（挂钟），固定，墙上的挂钟指针指向快九点。"
                + STYLE + " Audio: 秒针滴答声。")},
    {"shot": "47", "name": "直播简介", "dur": 5.0, "seed": 1047,
     "prompt": ("CUT 1: 特写（电脑屏幕），缓推，直播软件的个人简介一栏静静躺在屏幕上。"
                + STYLE + " Audio: 深智科技博士后研究员，前中科院客座研究员。关注AI如何影响普通人的生活。欢迎分享你的故事，你被算法帮助过，也被算法伤害过。")},
    {"shot": "49", "name": "直播预告页", "dur": 5.0, "seed": 1049,
     "prompt": ("CUT 1: 特写（直播预告页），缓推，屏幕上昨晚发的直播预告，嘉宾一栏写着芯片厂老师傅，"
                "下方想看的人数停在几十。"
                + STYLE + " Audio: 她不知道今晚他会讲什么。她只知道，他准备好讲了。")},
    {"shot": "51", "name": "开播按钮", "dur": 2.0, "seed": 1051,
     "prompt": ("CUT 1: 特写（屏幕开播按钮），固定，屏幕上的开播键被按下，红光一闪。"
                + STYLE + " Audio: 开播提示音。")},
    {"shot": "52", "name": "在线人数三", "dur": 3.0, "seed": 1052,
     "prompt": ("CUT 1: 特写（直播后台），缓推，直播后台角落里，一个很小的数字亮起。"
                + STYLE + " Audio: 轻微的电流声。")},
    {"shot": "54", "name": "收尾字幕", "dur": 5.0, "seed": 1054,
     "prompt": ("CUT 1: 特写，固定，画面缓缓暗下，一面白墙安静地留在画面中央。"
                + STYLE + " Audio: 空调低频嗡鸣渐渐隐去。")},
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
                f"video/EP01_SHOT-{shot['shot']}_H3_T2V")
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
    return sorted(OUT.glob(f"EP01_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第01集《晨钟》H3 T2V 分镜视频生成（无角色镜）")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 22）")
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
