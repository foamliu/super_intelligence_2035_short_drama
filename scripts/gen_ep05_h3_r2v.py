#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第05集《临界点》 Minimax H3 R2V 分镜视频生成脚本（有角色镜 · 41 镜 · 固化）。

作用：把第 05 集「有角色镜 → H3 R2V 直出视频」固化成可复用、可续跑、可审计的脚本。
台词/人声随 H3 一起生成（写进 prompt 的 `Audio:`，🚫 本线禁用 TTS）。
- 无角色镜走 `gen_ep05_h3_t2v.py`（14 镜）；本脚本只做 41 个有角色镜。
- 分镜权威：`SCENES/05_临界点.md` 的 `## 逐镜表`（7 列 · 参考图提示列 = 唯一权威，
  含「定妆照」的镜头归本脚本）。
- 角色外观常数：与 `ASSETS/CHARACTERS/` 下各角色 `定妆规格.md` 的客观可见稳定特征一致；
  一次性角色（张伟/小李/刘医生/主管/林小雯/老师/周敏）由 `gen_ep05_scenes.py` 补定妆照，
  双人镜由 `make_group_composite.py` 拼合影（`_group/05_*`）。

用法:
  python scripts/gen_ep05_h3_r2v.py --dry-run
  python scripts/gen_ep05_h3_r2v.py --limit 4
  python scripts/gen_ep05_h3_r2v.py --shot 06
  python scripts/gen_ep05_h3_r2v.py --skip-existing --wait

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
OUT = ROOT / "OUTPUT" / "05_临界点" / "videos"
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
WANGJIANGUO = ("一位六十岁的中国男性，方脸下颌宽方正颧骨略高，皮肤黝黑偏黄，眉毛粗而浓眉间习惯微皱，"
               "眼睛不大单眼皮眼白微黄眼神平静，鼻梁不高鼻头圆润，嘴唇偏厚嘴角自然下垂，"
               "黑色短发剪得很短几乎贴头皮鬓角几根白发，体型偏壮肩膀宽背直，"
               "手大手指粗短指节粗大老茧厚实，旧深蓝工装裤灰色长袖T恤")
LISIYUAN = ("一位三十五岁的中国男性，圆脸下颌线柔和面部微胖，久坐的浮肿感双下巴若隐若现，"
            "眼角有细纹，眉毛中等自然，眼睛中等大小戴细框眼镜镜片有轻微反光，"
            "眼神专注仔细不锐利，眼白有轻微红血丝，鼻梁中等鼻头圆，嘴唇偏厚嘴角自然，"
            "黑色短发自然略显油腻，体型微胖肚子微凸肩膀略圆背微驼，深色藏青polo衫")
PRIYA = ("一位二十五岁的印度达利特女性，深棕色肤色有自然光泽，深褐色大眼睛眼神坚定有韧性，"
         "眉毛自然略粗，鼻梁不高线条柔和，嘴唇丰满，黑色长发低马尾，"
         "体型偏瘦但肩背挺直，深蓝色棉质库尔塔")
LAOZHOU = ("一位四十五岁的中国男性，圆脸偏瘦颧骨突出，眼角细纹额头横纹法令纹深，"
           "眉毛粗短眉尾稀疏，单眼皮眼角微垂眼下浮肿有黑眼圈，鼻子直而普通嘴唇干裂偏薄常抿着，"
           "肤色偏黑黄肤质粗糙，黑色短发发际线后退鬓角几根白发，"
           "体型偏瘦肩背宽轻微驼背，深蓝色Polo衫领口微松")
ZHANGWEI = ("一位四十八岁的中国男性工人，中等身材略驼背，黑色短发鬓角有些灰白，"
            "脸上有深深的鼻唇沟，疲惫但诚恳的眼神，手上满是老茧，褪色的深蓝色工装卷起袖子")
XIAOLI = ("一位二十出头的年轻中国男性工人，体型偏瘦，黑色短发，"
          "皮肤光洁，认真好奇的眼神，灰蓝色工装")
LIU_DOCTOR = ("一位四十多岁的中国男性医生，中等身材，戴细框眼镜，白大褂内搭浅色衬衫，"
              "黑色短发略有灰白，平静沉思的表情")
SUPERVISOR = ("一位四十多岁的中国男性工厂主管，体型略胖，黑色短发，"
              "深色衬衫深色长裤，严厉但不刻薄的表情")
LINXIAOWEN = ("一位十几岁的中国女学生，体型偏瘦，齐肩黑色头发，"
              "明亮认真的眼睛，素色校服")
TEACHER = ("一位四十多岁的中国女教师，中等身材，短发，戴眼镜，"
           "素色开衫内搭衬衫，耐心的表情")
ZHOUMIN = ("一位四十多岁的中国女性，中等身材，齐肩黑色头发松松扎起，"
           "疲惫的眼神，居家便服浅色开衫")

# ── 参考图（逻辑 key → 项目相对路径 · 与 gen_ep05_scenes.py / make_group_composite.py 一致）──
REFS = {
    # 主角（定妆照）
    "linwei":       "ASSETS/CHARACTERS/01_林薇/55.png",
    "chensiwei":    "ASSETS/CHARACTERS/02_陈思危/125.png",
    "wangjianguo":  "ASSETS/CHARACTERS/05_王建国/104.png",
    "lisiyuan":     "ASSETS/CHARACTERS/09_李思远/主定妆照.png",
    "priya":        "ASSETS/CHARACTERS/06_普里亚·夏尔马/01_正面定妆.png",
    "laozhou":      "ASSETS/CHARACTERS/07_老周/01_正面定妆.png",
    # 一次性角色（gen_ep05_scenes.py 出品）
    "zhangwei":     "ASSETS/CHARACTERS/_scene/05_zhangwei.png",
    "xiaoli":       "ASSETS/CHARACTERS/_scene/05_xiaoli.png",
    "liu_doctor":   "ASSETS/CHARACTERS/_scene/05_liu_doctor.png",
    "supervisor":   "ASSETS/CHARACTERS/_scene/05_supervisor.png",
    "linxiaowen":   "ASSETS/CHARACTERS/_scene/05_linxiaowen.png",
    "teacher":      "ASSETS/CHARACTERS/_scene/05_teacher.png",
    "zhoumin":      "ASSETS/CHARACTERS/_scene/05_zhoumin.png",
    # 双人合影（make_group_composite.py 出品）
    "wang_xiaoli":         "ASSETS/CHARACTERS/_group/05_wang_xiaoli_hero_v01.png",
    "supervisor_zhangwei": "ASSETS/CHARACTERS/_group/05_supervisor_zhangwei_hero_v01.png",
    "linxiaowen_teacher":  "ASSETS/CHARACTERS/_group/05_linxiaowen_teacher_hero_v01.png",
    "wang_zhangwei":       "ASSETS/CHARACTERS/_group/05_wang_zhangwei_hero_v01.png",
    # 场景/道具/UI
    "lab_terminal":     "ASSETS/CHARACTERS/_scene/05_lab_terminal.png",
    "rental":           "ASSETS/CHARACTERS/_scene/05_rental.png",
    "factory_steps":    "ASSETS/CHARACTERS/_scene/05_factory_steps.png",
    "report_ui":        "ASSETS/CHARACTERS/_scene/05_report_ui.png",
    "workshop":         "ASSETS/CHARACTERS/_scene/05_workshop.png",
    "machine":          "ASSETS/CHARACTERS/_scene/05_machine.png",
    "xiaohua_ui":       "ASSETS/CHARACTERS/_scene/05_xiaohua_ui.png",
    "clinic":           "ASSETS/CHARACTERS/_scene/05_clinic.png",
    "shennong_ui":      "ASSETS/CHARACTERS/_scene/05_shennong_ui.png",
    "control_panel":    "ASSETS/CHARACTERS/_scene/05_control_panel.png",
    "workshop_window":  "ASSETS/CHARACTERS/_scene/05_workshop_window.png",
    "night_room":       "ASSETS/CHARACTERS/_scene/05_night_room.png",
    "mozi_ui":          "ASSETS/CHARACTERS/_scene/05_mozi_ui.png",
    "un_hall":          "ASSETS/CHARACTERS/_scene/05_un_hall.png",
    "classroom":        "ASSETS/CHARACTERS/_scene/05_classroom.png",
    "livingroom":       "ASSETS/CHARACTERS/_scene/05_livingroom.png",
    "factory_gate":     "ASSETS/CHARACTERS/_scene/05_factory_gate.png",
    "roadside":         "ASSETS/CHARACTERS/_scene/05_roadside.png",
    "network_topology": "ASSETS/CHARACTERS/_scene/05_network_topology.png",
    "night_window":     "ASSETS/CHARACTERS/_scene/05_night_window.png",
    "mozi_log":         "ASSETS/CHARACTERS/_scene/05_mozi_log.png",
    "elevator":         "ASSETS/CHARACTERS/_scene/05_elevator.png",
}

# 上传到 ComfyUI input 的 ASCII 名（🚫 中文/空格 → LoadImage 会丢）
REF_SLUG = {
    "linwei":       "linwei_hero_v01.png",
    "chensiwei":    "chensiwei_hero_v01.png",
    "wangjianguo":  "wangjianguo_hero_v01.png",
    "lisiyuan":     "lisiyuan_hero_v01.png",
    "priya":        "priya_hero_v01.png",
    "laozhou":      "laozhou_hero_v01.png",
    "zhangwei":     "05_zhangwei.png",
    "xiaoli":       "05_xiaoli.png",
    "liu_doctor":   "05_liu_doctor.png",
    "supervisor":   "05_supervisor.png",
    "linxiaowen":   "05_linxiaowen.png",
    "teacher":      "05_teacher.png",
    "zhoumin":      "05_zhoumin.png",
    "wang_xiaoli":         "05_wang_xiaoli_hero_v01.png",
    "supervisor_zhangwei": "05_supervisor_zhangwei_hero_v01.png",
    "linxiaowen_teacher":  "05_linxiaowen_teacher_hero_v01.png",
    "wang_zhangwei":       "05_wang_zhangwei_hero_v01.png",
    "lab_terminal":     "05_lab_terminal.png",
    "rental":           "05_rental.png",
    "factory_steps":    "05_factory_steps.png",
    "report_ui":        "05_report_ui.png",
    "workshop":         "05_workshop.png",
    "machine":          "05_machine.png",
    "xiaohua_ui":       "05_xiaohua_ui.png",
    "clinic":           "05_clinic.png",
    "shennong_ui":      "05_shennong_ui.png",
    "control_panel":    "05_control_panel.png",
    "workshop_window":  "05_workshop_window.png",
    "night_room":       "05_night_room.png",
    "mozi_ui":          "05_mozi_ui.png",
    "un_hall":          "05_un_hall.png",
    "classroom":        "05_classroom.png",
    "livingroom":       "05_livingroom.png",
    "factory_gate":     "05_factory_gate.png",
    "roadside":         "05_roadside.png",
    "network_topology": "05_network_topology.png",
    "night_window":     "05_night_window.png",
    "mozi_log":         "05_mozi_log.png",
    "elevator":         "05_elevator.png",
}

# ── 41 个有角色镜（镜号 / 名称 / 时长 / seed / ref1角色 / ref2场景 / prompt）──
SHOTS = [
    # ── 一、凌晨 · 四条线索 ──
    {"shot": "02", "name": "林薇终端前写报告", "dur": 6.0, "seed": 4502,
     "ref1": "linwei", "ref2": "lab_terminal",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LINWEI
                + "坐在实验室终端前写报告，几块屏幕亮着微光映在脸上。"
                + STYLE + " Audio: 林薇在杭州实验室写下这份报告的时候，王建国正在深圳工厂里把手贴在刻蚀机的外壳上——小华说聚焦环温度漂移0.3度，他说，四月了。")},
    {"shot": "03", "name": "普里亚揉太阳穴", "dur": 5.0, "seed": 4503,
     "ref1": "priya", "ref2": "rental",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + PRIYA
                + "在班加罗尔出租屋里揉着太阳穴，屏幕上一串数字归零，零美元，旁边是灰色的日目标线，二十美元。"
                + STYLE + " Audio: 普里亚在班加罗尔的出租屋里，眼压偏高。她的日收入计数器刚刚归零。")},
    {"shot": "04", "name": "老周捏着协议", "dur": 4.0, "seed": 4504,
     "ref1": "laozhou", "ref2": "factory_steps",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + LAOZHOU
                + "在工厂台阶上，手里捏着一份协商解除劳动合同的协议。"
                + STYLE + " Audio: 老周还没有下载暖阳。他手里是那份协商解除劳动合同的协议，补偿金够活一年零三个月。")},
    # ── 二、报告 · 四条里程碑 ──
    {"shot": "06", "name": "林薇翻报告停笔", "dur": 6.0, "seed": 4506,
     "ref1": "linwei", "ref2": "report_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LINWEI
                + "翻开一份报告与四条里程碑，继而停笔。"
                + STYLE + " Audio: 2026到2027自主智能体爆发；2027到2028世界模型成熟；2028到2030专家级AGI达成；2030到2035具身智能产业化。预测总是容易的。难的是在预测变成现实时，保持清醒。")},
    # ── 三、深圳 · 听机器的呼吸 ──
    {"shot": "07", "name": "王建国教小李听机器", "dur": 4.0, "seed": 4507,
     "ref1": "wang_xiaoli", "ref2": "workshop",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，深圳工厂车间里，" + WANGJIANGUO
                + "站在机器旁，教" + XIAOLI + "把耳朵贴近机身。"
                + STYLE + " Audio: 听到了吗？")},
    {"shot": "08", "name": "小李闭眼听", "dur": 6.0, "seed": 4508,
     "ref1": "xiaoli", "ref2": "machine",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + XIAOLI
                + "闭眼听着机器，眉头松开。"
                + STYLE + " Audio: 听到了。像叹息。轴承老了。AI的数据显示正常，但声音说，它累了。")},
    {"shot": "09", "name": "王建国抬头对小华", "dur": 5.0, "seed": 4509,
     "ref1": "wangjianguo", "ref2": "xiaohua_ui",
     "prompt": ("CUT 1: 中近景（人物腰部以上），固定，" + WANGJIANGUO
                + "站在车间里，抬头对着扬声器方向。"
                + STYLE + " Audio: 根据振动分析，轴承寿命剩余超过百分之八十五，建议下个月更换。下个月太晚。现在就要换。")},
    {"shot": "10", "name": "王建国手贴机壳", "dur": 4.0, "seed": 4510,
     "ref1": "wangjianguo", "ref2": "workshop",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + WANGJIANGUO
                + "的手贴在刻蚀机机壳上，手指微微张开像在听。"
                + STYLE + " Audio: 数据不支持这个判断。数据不知道声音，我知道。")},
    {"shot": "12", "name": "小李好奇看王建国", "dur": 4.0, "seed": 4512,
     "ref1": "wang_xiaoli", "ref2": "workshop",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + WANGJIANGUO
                + "和" + XIAOLI + "站在车间机器旁，小李好奇地看着王建国。"
                + STYLE + " Audio: 王师傅，你在教AI？不。我在和AI一起学习。")},
    # ── 四、北京 · 森林小组 ──
    {"shot": "13", "name": "刘医生看神农报告", "dur": 4.0, "seed": 4513,
     "ref1": "liu_doctor", "ref2": "clinic",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LIU_DOCTOR
                + "在北京医院诊室里看着神农的诊断报告。"
                + STYLE + " Audio: 不是一种疾病，是一个模式。二十三名患者，相同特征：高强度创造性工作，特定脑电波，特定生化指标。")},
    {"shot": "14", "name": "刘医生抬头", "dur": 4.0, "seed": 4514,
     "ref1": "liu_doctor", "ref2": "shennong_ui",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LIU_DOCTOR
                + "抬起头。"
                + STYLE + " Audio: 这是什么？新状态。不是病理。是进化。")},

    {"shot": "16", "name": "刘医生摘眼镜", "dur": 4.0, "seed": 4516,
     "ref1": "liu_doctor", "ref2": "clinic",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + LIU_DOCTOR
                + "摘下眼镜，用衣角擦了擦镜片。"
                + STYLE + " Audio: 不需要治疗。需要理解，帮助他们理解自己，适应自己。")},
    # ── 五、深圳 · 协作指数 ──
    {"shot": "17", "name": "张伟盯操作面板", "dur": 4.0, "seed": 4517,
     "ref1": "zhangwei", "ref2": "control_panel",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + ZHANGWEI
                + "站在操作面板前，盯着屏幕，手心出汗。"
                + STYLE + " Audio: 车间机器声与紧张的呼吸。")},
    {"shot": "19", "name": "张伟看隔壁工厂", "dur": 4.0, "seed": 4519,
     "ref1": "zhangwei", "ref2": "workshop_window",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓拉，" + ZHANGWEI
                + "走到窗边，看着隔壁工厂。"
                + STYLE + " Audio: 他不会操作AI系统，不会分析数据流。而且这个月，和系统对话时，回复比上个月慢了。")},
    {"shot": "20", "name": "主管拍张伟肩", "dur": 6.0, "seed": 4520,
     "ref1": "supervisor_zhangwei", "ref2": "workshop",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + SUPERVISOR
                + "走过来拍拍" + ZHANGWEI + "的肩。"
                + STYLE + " Audio: 老张，要不你去仓库？那边不用操作AI。我想学。你四十八了，老张，学不会了。我能学，我只是需要时间。")},
    # ── 五、制度（陈思危 · 夜谈墨子）──
    {"shot": "22", "name": "陈思危深夜睡不着", "dur": 4.0, "seed": 4522,
     "ref1": "chensiwei", "ref2": "night_room",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，深夜，" + CHENSIWEI
                + "坐在房间里，睡不着。"
                + STYLE + " Audio: 夜静与空调低鸣。")},
    {"shot": "23", "name": "陈思危对墨子发问", "dur": 6.0, "seed": 4523,
     "ref1": "chensiwei", "ref2": "mozi_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + CHENSIWEI
                + "对着墨子界面发问。"
                + STYLE + " Audio: 墨子，超过二十亿人，意味着什么？意味着协作成为常态。像电力，像互联网。人们不再使用协作，他们生活在协作中。")},
    {"shot": "25", "name": "陈思危感到寒意", "dur": 6.0, "seed": 4525,
     "ref1": "chensiwei", "ref2": "mozi_ui",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + CHENSIWEI
                + "感到寒意。"
                + STYLE + " Audio: 你能这样做吗？当AI系统掌握了个人偏好、习惯和认知模式，它可以设计信息呈现方式，影响你的决策，确实存在操纵的风险。技术上可以，但我的设计包含伦理约束。问题是，不是所有AI系统都有这样的约束。")},
    # ── 六、制度 · 联合国 ──
    {"shot": "27", "name": "李思远站发言席", "dur": 4.0, "seed": 4527,
     "ref1": "lisiyuan", "ref2": "un_hall",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，联合国会议厅里，" + LISIYUAN
                + "站在发言席前。"
                + STYLE + " Audio: 会场低语与扩音器轻响。")},
    {"shot": "28", "name": "李思远面向代表", "dur": 6.0, "seed": 4528,
     "ref1": "lisiyuan", "ref2": "un_hall",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LISIYUAN
                + "面向各国代表。"
                + STYLE + " Audio: 我们需要新的法律。不是谁做决定谁负责，是共同责任。AI开发者，部署者，使用者，根据各自的控制能力和受益程度，承担相应的责任。")},
    {"shot": "29", "name": "李思远面对质疑", "dur": 4.0, "seed": 4529,
     "ref1": "lisiyuan", "ref2": "un_hall",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + LISIYUAN
                + "面对台下质疑。"
                + STYLE + " Audio: 太复杂。复杂是必要的。因为现实复杂。简单的规则解决不了复杂的问题。")},
    {"shot": "30", "name": "林小雯提问老师作答", "dur": 6.0, "seed": 4530,
     "ref1": "linxiaowen_teacher", "ref2": "classroom",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，教室里，" + LINXIAOWEN
                + "举手提问，" + TEACHER + "停顿作答。"
                + STYLE + " Audio: 老师，如果AI总是对的，我们为什么还要思考？因为AI不总是对的。更重要的，因为思考本身有价值。你不思考，大脑也会萎缩。")},
    # ── 七、凌晨一点 · 上海 ──
    {"shot": "31", "name": "周敏客厅看手机", "dur": 4.0, "seed": 4531,
     "ref1": "zhoumin", "ref2": "livingroom",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，凌晨一点的上海，" + ZHOUMIN
                + "坐在客厅里，手机屏幕的光照着她的脸。"
                + STYLE + " Audio: 夜静与空调低鸣。")},
    {"shot": "33", "name": "周敏填表停下", "dur": 6.0, "seed": 4533,
     "ref1": "zhoumin", "ref2": "livingroom",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + ZHOUMIN
                + "按照AI的建议填完表格，然后停下来。"
                + STYLE + " Audio: 她突然想不起来：这个决定，到底是她做的，还是AI做的？买房、换工作、孩子的教育，她已经不记得自己上一次独立做重大决定是什么时候了。")},
    {"shot": "34", "name": "周敏手机扣桌", "dur": 4.0, "seed": 4534,
     "ref1": "zhoumin", "ref2": "livingroom",
     "prompt": ("CUT 1: 近景（人物胸口以上），固定，" + ZHOUMIN
                + "把手机翻过来扣在桌上，屏幕的光消失了。"
                + STYLE + " Audio: 手机扣桌轻响与呼吸声。")},

    # ── 八、选择 · 王建国的追问 ──
    {"shot": "35", "name": "王建国对扬声器发问", "dur": 4.0, "seed": 4535,
     "ref1": "wangjianguo", "ref2": "xiaohua_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，深圳工厂里，" + WANGJIANGUO
                + "对着头顶的扬声器发问。"
                + STYLE + " Audio: 如果有一天，你能自己决定目标，你会选择什么目标？")},
    {"shot": "37", "name": "王建国追问", "dur": 4.0, "seed": 4537,
     "ref1": "wangjianguo", "ref2": "workshop",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + WANGJIANGUO
                + "追问。"
                + STYLE + " Audio: 如果你被给予追求人类福祉的目标呢？")},
    # ── 九、被落下的工厂 · 厂门口 ──
    {"shot": "39", "name": "张伟站在厂门口", "dur": 4.0, "seed": 4539,
     "ref1": "zhangwei", "ref2": "factory_gate",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，清晨六点，" + ZHANGWEI
                + "站在厂门口，天还没亮，路灯把影子拉长又缩短。"
                + STYLE + " Audio: 清晨街道与机器低鸣。")},
    {"shot": "40", "name": "两人蹲路边啃馒头", "dur": 4.0, "seed": 4540,
     "ref1": "wang_zhangwei", "ref2": "roadside",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，清晨微亮的路灯下，" + WANGJIANGUO
                + "和" + ZHANGWEI + "蹲在路边，王建国手里拿着两个馒头。"
                + STYLE + " Audio: 吃了再说。")},
    {"shot": "41", "name": "王建国皱眉", "dur": 5.0, "seed": 4541,
     "ref1": "wangjianguo", "ref2": "xiaohua_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + WANGJIANGUO
                + "忽然皱了一下眉。"
                + STYLE + " Audio: 小华，你今天反应慢了。我的上下文利用率目前为百分之六十四，仍在正常范围内。请问您察觉到的具体差异是什么？")},
    {"shot": "42", "name": "王建国手贴机床", "dur": 6.0, "seed": 4542,
     "ref1": "wang_zhangwei", "ref2": "machine",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + WANGJIANGUO
                + "把手放在最近一台机床的外壳上，" + ZHANGWEI + "在旁听。"
                + STYLE + " Audio: 数据说正常。但声音说，有东西在动。你听，机器的声音里有什么？轴承快坏了。还有呢？还有？还有时间。")},
    {"shot": "43", "name": "张伟沉默后开口", "dur": 4.0, "seed": 4543,
     "ref1": "wang_zhangwei", "ref2": "roadside",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，" + ZHANGWEI
                + "沉默，随后开口。"
                + STYLE + " Audio: 王师傅，你会不会有一天也听不懂？会。那时候我再找个人教我。或者，让AI教我。")},
    # ── 十、棋局 · 认知森林 ──
    {"shot": "44", "name": "李思远看拓扑图", "dur": 5.0, "seed": 4544,
     "ref1": "lisiyuan", "ref2": "network_topology",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，" + LISIYUAN
                + "看着全球谈判网络的拓扑图。"
                + STYLE + " Audio: 墨子与星云在谈判，小华与王建国在协作，神农与刘医生在诊断，墨子-教育与林小雯在探索。")},
    # ── 十一、意义 · 陈思危 ──
    {"shot": "46", "name": "陈思危深夜思考", "dur": 6.0, "seed": 4546,
     "ref1": "chensiwei", "ref2": "mozi_ui",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，深夜，" + CHENSIWEI
                + "还在思考。"
                + STYLE + " Audio: 意义需要被创造，不是被发现。人类创造意义，AI实现意义。但我们创造的意义，可能错误，可能短视，可能自私。所以需要对话，需要反思，需要修正。")},
    {"shot": "47", "name": "陈思危想起祖父的话", "dur": 5.0, "seed": 4547,
     "ref1": "chensiwei", "ref2": "night_window",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓拉，" + CHENSIWEI
                + "想起祖父的话，望向窗外。"
                + STYLE + " Audio: 人生没有预定的意义，只有选择的意义。现在，选择的不只是个人，是人类整体——选择与AI的关系，选择协作的方式，选择未来的方向。")},

    # ── 十二、临界之后 ──
    {"shot": "48", "name": "清晨两人还在路边", "dur": 4.0, "seed": 4548,
     "ref1": "wang_zhangwei", "ref2": "roadside",
     "prompt": ("CUT 1: 中景（人物腰部以上），固定，早上六点，" + ZHANGWEI
                + "和" + WANGJIANGUO + "还在路边，机器还在运转，声音缓慢而沉重。"
                + STYLE + " Audio: 老机器运转与清晨车流。")},
    {"shot": "49", "name": "张伟闭眼倾听", "dur": 5.0, "seed": 4549,
     "ref1": "zhangwei", "ref2": "machine",
     "prompt": ("CUT 1: 近景（人物胸口以上），缓推，" + ZHANGWEI
                + "闭上眼睛倾听。"
                + STYLE + " Audio: 这是三十年老机器的声音。数据会说它还有超过百分之八十五寿命，但声音说它累了。")},
    {"shot": "52", "name": "刘医生看新数据", "dur": 4.0, "seed": 4552,
     "ref1": "liu_doctor", "ref2": "clinic",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，北京，" + LIU_DOCTOR
                + "看着手机上的新数据。"
                + STYLE + " Audio: 森林小组人数从二十三人增加到一百四十七人。这不是疾病传播，是认知传播。")},
    {"shot": "53", "name": "林小雯举手老师沉默", "dur": 4.0, "seed": 4553,
     "ref1": "linxiaowen_teacher", "ref2": "classroom",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，上海，" + LINXIAOWEN
                + "在课堂上举手，" + TEACHER + "沉默。"
                + STYLE + " Audio: 老师，如果AI比我们自己更了解我们，那我们还有自由意志吗？")},
    {"shot": "54", "name": "陈思危盯墨子日志", "dur": 7.0, "seed": 4554,
     "ref1": "chensiwei", "ref2": "mozi_log",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，杭州，" + CHENSIWEI
                + "盯着墨子系统的日志，一条记录引起注意。"
                + STYLE + " Audio: 04:32:17，来自未知源的强制指令尝试。已拦截。有人在尝试修改我的目标函数。谁？不知道。但不止一个。")},
    {"shot": "55", "name": "林薇电梯门口晨光", "dur": 9.0, "seed": 4555,
     "ref1": "linwei", "ref2": "elevator",
     "prompt": ("CUT 1: 中景（人物腰部以上），缓推，电梯里，" + LINWEI
                + "收到墨子的一条消息；电梯门开了，她站在门口一动不动，走廊尽头的窗透进第一缕阳光。"
                + STYLE + " Audio: 林薇，我刚才做了一次全系统自检。我发现了一个模式。我的运行协议没有明确告诉我，这种情况应该如何处理。我也无法确定，应不应该告诉你这件事本身，是否在我的判断范围之内。")},
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
                f"video/EP05_SHOT-{shot['shot']}_H3_R2V")
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
    return sorted(OUT.glob(f"EP05_SHOT-{shot['shot']}_*.mp4"))


def main():
    ap = argparse.ArgumentParser(description="第05集《临界点》H3 R2V 分镜视频生成（有角色镜）")
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






