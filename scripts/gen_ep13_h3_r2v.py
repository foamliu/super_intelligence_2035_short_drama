#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第13集《外骨骼》 Minimax H3 R2V 分镜视频生成脚本（固化 · 2026-10-12 推翻旧法 · R2V 直出）。

作用：把第 13 集「参考图（定妆照/合影 + 场景图）→ H3 R2V 直出视频」固化成
可复用、可续跑、可审计的脚本。台词/人声**随 H3 一起生成**（写进 prompt 的
`Audio:`，🚫 本线禁用 TTS，见任务书 §4.5 / 运维指令区 ①）。

- 分镜权威：`SCENES/13_外骨骼.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威）
- 参考图规则（运维指令区 ① · 硬）：
  * 有角色镜 → R2V：`ref1`=定妆照/合影（`<Picture 1>`，按「在场人数」给脸），
    `ref2`=场景图（`<Picture 2>`，🚫 别用空场景）
  * 无角色镜 → T2V（本脚本只做 R2V；无角色镜另走 `gen_ep13_h3_t2v.py`）
  * ★ 合影 = 程序拼版（`ASSETS/CHARACTERS/_group/`），🚫 不经 `image_edit_longcat` 转
- 风格：以短剧仓 `ASSETS/半写实半水墨视觉规范.md` / `视觉总纲.md` 为准

用法:
  python scripts/gen_ep13_h3_r2v.py --dry-run          # 仅打印计划 + 核参考图是否都在
  python scripts/gen_ep13_h3_r2v.py --limit 4          # 只跑前 N 镜
  python scripts/gen_ep13_h3_r2v.py --shot 06          # 只跑某镜（按镜号）
  python scripts/gen_ep13_h3_r2v.py --skip-existing    # 跳过已出片镜（续跑）

参数纪律（§4.3 / §4.4 / §4.5）：
  - megapixels=0.4（R2V 双参考图 · 16GB VRAM 红线）
  - steps=10（角色镜默认；本批全部为静态/单人/对话/慢推，无环境剧变镜）
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
WF = ROOT / "workflows" / "video_minimax_h3_r2v.json"
OUT = ROOT / "OUTPUT" / "13_外骨骼" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

MEGAPIXELS = 0.4   # R2V 双参考图更吃显存，16GB 红线（见任务书 §4.3）
STEPS = 10         # 角色镜默认（4=静态对话 / 10=角色镜 / 20=环境剧变）
ASPECT = "16:9 (Widescreen)"

# ── 参考图注册表（逻辑名 → 源文件相对 ROOT 路径 · 上传时转 ASCII slug）──
REFS = {
    # 定妆照（外形的唯一权威）
    "sarah":    "ASSETS/CHARACTERS/08_莎拉·赵/主定妆照.png",
    "shixiong": "ASSETS/CHARACTERS/师兄/主定妆照.png",
    "linwei":   "ASSETS/CHARACTERS/01_林薇/55.png",
    # 合影（程序拼版，_group/）
    "sarah_shixiong": "ASSETS/CHARACTERS/_group/sarah_shixiong_hero_v01.png",
    "sarah_linwei":   "ASSETS/CHARACTERS/_group/sarah_linwei_hero_v01.png",
    # 场景图（缺的待补 · --dry-run 会报缺）
    "backstage":        "ASSETS/CHARACTERS/_scene/13_theatre_backstage.png",
    "openmic":          "ASSETS/CHARACTERS/_scene/13_openmic_stage.png",
    "interview":        "ASSETS/CHARACTERS/_scene/13_interview_room.png",
    "testcar":          "ASSETS/CHARACTERS/_scene/13_testcar_interior.png",
    "annualparty":      "ASSETS/CHARACTERS/_scene/13_annual_party_stage.png",
    "cafe":             "ASSETS/CHARACTERS/_scene/13_cafe.png",
    "office":           "ASSETS/CHARACTERS/_scene/13_office.png",
    "lab":              "ASSETS/CHARACTERS/_scene/13_lab_night.png",
    "subway":           "ASSETS/CHARACTERS/_scene/13_subway_car.png",
    "street":           "ASSETS/CHARACTERS/_scene/13_street.png",
    "phone":            "ASSETS/CHARACTERS/_scene/13_phone_screen.png",
    "screen_ui":        "ASSETS/CHARACTERS/_scene/13_screen_ui.png",
    "virtual_audience": "ASSETS/CHARACTERS/_scene/13_virtual_audience.png",
    "theatre_door":     "ASSETS/CHARACTERS/_scene/13_theatre_door.png",
}

# 逻辑名 → ComfyUI input 里的 ASCII 文件名（中文名会被改写成 mcp_ref_<hex>，见 §4.2）
REF_SLUG = {
    "sarah": "sarah_hero_v01.png",
    "shixiong": "shixiong_hero_v01.png",
    "linwei": "linwei_hero_v01.png",
    "sarah_shixiong": "sarah_shixiong_hero_v01.png",
    "sarah_linwei": "sarah_linwei_hero_v01.png",
    "backstage": "13_theatre_backstage.png",
    "openmic": "13_openmic_stage.png",
    "interview": "13_interview_room.png",
    "testcar": "13_testcar_interior.png",
    "annualparty": "13_annual_party_stage.png",
    "cafe": "13_cafe.png",
    "office": "13_office.png",
    "lab": "13_lab_night.png",
    "subway": "13_subway_car.png",
    "street": "13_street.png",
    "phone": "13_phone_screen.png",
    "screen_ui": "13_screen_ui.png",
    "virtual_audience": "13_virtual_audience.png",
    "theatre_door": "13_theatre_door.png",
}


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


# ── 有角色镜（R2V · 29 镜 · 台词随 H3 生成）────────────────
# 每镜：ref1=定妆照/合影(<Picture 1>)  ref2=场景图(<Picture 2>)
# prompt：`CUT 1:` + 景别范围 + 动作/站位 + 环境 + 风格 + `Audio:`（只放 L1 台词原文）
# ⚠️ 无台词镜只写正向音景；🚫 禁元信息/否定式/镜头编号指代
STYLE = ("semi-realistic Chinese ink-wash cinematic aesthetic, restrained color, "
         "16:9, photorealistic base with subtle ink bleed")

SHOTS = [
    {"shot": "03", "name": "莎拉·后台看手机", "dur": 5.0, "seed": 1303,
     "ref1": "sarah", "ref2": "backstage",
     "prompt": ("CUT 1: 中近景，一位三十岁中国女性坐在剧场后台一角低头看手机，耳机线垂在胸前；"
                "化妆镜暖黄灯光从一侧照来，台前的笑声与冷光从幕布缝隙漏进，冷暖交界。"
                + STYLE +
                " Audio: 明天那个模型的上线评审，你准备一下。在准备。")},
    {"shot": "06", "name": "面试室·师兄提问", "dur": 5.0, "seed": 1306,
     "ref1": "sarah_shixiong", "ref2": "interview",
     "prompt": ("CUT 1: 中景，面试室里两人面对面坐，中间隔一张桌板；女方在左、男方在右，"
                "冷白日光灯；男方提问、女方回答，神态认真，偶有手势。"
                + STYLE +
                " Audio: 你觉得自动驾驶最难的是什么？让车开得像人。不对。最难的是让别人相信你的车开得像人。")},
    {"shot": "07", "name": "测试车副驾·便利店", "dur": 6.0, "seed": 1307,
     "ref1": "sarah", "ref2": "testcar",
     "prompt": ("CUT 1: 中景，测试车行驶在上海街道上，一位三十岁中国女性坐副驾，目光看向前方街边的便利店；"
                "车身平稳减速，路边招牌缓缓入画。"
                + STYLE +
                " Audio: 在前边那个便利店门口停一下。已识别便利店，距离120米。正在减速。")},
    {"shot": "09", "name": "年会舞台·讲段子", "dur": 5.0, "seed": 1309,
     "ref1": "sarah", "ref2": "annualparty",
     "prompt": ("CUT 1: 中景，周末的公司年会现场，一位三十岁中国女性站在台上握着话筒讲段子，"
                "台下是年会的人群剪影，舞台暖光、背景压暗。"
                + STYLE +
                " Audio: 她的副业是脱口秀。一场15分钟，万把块钱。")},
    {"shot": "10", "name": "咖啡馆·对坐", "dur": 6.0, "seed": 1310,
     "ref1": "sarah_linwei", "ref2": "cafe",
     "prompt": ("CUT 1: 中景，咖啡馆里两位女性面对面坐、中间隔小桌板；女方在左、另一方在右，"
                "暖黄灯光与窗外冷光交界，神情平静。"
                + STYLE +
                " Audio: 以前写段子是因为我有话想说。现在写段子是因为我接了单。")},
    {"shot": "11", "name": "咖啡馆·还写吗", "dur": 5.0, "seed": 1311,
     "ref1": "sarah_linwei", "ref2": "cafe",
     "prompt": ("CUT 1: 近景，咖啡馆里两位女性面对面坐、中间隔小桌板；一方发问、另一方认真作答，"
                "暖黄灯光，眼神交流。"
                + STYLE +
                " Audio: 那你还写吗？写。但我需要找到那个有话想说的东西。不是为了甲方，是为了自己。")},
    {"shot": "13", "name": "界面·指着虚拟观众", "dur": 6.0, "seed": 1313,
     "ref1": "sarah", "ref2": "screen_ui",
     "prompt": ("CUT 1: 中景，一位三十岁中国女性站在电脑屏幕前，抬手指向屏幕上一排排渲染出的"
                "虚拟观众脸，冷白+冷青数据色，界面干净克制。"
                + STYLE +
                " Audio: 意味着它在想象观众。它不是在分析我的文本，是在看我讲。")},
    {"shot": "15", "name": "办公室·合法吗", "dur": 5.0, "seed": 1315,
     "ref1": "sarah_shixiong", "ref2": "office",
     "prompt": ("CUT 1: 中景，办公室里两人面对面、中间隔桌板；男方在左、女方在右，"
                "男方语气试探、女方平静回应，冷白灯光。"
                + STYLE +
                " Audio: 你拿公司的模型改的？嗯。合法吗？我读了一遍用户协议。没说不让。")},
    {"shot": "16", "name": "办公室·师兄沉默", "dur": 5.0, "seed": 1316,
     "ref1": "shixiong", "ref2": "office",
     "prompt": ("CUT 1: 近景，办公室里的男方沉默片刻，端起咖啡杯抿了一口，冷白灯光，画面克制。"
                + STYLE +
                " Audio: 那你别用来赚钱。我不赚。我只是用来筛段子。")},
    {"shot": "17", "name": "办公室·别写进段子", "dur": 4.0, "seed": 1317,
     "ref1": "sarah", "ref2": "office",
     "prompt": ("CUT 1: 近景，办公室里的女方笑着回了一句，神态轻松，冷白灯光。"
                + STYLE +
                " Audio: 但你别把我的代码写进段子里。我已经写了。哪段？")},
    {"shot": "18", "name": "办公室·第147行", "dur": 4.0, "seed": 1318,
     "ref1": "sarah_shixiong", "ref2": "office",
     "prompt": ("CUT 1: 近景，办公室里两人面对面、中间隔桌板；男方看着女方，女方带着笑意，冷白灯光。"
                + STYLE +
                " Audio: 第147行，括号错了。那是真的。真的才好笑。")},
    {"shot": "19", "name": "实验室·熬夜改代码", "dur": 6.0, "seed": 1319,
     "ref1": "sarah_shixiong", "ref2": "lab",
     "prompt": ("CUT 1: 中景，夜间实验室里女方坐在工位前熬夜改代码，男方站在她身后；"
                "屏幕冷光映脸，室内昏暗。"
                + STYLE +
                " Audio: 你去睡。我不困。你眼睛红了。那是屏幕反光。")},
    {"shot": "21", "name": "喂模型数据", "dur": 5.0, "seed": 1321,
     "ref1": "sarah", "ref2": "screen_ui",
     "prompt": ("CUT 1: 中景，一位三十岁中国女性把开放麦录像拖进电脑工具界面，"
                "冷白+冷青数据色，界面克制。"
                + STYLE +
                " Audio: 训练数据来自开放麦的录像。但这里有一个问题。")},
    {"shot": "23", "name": "屏幕标注·第三排", "dur": 5.0, "seed": 1323,
     "ref1": "sarah", "ref2": "screen_ui",
     "prompt": ("CUT 1: 中景，电脑屏幕上标注出观众席第三排左侧、预测笑声强度高；"
                "旁边一位三十岁中国女性凝视屏幕，冷白界面光。"
                + STYLE +
                " Audio: 模型学到的是一个模式，认为这个位置应该响。但那两个人笑，不是因为段子好。")},
    {"shot": "24", "name": "咖啡馆·脏数据", "dur": 5.0, "seed": 1324,
     "ref1": "sarah_linwei", "ref2": "cafe",
     "prompt": ("CUT 1: 中景，咖啡馆里两位女性面对面坐、中间隔小桌板；一方发问、另一方解释，"
                "暖黄灯光，认真神态。"
                + STYLE +
                " Audio: 所以你是在教模型一个脏数据？我在教模型看到数据，然后我自己来修正。")},
    {"shot": "26", "name": "刷手机·更新词表", "dur": 5.0, "seed": 1326,
     "ref1": "sarah", "ref2": "phone",
     "prompt": ("CUT 1: 中近景，一位三十岁中国女性刷着手机，看微博、B站、小红书，"
                "屏幕冷光映在脸上，神态专注。"
                + STYLE +
                " Audio: 模型听不懂最新的梗。所以莎拉每周都要手动更新词表。")},
    {"shot": "27", "name": "咖啡馆·我有身体", "dur": 5.0, "seed": 1327,
     "ref1": "sarah_linwei", "ref2": "cafe",
     "prompt": ("CUT 1: 近景，咖啡馆里一方发问、另一方从容作答，暖黄灯光，眼神坚定。"
                + STYLE +
                " Audio: 你在教模型听懂新梗？我在教它听懂人话。我学得比它快。因为我有身体。")},
    {"shot": "29", "name": "后台·贴新段子", "dur": 5.0, "seed": 1329,
     "ref1": "sarah", "ref2": "backstage",
     "prompt": ("CUT 1: 中近景，周三晚上开放麦后台，一位三十岁中国女性把新段子贴进模型，"
                "化妆镜暖黄灯与冷屏光交界。"
                + STYLE +
                " Audio: 安静的剧场后台底噪；键盘敲击声与偶尔的衣料摩擦声。")},
    {"shot": "32", "name": "后台·0.52的结尾", "dur": 4.0, "seed": 1332,
     "ref1": "sarah", "ref2": "backstage",
     "prompt": ("CUT 1: 近景，后台里一位三十岁中国女性在屏幕上选定一个标注0.52的位置，"
                "暖黄灯与冷屏光交界，神情专注。"
                + STYLE +
                " Audio: 她想起师兄说的话。模型告诉你什么大概率是对的。但它不知道什么小概率。")},
    {"shot": "33", "name": "舞台·自动驾驶段子", "dur": 8.0, "seed": 1333,
     "ref1": "sarah", "ref2": "openmic",
     "prompt": ("CUT 1: 中景，开放麦舞台上一位三十岁中国女性对着话筒讲段子，带一点手持现场感，"
                "舞台暖光、背景压暗。"
                + STYLE +
                " Audio: 我说，在前边那个便利店停一下。车说，已识别便利店。我说，你认识便利店？"
                "车说，我认识十二种便利店。我说，那你认识我常买的那种水吗？车说，你常买的是农夫山泉。"
                "我说，那不是水？")},
    {"shot": "34", "name": "观众席·没想到", "dur": 6.0, "seed": 1334,
     "ref1": "sarah", "ref2": "openmic",
     "prompt": ("CUT 1: 中景，开放麦观众席上一群真实观众先愣零点五秒、再恍然大悟般笑开，"
                "第三排左侧也笑了，舞台暖光，写实。"
                + STYLE +
                " Audio: 不是0.52。是没想到。模型知道小周会笑，但不知道为什么。莎拉知道。这就是区别。")},
    {"shot": "35", "name": "散场·看手机", "dur": 5.0, "seed": 1335,
     "ref1": "sarah", "ref2": "phone",
     "prompt": ("CUT 1: 近景，散场后一位三十岁中国女性看手机，屏幕冷光映脸，暖黄环境光。"
                + STYLE +
                " Audio: 今天那个结尾，0.52？是。")},
    {"shot": "36", "name": "打字回复", "dur": 6.0, "seed": 1336,
     "ref1": "sarah", "ref2": "phone",
     "prompt": ("CUT 1: 近景，一位三十岁中国女性低头打字回复消息，屏幕冷光，神态平静而笃定。"
                + STYLE +
                " Audio: 模型说的是预测笑声强度0.52，不是不行。训练数据里没有我的声音，没有我的停顿，没有小周。")},
    {"shot": "38", "name": "闪回·师兄的话", "dur": 6.0, "seed": 1338,
     "ref1": "sarah_shixiong", "ref2": "office",
     "prompt": ("CUT 1: 中景，办公室里男方对女方说话，两人面对面、中间隔桌板，冷白灯光，神态沉稳。"
                + STYLE +
                " Audio: 你知道为什么我从不评价你的段子吗？因为你不需要。你有自己的判断。"
                "你只是需要一个人帮你把那些肯定不行的去掉。")},
    {"shot": "39", "name": "问向模型·无回应", "dur": 5.0, "seed": 1339,
     "ref1": "sarah", "ref2": "screen_ui",
     "prompt": ("CUT 1: 近景，一位三十岁中国女性低声重复一个问题、问向屏幕，屏幕上没有回应，冷白界面光。"
                + STYLE +
                " Audio: 那你是我的工具还是我的搭档？模型没有回答。她没给它设计这个功能。")},
    {"shot": "41", "name": "剧场门口·夜色", "dur": 5.0, "seed": 1341,
     "ref1": "sarah", "ref2": "theatre_door",
     "prompt": ("CUT 1: 中景，一位三十岁中国女性站在剧场门口望向夜色，上海冬夜冷调，路灯暖光与夜色交界。"
                + STYLE +
                " Audio: 但她的观众会那样笑。这就是她还站在台上的原因。")},
    {"shot": "42", "name": "地铁·看车厢里的人", "dur": 5.0, "seed": 1342,
     "ref1": "sarah", "ref2": "subway",
     "prompt": ("CUT 1: 中景，第二天早上的上海地铁车厢里，一位三十岁中国女性看着车厢里的人群，"
                "不玩手机，目光缓缓扫过，荧光灯与隧道灯交替掠过。"
                + STYLE +
                " Audio: 她想起地铁。明天早上，她不开车，坐地铁上班。是为了看看那些人，那些不在训练数据里的人。")},
    {"shot": "45", "name": "手机·明天坐地铁", "dur": 5.0, "seed": 1345,
     "ref1": "sarah", "ref2": "phone",
     "prompt": ("CUT 1: 近景，手机亮起一条消息，一位三十岁中国女性回复，屏幕冷光映脸。"
                + STYLE +
                " Audio: 明天九点，别迟到。知道。师兄，我明天坐地铁。")},
    {"shot": "47", "name": "走出剧场·晨光", "dur": 5.0, "seed": 1347,
     "ref1": "sarah", "ref2": "theatre_door",
     "prompt": ("CUT 1: 中景，一位三十岁中国女性拿起包走出剧场，窗外东方的晨光从楼宇之间漏出来，暖金天光。"
                + STYLE +
                " Audio: 不是算法预测的下一个窗口。是今天。是现在。她不想预测。想坐地铁。")},
]


# ── ComfyUI API 原语（照 gen_ep13_h3_i2v.py 范式）─────────
import urllib.parse


def load_wf():
    with open(WF, encoding="utf-8") as f:
        return json.load(f)


def _prompt(prompt):
    p = {"prompt": prompt, "client_id": str(uuid.uuid4())}
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
            status = hist[prompt_id].get("status", {})
            if status.get("status_str") == "success" or status.get("completed"):
                return hist[prompt_id]
            if status.get("status_str") == "error":
                raise RuntimeError(f"prompt_id={prompt_id} 执行出错: {status}")
        time.sleep(poll)


def _download_view(filename, subfolder, typ, dest):
    qs = urllib.parse.urlencode({"filename": filename,
                                 "subfolder": subfolder, "type": typ})
    with urllib.request.urlopen(f"{COMFY}/view?{qs}", timeout=180) as r, \
            open(dest, "wb") as f:
        shutil.copyfileobj(r, f)
    return dest


def _save_outputs(hist, shot):
    """从 history 里抓视频产物落盘到 OUT，返回 [Path,...]。"""
    out_files = []
    for _nid, node in hist.get("outputs", {}).items():
        for item in node.get("videos", []):
            fname = item.get("filename")
            dst = OUT / fname
            _download_view(fname, item.get("subfolder", ""), item.get("type", ""), dst)
            out_files.append(dst)
    return out_files


def build_workflow(shot):
    wf = load_wf()
    ref1 = resolve_ref(shot["ref1"])
    ref2 = resolve_ref(shot["ref2"]) if shot.get("ref2") else ref1
    # LoadImage 按节点 id 升序：第一个 → ref1(<Picture 1>)，第二个 → ref2(<Picture 2>)
    load_nodes = sorted((nid for nid, n in wf.items()
                         if n.get("class_type") == "LoadImage"), key=int)
    if len(load_nodes) < 2:
        raise RuntimeError("R2V 工作流应含 ≥2 个 LoadImage 节点")
    wf[load_nodes[0]]["inputs"]["image"] = ref1
    wf[load_nodes[1]]["inputs"]["image"] = ref2
    # 参数注入（对齐 MCP `_apply_h3_common` + `PrimitiveStringMultiline`=prompt）
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
                f"video/EP13_SHOT-{shot['shot']}_H3_R2V")
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
    return sorted(OUT.glob(f"EP13_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第13集《外骨骼》H3 R2V 分镜视频生成")
    ap.add_argument("--dry-run", action="store_true", help="仅打印计划 + 核参考图")
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 镜（0=全部）")
    ap.add_argument("--shot", type=str, default="", help="只跑某镜（镜号，如 06）")
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

    # 参考图可用性预检（缺图 = 补资产清单）
    missing = []
    for s in shots:
        for key in (s["ref1"], s.get("ref2")):
            if key and not (ROOT / REFS[key]).exists():
                missing.append((s["shot"], key, REFS[key]))
    if missing:
        print("⚠️  缺参考图（需先补资产）：")
        for shot, key, path in missing:
            print(f"   - 镜{shot}: [{key}] {path}")
    else:
        print("✅ 所有参考图在位")

    if args.dry_run:
        print(f"\n计划生成 {len(shots)} 镜（R2V · mp=0.4 · steps=10 · 16:9）：")
        for s in shots:
            note = " [已出片]" if _existing_files(s) else ""
            print(f"  镜{s['shot']} {s['name']:　<14} {s['dur']}s  "
                  f"{s['ref1']}+{s.get('ref2')}{note}")
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

