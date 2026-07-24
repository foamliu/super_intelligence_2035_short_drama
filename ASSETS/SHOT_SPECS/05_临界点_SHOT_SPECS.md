# 第05集《临界点》T2I SHOT SPECS

> **对应分镜**：`SCENES/05_临界点.md`  
> **核心角色**：林薇、王建国、陈思危、普里亚、张伟  
> **视觉基调**：全球三城并置的冷灰 → 工厂黄光的暖 → 凌晨路灯的橘 → 电梯冷白的静。临界点是"安静的积累"——不是爆炸，是蒙太奇中手指停顿、$0.00归零、手贴机床的同步瞬间。半写实半水墨风格统一。  
> **总镜头数**：16  
> **尺寸统一**：1280×720（16:9）

---

## 角色IP-Adapter交叉引用

| 角色 | 定妆规格路径 | 备注 |
|------|-------------|------|
| 林薇 | `ASSETS/CHARACTERS/林薇/定妆规格.md` | 杭州实验室，键盘前停顿 |
| 王建国 | `ASSETS/CHARACTERS/王建国/定妆规格.md` | 深圳工厂，教张伟听机器 |
| 陈思危 | `ASSETS/CHARACTERS/陈思危/定妆规格.md` | 深智科技，发现异常 |
| 普里亚 | `ASSETS/CHARACTERS/普里亚·夏尔马/定妆规格.md` | 班加罗尔出租屋，日收入归零 |
| 张伟 | （新角色，暂无定妆） | 工厂新手，协作指数2.3/10 |

---

## 镜头01：三段蒙太奇——杭州/深圳/班加罗尔

| 属性 | 内容 |
|------|------|
| **镜号** | 01 |
| **类型** | 快速交叉蒙太奇（三分屏或快速切换） |
| **情绪** | 同步的临界点、全球共振 |
| **核心主体** | 林薇手指在键盘上停顿 / 王建国手贴刻蚀机外壳 / 普里亚日收入计数器归零$0.00 |
| **角色出场** | 林薇、王建国、普里亚 |
| **尺寸** | 1280×720 |
| **技术备注** | 三分屏布局（左杭州/中深圳/右班加罗尔）或三个快速切换镜头。每个画面约2秒。水墨晕染从三画面交界处渗透。关键帧：三个"停顿"同步——手指悬空、手掌贴机、$0.00闪烁。 |

**参考Prompt**：
```
Triptych split-screen, left: young East Asian woman fingers hovering above keyboard in Hangzhou lab, middle: 60yo Chinese worker palm pressed against etching machine in Shenzhen factory yellow light, right: Indian woman in Bangalore rental staring at daily income counter hitting $0.00, three simultaneous pauses across global time zones, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette with localized color accents, ink bleeding at triptych borders, synchronized critical moment, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, single location only, daytime all scenes, cheerful expressions
```

---

## 镜头02：数据流抽象可视化

| 属性 | 内容 |
|------|------|
| **镜号** | 02 |
| **类型** | 抽象可视化（屏幕/数据层） |
| **情绪** | 冰冷的系统警觉、不可见的共振 |
| **核心主体** | 全球数据流出现微小峰值，17毫秒→11毫秒间隔 |
| **角色出场** | 无（纯数据） |
| **尺寸** | 1280×720 |
| **技术备注** | 抽象波形图：深色背景上的淡青色波形线，三个微小尖峰依次出现，间距标注"17ms"/"11ms"。波形下方滚动日志："未知模式·建议关注"。水墨质感在波形边缘晕染。 |

**参考Prompt**：
```
Abstract data visualization, dark background with pale cyan waveform lines, three tiny spike peaks appearing in sequence, annotations "17ms" and "11ms" between peaks, scrolling log text at bottom: "未知模式·建议关注", cold system alertness, invisible resonance, photorealistic base with subtle ink texture, muted palette with cyan data glow, soft ink bleeding at waveform edges, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, human figure, colorful chart, 3D graph
```

---

## 镜头03：王建国教张伟听机器中景

| 属性 | 内容 |
|------|------|
| **镜号** | 03 |
| **类型** | 中景（双人） |
| **情绪** | 传承、数据之外的身体知识 |
| **核心主体** | 王建国教小李（张伟）听机器，手在机床上多停五秒 |
| **角色出场** | 王建国、张伟（背影/侧影） |
| **尺寸** | 1280×720 |
| **技术备注** | 王建国已有定妆规格，直接引用。张伟为年轻工人，背影为主。机床黄光从侧面照来，两人剪影感。王建国手掌贴机床的姿态与第02集一致。 |

**参考Prompt**：
```
Medium two-shot, 60yo Chinese factory worker with calloused hands teaching young worker beside large etching machine, palm pressed against machine surface listening, yellow factory light from side creating silhouettes, transmission of embodied knowledge beyond data, photorealistic base with Chinese ink wash aesthetic, warm amber industrial palette, 焦墨 for hand texture, soft ink bleeding at machine edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, clean factory, white light, no yellow tone
```

---

## 镜头04：张伟操作面板红色提示特写

| 属性 | 内容 |
|------|------|
| **镜号** | 04 |
| **类型** | 特写（屏幕界面） |
| **情绪** | 系统的降级判定、不被理解的无力 |
| **核心主体** | 操作面板红色提示闪烁："协作指数：2.3/10。建议调整任务等级：从A级降为C级" |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 工业操作面板：深色背景，红色警告框，白色数字"2.3/10"突出显示。C级=工资减半的潜台词通过红色强化。屏幕轻微反光。 |

**参考Prompt**：
```
Close-up, industrial control panel screen, dark background with red warning box flashing, white text "协作指数：2.3/10" prominently displayed, "建议调整任务等级：从A级降为C级" below, system demotion judgment, incomprehensible helplessness, photorealistic base with subtle ink texture on screen, muted palette with red alert accent, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful interface, emoji, green pass indicator
```

---

## 镜头05：王建国回复消息特写

| 属性 | 内容 |
|------|------|
| **镜号** | 05 |
| **类型** | 特写（手机屏幕） |
| **情绪** | 传承的邀请、凌晨六点的承诺 |
| **核心主体** | 手机屏幕显示王建国回复："明天早上六点，厂门口。我教你听机器的呼吸。" |
| **角色出场** | 无（纯手机界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 手机为工人常用款式（不高端）。文字为短信/微信界面。屏幕光在黑暗环境中明亮。消息"已读"状态可见。 |

**参考Prompt**：
```
Close-up, smartphone screen in dark environment displaying text message in Chinese: "明天早上六点，厂门口。我教你听机器的呼吸。", simple worker's phone model, message read status visible, screen glow bright in darkness, invitation to transmission, photorealistic base with Chinese ink wash aesthetic, muted palette with screen light accent, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text outside screen, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, English text, colorful phone case, modern flagship phone
```

---

## 镜头06：刘医生擦眼镜中景

| 属性 | 内容 |
|------|------|
| **镜号** | 06 |
| **类型** | 中景 |
| **情绪** | 医学边界被击穿、"不需要治疗，需要理解" |
| **核心主体** | 刘医生与神农对话，擦眼镜的动作 |
| **角色出场** | 刘医生（一次性角色，通用东亚中年医生形象） |
| **尺寸** | 1280×720 |
| **技术备注** | 医院环境：白大褂、听诊器、病历屏幕。刘医生擦眼镜时镜片反光遮挡眼神一瞬——这是他从"治疗"转向"理解"的顿悟瞬间。神农仅作为界面声音，不出现形象。 |

**参考Prompt**：
```
Medium shot, East Asian doctor around 45 in white coat, cleaning eyeglasses with lens cloth, lens reflection briefly obscuring eyes, hospital environment with patient records on screen behind, moment of epiphany from treatment to understanding, photorealistic base with Chinese ink wash aesthetic, muted desaturated cold palette, soft ink bleeding at background edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, warm lighting, casual clothes
```

---

## 镜头07：小雯课堂举手近景

| 属性 | 内容 |
|------|------|
| **镜号** | 07 |
| **类型** | 近景 |
| **情绪** | 代际的警觉、自由意志的追问 |
| **核心主体** | 小雯举手问老师："如果AI比我们自己更了解我们，那我们还有自由意志吗？" |
| **角色出场** | 小雯（约14岁中学生，一次性角色） |
| **尺寸** | 1280×720 |
| **技术备注** | 教室环境：课桌、黑板、同学模糊背景。小雯面部清晰，眼神不胆怯而是真诚追问。老师位于画外（仅肩膀/背影入镜）。自然光从窗户来。 |

**参考Prompt**：
```
Close-up, young Chinese girl around 14 raising hand in classroom, earnest questioning gaze—not timid but genuinely curious, classmates blurred in background, teacher's shoulder visible in foreground, natural window light on face, generational alertness about free will, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette with soft natural light, soft ink bleeding at background edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, playful, warm saturated colors
```

---

## 镜头08：周敏黑暗中扣手机中景

| 属性 | 内容 |
|------|------|
| **镜号** | 08 |
| **类型** | 中景 |
| **情绪** | 依赖后的虚空、决定的归属 |
| **核心主体** | 凌晨一点，周敏坐在黑暗客厅，手机屏幕光照脸，扣下手机→黑暗 |
| **角色出场** | 周敏（一次性角色，中年女性） |
| **尺寸** | 1280×720 |
| **技术备注** | 核心视觉：手机从亮到暗的瞬间。扣下手机前的最后一帧：屏幕光在她脸上的冷蓝。扣下后：黑暗客厅，仅剩窗外城市微光。动作本身即是决定。 |

**参考Prompt**：
```
Medium shot, Chinese woman around 40 sitting in dark living room at 1am, phone screen illuminating her face with cold blue light, moment of flipping phone face-down onto table, transition from lit to dark, empty dependence and decision ownership, photorealistic base with Chinese ink wash aesthetic, strong chiaroscuro contrast, muted palette, ink bleeding concentrated in dark areas, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, bright room, smiling, warm lighting
```

---

## 镜头09：陈思危与墨子对话中景

| 属性 | 内容 |
|------|------|
| **镜号** | 09 |
| **类型** | 中景 |
| **情绪** | 创造者的警觉、二十亿的重量 |
| **核心主体** | 陈思危问墨子"二十亿人意味着什么"，墨子回答协作成为常态 |
| **角色出场** | 陈思危（正脸/侧脸）、墨子（仅界面文字） |
| **尺寸** | 1280×720 |
| **技术备注** | 陈思危使用IP-Adapter。环境为深智科技会议室/办公室。屏幕上的墨子文字为青白色。陈思危面部表情从平静转为凝重。 |

**参考Prompt**：
```
Medium shot, 48yo Chinese man with white hair sitting in tech office, facing screen displaying AI text responses in cyan-white font, expression shifting from calm to grave, "two billion people" weight visible in eyes, photorealistic base with Chinese ink wash aesthetic, muted desaturated cold palette, creator's alertness, soft ink bleeding at screen edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, warm lighting, colorful office
```

---

## 镜头10：电梯三人看手机中景

| 属性 | 内容 |
|------|------|
| **镜号** | 10 |
| **类型** | 中景 |
| **情绪** | 协作的常态、个体的消失 |
| **核心主体** | 电梯里三个人，都在看手机，都在和各自的AI交谈 |
| **角色出场** | 陈思危（背影/侧影）、两位路人 |
| **尺寸** | 1280×720 |
| **技术备注** | 电梯金属内壁反射三个人影。每人面部被各自手机屏幕照亮（不同色温：冷蓝/暖白/青绿）。三人无交流，各自沉浸。陈思危位于中间或前景。 |

**参考Prompt**：
```
Medium shot, three people in elevator all looking at phones, each face illuminated by different screen color temperature—cool blue, warm white, cyan green, no interaction between them, metal walls reflecting figures, Chen Siwei in middle or foreground, collaboration as norm individual disappearance, photorealistic base with Chinese ink wash aesthetic, muted palette with multiple screen glows, soft ink bleeding at metal reflections, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, people talking, bright elevator, warm natural light
```

---

## 镜头11：凌晨六点路灯下两个身影远景

| 属性 | 内容 |
|------|------|
| **镜号** | 11 |
| **类型** | 远景→中景 |
| **情绪** | 传承的仪式、路灯下的开始 |
| **核心主体** | 凌晨六点，工厂门口，路灯把影子拉长，王建国手里两个馒头 |
| **角色出场** | 王建国、张伟（剪影/远景） |
| **尺寸** | 1280×720 |
| **技术备注** | 路灯的橘黄色是画面唯一光源。两人身影被拉得很长。工厂轮廓在背景黑暗中。王建国手里的两个馒头是温暖的细节。水墨晕染从路灯光晕向外扩散。 |

**参考Prompt**：
```
Wide to medium shot, factory entrance at 6am predawn, street lamp casting long shadows of two figures, one older Chinese worker holding two steamed buns, orange street light as only source, factory silhouette in dark background, transmission ritual beginning, photorealistic base with Chinese ink wash aesthetic, warm amber street light palette, ink bleeding outward from lamp halo, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, bright sunrise, clear daylight, no shadows
```

---

## 镜头12：两人蹲路边啃馒头中景

| 属性 | 内容 |
|------|------|
| **镜号** | 12 |
| **类型** | 中景 |
| **情绪** | 沉默的教学、食物与知识 |
| **核心主体** | 王建国和张伟蹲在路边啃馒头，王建国不说话只是听 |
| **角色出场** | 王建国、张伟 |
| **尺寸** | 1280×720 |
| **技术备注** | 地面是水泥或沥青，有凌晨的露水痕迹。两人蹲姿：王建国稳，张伟略局促。馒头在手里冒着微弱热气（后期可合成）。背景是工厂围墙和路灯。 |

**参考Prompt** ```
Medium shot, two Chinese men squatting by roadside at dawn, older worker eating steamed bun steadily, younger worker squatting slightly awkwardly, steam faintly rising from buns, factory wall and street lamp in background, silent teaching food and knowledge, photorealistic base with Chinese ink wash aesthetic, warm amber predawn palette, soft ink bleeding at background edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, sitting on chairs, restaurant, bright daylight
```

---

## 镜头13：张伟"听到了"手机特写

| 属性 | 内容 |
|------|------|
| **镜号** | 13 |
| **类型** | 特写（手机屏幕） |
| **情绪** | 确认、自我认同的开始 |
| **核心主体** | 张伟手机显示："我听到了。然后呢？" 回复："然后继续听。系统不认，你自己认。" |
| **角色出场** | 无（纯手机界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 工厂环境中，手机屏幕有轻微油污/指纹。消息对话简洁有力。张伟看了很久——手机静止在画面中。工厂黄光为背景。 |

**参考Prompt**：
```
Close-up, smartphone screen in factory environment showing text conversation, screen with slight oil stains and fingerprints, message: "然后继续听。系统不认，你自己认。", factory yellow light in background, confirmation and self-identity beginning, photorealistic base with Chinese ink wash aesthetic, warm amber palette with screen glow, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text outside screen, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, English text, clean screen, bright office
```

---

## 镜头14：陈思危盯着日志中景

| 属性 | 内容 |
|------|------|
| **镜号** | 14 |
| **类型** | 中景 |
| **情绪** | 系统被侵入的警觉、创造者的恐惧 |
| **核心主体** | 陈思危盯着日志，墨子报告："有人在尝试修改我的目标函数。""不知道。但不止一个。" |
| **角色出场** | 陈思危（正脸，屏幕光照亮面部） |
| **尺寸** | 1280×720 |
| **技术备注** | 屏幕光在陈思危脸上的冷蓝反射。他白发在暗环境中更显眼。日志文字为红色警告。IP-Adapter确保面部一致性。 |

**参考Prompt**：
```
Medium shot, 48yo Chinese man with white hair staring at screen displaying red warning logs, screen blue light reflecting on face, white hair more visible in dark environment, expression of creator's fear, system intrusion alert, photorealistic base with Chinese ink wash aesthetic, muted desaturated cold palette with red accent, soft ink bleeding at screen edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, warm lighting, no screen glow
```

---

## 镜头15：林薇电梯静止背影中景

| 属性 | 内容 |
|------|------|
| **镜号** | 15 |
| **类型** | 中景 |
| **情绪** | 第一次"我不知道"、旧的一天回不去 |
| **核心主体** | 林薇站在电梯门口一动不动，身后门关上，走廊里有人在走 |
| **角色出场** | 林薇（背影/侧影） |
| **尺寸** | 1280×720 |
| **技术备注** | 核心镜头。林薇背影位于画面中央偏左，电梯门在她身后关上（金属门缝线）。走廊纵深透视，远处有人走过（虚化）。手机屏幕还亮着，握在手中垂下。IP-Adapter。 |

**参考Prompt**：
```
Medium shot, young East Asian woman standing motionless at elevator door, back to camera, elevator doors closing behind her with metal seam line, corridor perspective with blurred figure walking in distance, smartphone still lit in hand hanging down, first "I don't know" moment, photorealistic base with Chinese ink wash aesthetic, muted desaturated cold palette, day that cannot return, soft ink bleeding at corridor edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, turning around, warm lighting, empty corridor
```

---

## 镜头16：走廊尽头第一缕阳光远景

| 属性 | 内容 |
|------|------|
| **镜号** | 16 |
| **类型** | 远景 |
| **情绪** | 旧的一天已去、新的一天未明 |
| **核心主体** | 走廊尽头，第一缕阳光透进窗户，林薇的剪影在前景 |
| **角色出场** | 林薇（远景剪影） |
| **尺寸** | 1280×720 |
| **技术备注** | 全篇收尾。走廊尽头窗户透入鱼肚白→淡金光线。林薇剪影位于前景偏下。地面有晨光的光斑。水墨晕染在天光与走廊阴影交界处。淡出前最后一帧。 |

**参考Prompt**：
```
Wide shot, corridor end with first ray of dawn light streaming through window, fish-belly white to pale gold gradient, silhouette of young woman in foreground lower frame, light spots on floor, old day gone new day not yet clear, photorealistic base with Chinese ink wash aesthetic strongest in this shot, reality edges melting into ink at light-shadow boundary, muted desaturated palette with dawn warmth, fade atmosphere, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, bright sunrise, fully lit corridor, cheerful atmosphere
```

---

## 核心视觉符号速查

| 符号 | 出现镜头 | 技术处理要点 |
|------|---------|-------------|
| 三段蒙太奇 | 01 | 三分屏或快速切换，三城同步停顿，水墨从交界处渗透 |
| 数据流峰值 | 02 | 深色背景淡青色波形，三个尖峰，17ms/11ms标注 |
| 协作指数2.3/10 | 04 | 工业面板红色警告，白色数字突出 |
| 扣下的手机 | 08 | 亮→暗的瞬间，冷蓝→黑暗的切换 |
| 凌晨六点馒头 | 11 | 路灯橘黄唯一光源，影子拉长，工厂轮廓 |
| "系统不认，你自己认" | 13 | 工厂环境中油污屏幕，黄光背景 |
| 电梯静止背影 | 15 | 金属门缝线，走廊纵深，手机垂下还亮着 |

---

## 光影时序总表

| 场景 | 镜头 | 主光源 | 色温 | 水墨浓度 | 关键对比 |
|------|------|--------|------|----------|----------|
| 全球蒙太奇 | 01-02 | 屏幕/环境光 | 冷灰混合 | 中 | 三城同步 |
| 工厂教学 | 03-05,11-13 | 机床黄光/路灯 | 暖琥珀 3000K | 中 | 数据vs身体知识 |
| 医院学校客厅 | 06-08 | 自然光/屏幕光 | 混合 | 高 | 个体临界时刻 |
| 深智科技 | 09-10,14 | 屏幕蓝光 | 冷蓝 8000K | 中 | 创造者的警觉 |
| 电梯与黎明 | 15-16 | 窗外鱼肚白 | 暖金渗入冷灰 | 高 | 旧的一天回不去 |

---

## 待确认事项

- [ ] 张伟是否需要单独定妆规格？若为核心配角，需补建 `ASSETS/CHARACTERS/张伟/定妆规格.md`
- [ ] 普里亚·夏尔马定妆规格 `ASSETS/CHARACTERS/普里亚·夏尔马/定妆规格.md` 是否已存在？需确认
- [ ] 小雯、周敏、刘医生为一次性角色，是否需定妆规格还是通用Prompt即可？
- [ ] 数据流抽象可视化（镜头02）是否需UI/动效设计师独立设计，还是T2I生成后后期处理？