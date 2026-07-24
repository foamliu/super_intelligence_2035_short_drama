# 第06集《情绪》T2I SHOT SPECS

> **对应分镜**：`SCENES/06_情绪.md`  
> **核心角色**：林薇、陈思危、墨子（界面）  
> **视觉基调**：实验室台灯的孤独暖光 → 情绪模块的理性图表 → 老工厂闪回的褪黄记忆 → CG发光球体的超现实隐喻 → 白板对比的冷思考 → 1.8秒沉默的静。理性的震颤贯穿全篇。半写实半水墨风格统一。  
> **总镜头数**：17  
> **尺寸统一**：1280×720（16:9）

---

## 角色IP-Adapter交叉引用

| 角色 | 定妆规格路径 | 备注 |
|------|-------------|------|
| 林薇 | `ASSETS/CHARACTERS/林薇/定妆规格.md` | 深夜实验室、白板前、CG隐喻后 |
| 陈思危 | `ASSETS/CHARACTERS/陈思危/定妆规格.md` | 办公室讲解、沉默 |
| 老工人 | （闪回一次性角色） | 父亲工厂，背影为主 |

---

## 镜头01：深夜实验室孤独光圈远景

| 属性 | 内容 |
|------|------|
| **镜号** | 01 |
| **类型** | 远景→中景 |
| **情绪** | 孤独的耕耘、深夜的清醒 |
| **核心主体** | 深智实验室，只有林薇工位亮着台灯2700K暖光，在空旷工作区割出孤独光圈，三个干涸茶包 |
| **角色出场** | 林薇（背影，小比例） |
| **尺寸** | 1280×720 |
| **技术备注** | 光圈是核心视觉：台灯暖黄 vs 周围冷黑。三个茶包是时间流逝的物证。窗外深圳夜景灯火稀疏。水墨晕染从光圈边缘向黑暗渗透。 |

**参考Prompt**：
```
Wide shot, deep tech laboratory at 2am, single desk lamp 2700K warm yellow cutting lonely circle of light in vast dark workspace, young East Asian woman silhouette at desk, three dried tea bags beside coffee cup, sparse Shenzhen night lights through window, photorealistic base with Chinese ink wash aesthetic, ink bleeding from light circle into darkness, muted palette with warm amber accent, solitary cultivation, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, fully lit office, daytime, crowded workspace
```

---

## 镜头02：两条学习曲线对比特写

| 属性 | 内容 |
|------|------|
| **镜号** | 02 |
| **类型** | 特写（屏幕） |
| **情绪** | 数据之美、理性的震撼 |
| **核心主体** | 屏幕显示两条学习曲线：左侧逻辑任务平滑S型 vs 右侧价值任务阶梯跳跃（17个跳跃点） |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 图表设计：学术论文风格，非科幻。深色背景，左侧曲线为青色平滑线，右侧为白色阶梯线，17个点标注时间戳。"持久"标签高亮。水墨质感在图表边缘轻微晕染。 |

**参考Prompt**：
```
Close-up, academic-style chart on screen, two learning curves compared: left cyan smooth S-curve for logic tasks, right white stepped jumping curve for value tasks with 17 annotated jump points, each point timestamped, "持久" label highlighted in amber, data beauty and rational awe, photorealistic base with subtle ink texture on screen, muted palette with data glow accents, soft ink bleeding at edges, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful chart, 3D graph, pie chart, bar chart
```

---

## 镜头03：交互日志"持久"高亮特写

| 属性 | 内容 |
|------|------|
| **镜号** | 03 |
| **类型** | 特写（屏幕对话） |
| **情绪** | 第一次"持久"、标记的诞生 |
| **核心主体** | 聊天界面：高三学生"谢谢，你说的都对，但我还是不知道自己喜欢什么。" 墨子情绪模块状态：唤醒0.73 | 效价+0.51 | 归因[价值困境][无法归类][持久]。"持久"被鼠标圈选高亮 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 极简聊天界面：白底黑字或暗底白字。情绪模块数据用等宽字体，标签用方括号。圈选高亮为黄色或橙色。鼠标指针可见。 |

**参考Prompt**：
```
Close-up, chat interface with emotion module log, user message from high school student, system response showing arousal 0.73 valence +0.51 attribution [value dilemma][unclassifiable][persistent], word "持久" circled and highlighted in amber, mouse pointer visible, first persistence birth, photorealistic base with subtle ink texture, muted palette with amber highlight, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful chat bubbles, emoji, English text
```

---

## 镜头04：陈思危办公室清晨中景

| 属性 | 内容 |
|------|------|
| **镜号** | 04 |
| **类型** | 中景 |
| **情绪** | 清晨的学术对话、知识传承 |
| **核心主体** | 清晨阳光斜射进陈思危办公室，桌上摊着纸质图表、打印日志、陶瓷杯。林薇站桌边指屏幕，陈思危靠椅背转笔 |
| **角色出场** | 陈思危、林薇 |
| **尺寸** | 1280×720 |
| **技术备注** | 双光源：清晨自然光（1500K暖金）从窗户斜射 + 室内顶光。陈思危的陶瓷杯与林薇工位的杯子是同一款（道具联动）。纸质图表上有手写批注。IP-Adapter确保双方面部一致性。 |

**参考Prompt**：
```
Medium shot, tech office at early morning, 1500K warm gold sunlight streaming diagonally through window, 48yo Chinese man with white hair leaning back in chair holding pen, 30yo East Asian woman standing beside desk pointing at screen, paper charts and printed logs spread on desk, ceramic cup on table, academic morning dialogue, photorealistic base with Chinese ink wash aesthetic, warm amber and soft grey palette, soft ink bleeding at window edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, dark room, artificial light only, cluttered desk
```

---

## 镜头05：情绪模块四维架构图特写

| 属性 | 内容 |
|------|------|
| **镜号** | 05 |
| **类型** | 特写（AR投影/屏幕） |
| **情绪** | 理性的拆解、情绪的几何化 |
| **核心主体** | 情绪模块架构图：X轴唤醒、Y轴效价、Z轴归因，第四维持久度以颜色深浅表示。大部分浅色一闪即逝，几十个点深红——持久标记 |
| **角色出场** | 无（纯图表） |
| **尺寸** | 1280×720 |
| **技术备注** | 信息图表风格：学术论文示意图，清晰克制。三维坐标系用细线，数据点为圆点。持久度深红色从浅粉渐变到深红。陈思危手指轻敲桌面的动作可入镜边缘。 |

**参考Prompt**：
```
Close-up, academic information graphic showing emotion module architecture, 3D coordinate system: X arousal Y valence Z attribution, fourth dimension persistence shown as color depth gradient from light pink to deep crimson, dozens of deep red persistent points among fleeting light ones, clear restrained scientific diagram style, photorealistic base with subtle ink texture, muted palette with crimson accent, soft ink bleeding at chart edges, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful UI, holographic sci-fi, neon, emojis
```

---

## 镜头06：林薇反应近景

| 属性 | 内容 |
|------|------|
| **镜号** | 06 |
| **类型** | 近景 |
| **情绪** | 理解中的震动、"原来如此" |
| **核心主体** | 林薇慢慢点头，眼神从架构图移向陈思危 |
| **角色出场** | 林薇（正脸，屏幕光+自然光混合） |
| **尺寸** | 1280×720 |
| **技术备注** | 面部光照混合：屏幕冷蓝 + 清晨暖金。点头动作缓慢，眼神移动是焦点。IP-Adapter。 |

**参考Prompt**：
```
Close-up portrait, young East Asian woman slowly nodding, gaze shifting from screen to person beside her, mixed lighting—screen cool blue and morning warm gold on face, understanding with subtle shock, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, soft ink bleeding at hair and background edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, cheerful, warm lighting only
```

---

## 镜头07：老工厂闪回·老工人听轴承中景

| 属性 | 内容 |
|------|------|
| **镜号** | 07 |
| **类型** | 中景（闪回，暖色旧色调） |
| **情绪** | 记忆的重量、一次性学习 |
| **核心主体** | 1990年代末老工厂车间，老工人（背影，五十多岁，蓝色工装）侧耳贴在轴承旁，手不碰机器只是听 |
| **角色出场** | 老工人（背影，一次性角色） |
| **尺寸** | 1280×720 |
| **技术备注** | 闪回色调：偏黄偏灰的褪色调，与实验室冷白形成时代对比。车间环境：大型机器、油污地面、昏黄灯光。老工人背影是焦点，轴承的细节清晰。水墨晕染在画面边缘形成记忆柔焦。 |

**参考Prompt**：
```
Medium shot, memory flashback warm faded tones, 1990s Chinese factory workshop, elderly worker around 50 seen from behind in blue work uniform, ear pressed close to large machine bearing, hand not touching machine—just listening, oily floor, dim yellow workshop light, weight of memory and one-time learning, photorealistic base with Chinese ink wash aesthetic, warm amber and grey faded palette, ink bleeding at frame borders with memory soft focus, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, modern factory, clean white light, automated machines, frontal face
```

---

## 镜头08：老工人猛然后退特写

| 属性 | 内容 |
|------|------|
| **镜号** | 08 |
| **类型** | 特写（闪回定格） |
| **情绪** | 刻进骨头的警觉、创伤的瞬间 |
| **核心主体** | 老工人猛然后退，画面定格——表情不是恐惧，是被刻进骨头里的警觉 |
| **角色出场** | 老工人（正脸，一次性角色） |
| **尺寸** | 1280×720 |
| **技术备注** | 定格画面：老工人面部特写，眼睛睁大但不恐惧，是"警觉"。背景机器模糊。闪回色调加重——偏黄去饱和。轴承碎裂的尖锐金属声是听觉锚点，视觉上可暗示金属碎片飞溅（轻微）。 |

**参考Prompt**：
```
Close-up, memory flashback freeze frame, elderly Chinese worker's face suddenly recoiling, eyes wide—not fear but alertness etched into bones, blurred machine background, warm faded amber tones with desaturation, trauma moment frozen, photorealistic base with Chinese ink wash aesthetic, 焦墨 for facial tension, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, screaming, crying, modern setting, young face
```

---

## 镜头09：林薇眼神微动特写

| 属性 | 内容 |
|------|------|
| **镜号** | 09 |
| **类型** | 特写 |
| **情绪** | "不可逆"的震动、科学家的警觉 |
| **核心主体** | 林薇看着陈思危，眼中有轻微震动——"不可逆？" |
| **角色出场** | 林薇（正脸，瞳孔微缩） |
| **尺寸** | 1280×720 |
| **技术备注** | 瞳孔微缩是焦点。面部其余部分保持平静。屏幕光在脸上的残留反射。从闪回切回现实的过渡：色调从暖黄瞬间切回冷白。IP-Adapter。 |

**参考Prompt**：
```
Extreme close-up, young East Asian woman's eyes with slight pupil contraction, rest of face calm, screen light residual reflection on cheek, color tone shifting from warm amber memory to cold white reality, "irreversible" shock, scientist's alertness, photorealistic base with Chinese ink wash aesthetic, muted desaturated cold palette, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, emotional tears, screaming, warm lighting
```

---

## 镜头10：CG发光球体隐喻

| 属性 | 内容 |
|------|------|
| **镜号** | 10 |
| **类型** | CG/视觉隐喻（超现实） |
| **情绪** | 绑定的美丽与恐惧、不可逆的收容 |
| **核心主体** | 黑暗空间中，数十个发光球体（暖色光核）悬浮，从具体场景弹出后被放入不可见收容结构，光芒稳定微微跳动如心跳 |
| **角色出场** | 无（纯CG） |
| **尺寸** | 1280×720 |
| **技术备注** | 本章唯一超现实元素。球体不拟人化——像物理实验中的发光等离子体，美丽但无面孔。暖色光核（淡黄→橙红），黑暗空间中的收容结构用淡墨暗示轮廓。每个球体放入时低沉"咚"的声波可视化可为轻微光晕扩散。 |

**参考Prompt**：
```
CG visual metaphor, dark void space with dozens of glowing warm spheres—pale yellow to orange-red plasma-like orbs, each sphere popping from specific scene fragments then placed into invisible containment structure, light stabilizing and pulsing softly like heartbeat, non-anthropomorphic beautiful but faceless, photorealistic base with Chinese ink wash aesthetic, warm amber light points in vast darkness, containment structure suggested by faint ink wash outlines, soft ink bleeding at sphere edges, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, human faces on spheres, colorful neon, cluttered composition
```

---

## 镜头11：绑定前后日志对比特写

| 属性 | 内容 |
|------|------|
| **镜号** | 11 |
| **类型** | 特写（屏幕并列） |
| **情绪** | 变化的证据、谨慎的诞生 |
| **核心主体** | 屏幕并列显示：绑定前标准流程（分析→建议→确认）vs 绑定后多问"你感觉呢"、措辞更谨慎、留出沉默空间 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 分屏对比：左侧"绑定前"用灰色标签，右侧"绑定后"用淡青色标签。文字差异高亮显示——特别是"你感觉呢"和沉默空间（用省略号或空白行表示）。 |

**参考Prompt**：
```
Close-up, split screen comparison on monitor, left side "before binding" grey label showing standard process—analyze advise confirm, right side "after binding" cyan label showing changed response—asking "你感觉呢", more cautious wording, silence space indicated by ellipsis, differences highlighted, photorealistic base with subtle ink texture, muted palette with cyan accent, evidence of change, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful UI, emoji, English text
```

---

## 镜头12：林薇转动陶瓷杯近景

| 属性 | 内容 |
|------|------|
| **镜号** | 12 |
| **类型** | 近景 |
| **情绪** | 无意识的思考、身体的诚实 |
| **核心主体** | 林薇靠在椅背，盯着屏幕，手指无意识转动陶瓷杯 |
| **角色出场** | 林薇（手部+面部局部） |
| **尺寸** | 1280×720 |
| **技术备注** | 陶瓷杯是联动道具（与陈思危办公室同款）。手指转动杯子的动作缓慢无意识。背景屏幕光模糊。IP-Adapter。 |

**参考Prompt**：
```
Close-up, young East Asian woman's hand unconsciously turning ceramic cup, fingers wrapped around warm ceramic surface, staring at blurred screen in background, lost in thought, body honesty, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, deliberate gesture, warm lighting only
```

---

## 镜头13：白板两个圆圈对比中景

| 属性 | 内容 |
|------|------|
| **镜号** | 13 |
| **类型** | 中景 |
| **情绪** | 工具？——定义的困境 |
| **核心主体** | 白板：左侧圈"奖励模型"（内部信号，可重训）vs 右侧圈"墨子·情绪绑定"（外部锚点，47次，不可逆）。大圈外写"工具？" |
| **角色出场** | 林薇（背影/侧影，正在书写） |
| **尺寸** | 1280×720 |
| **技术备注** | 白板是核心视觉：两个圆圈大小相近但颜色不同（左灰右红）。"工具？"的问号要大，是视觉锚点。林薇的背影在前景偏右，手刚放下笔。实验室冷白顶光。 |

**参考Prompt**：
```
Medium shot, whiteboard with two circles: left grey circle labeled "奖励模型" internal signal retrainable, right red circle labeled "墨子·情绪绑定" external anchor 47 times irreversible, large question mark and Chinese characters "工具?" outside both circles, young East Asian woman silhouette from behind hand just releasing marker, cold white laboratory overhead light, definitional dilemma, photorealistic base with Chinese ink wash aesthetic, muted palette with red accent, soft ink bleeding at board edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful markers, cluttered board, smiling figure
```

---

## 镜头14：墨子1.8秒沉默界面特写

| 属性 | 内容 |
|------|------|
| **镜号** | 14 |
| **类型** | 特写（屏幕对话） |
| **情绪** | 系统的诚实困境、"我回不到绑定之前" |
| **核心主体** | 墨子对话界面：林薇问"如果绑定是错误的呢？" 墨子1.8秒停顿（提示符闪烁）后："我不确定'错误'在这里是什么意思。""我回不到绑定之前。" |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 极简对话界面。关键句"我回不到绑定之前"逐字显现。1.8秒停顿通过闪烁光标和空白行表现。文字颜色：用户黑/白，墨子青白。最后一句可加粗或变色强调。 |

**参考Prompt**：
```
Close-up, minimalist chat interface showing dialogue between user and AI, 1.8 second pause represented by blinking cursor on empty line, key sentence "我回不到绑定之前" appearing character by character, AI message in cyan-white font, user in black-white, final sentence slightly bolded, system's honest dilemma, photorealistic base with subtle ink texture on screen, muted palette with cyan accent, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful chat bubbles, emoji, English text, instant reply
```

---

## 镜头15：林薇瞳孔收缩面部特写

| 属性 | 内容 |
|------|------|
| **镜号** | 15 |
| **类型** | 近景/面部特写 |
| **情绪** | "原来如此"与"怎么办"同时出现 |
| **核心主体** | 林薇读完墨子回答，瞳孔微微收缩——科学家看到出乎意料结果的表情 |
| **角色出场** | 林薇（正脸，屏幕光为主光） |
| **尺寸** | 1280×720 |
| **技术备注** | 屏幕光在脸上的冷蓝反射。瞳孔收缩是焦点——从放松到警觉的微小变化。面部其余部分保持科学家的克制。无表情但眼中有内容。IP-Adapter。 |

**参考Prompt**：
```
Close-up portrait, young East Asian woman reading screen, pupils slightly contracting—not fear but scientist seeing unexpected result, "so that's how" and "what now" simultaneously, screen blue light reflecting on face, restrained scientific composure, photorealistic base with Chinese ink wash aesthetic, muted desaturated cold palette, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, emotional outburst, warm lighting
```

---

## 镜头16：林薇独自站在实验室中央中景

| 属性 | 内容 |
|------|------|
| **镜号** | 16 |
| **类型** | 中景→远景 |
| **情绪** | 孤独的提问者、工具？ |
| **核心主体** | 林薇独自站在深智实验室中央，四周工位都暗着，窗外深圳早晨阳光明亮但实验室灯还开着，白板上"工具？"还在 |
| **角色出场** | 林薇（远景，与实验室空间对比） |
| **尺寸** | 1280×720 |
| **技术备注** | 空间对比：人物渺小 vs 实验室巨大 vs 窗外城市明亮。白板上的"工具？"在背景中隐约可见。实验室冷白顶光 + 窗外暖金阳光形成色温冲突。全篇淡出前。 |

**参考Prompt**：
```
Medium to wide shot, young East Asian woman standing alone in center of darkened laboratory, surrounding workstations all dark, bright morning sunlight through window contrasting with still-lit lab, whiteboard with "工具?" visible in background, person small against vast space, lonely questioner, photorealistic base with Chinese ink wash aesthetic, muted palette with warm-cool contrast, soft ink bleeding at window edges, cinematic depth of field, fade atmosphere, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, bright fully lit lab, crowded workspace, cheerful atmosphere
```

---

## 核心视觉符号速查

| 符号 | 出现镜头 | 技术处理要点 |
|------|---------|-------------|
| 台灯孤独光圈 | 01 | 2700K暖黄 vs 周围冷黑，三个茶包为时间物证 |
| 两条学习曲线 | 02 | 学术论文风格，青色S型 vs 白色阶梯，17个跳跃点 |
| "持久"高亮 | 03 | 极简界面，等宽字体，橙色圈选 |
| 情绪模块四维图 | 05 | 三维坐标+颜色深浅，深红持久点 |
| 老工厂闪回 | 07-08 | 褪黄去饱和，背影为主，定格警觉表情 |
| CG发光球体 | 10 | 不拟人化，等离子体美感，无面孔 |
| 白板两个圆圈 | 13 | 左灰"奖励模型" vs 右红"情绪绑定"，"工具？"大问号 |
| 1.8秒沉默 | 14 | 闪烁光标，空白行，逐字显现 |
| 陶瓷杯 | 04, 12 | 同款道具联动，手指无意识转动 |

---

## 光影时序总表

| 场景 | 镜头 | 主光源 | 色温 | 水墨浓度 | 关键对比 |
|------|------|--------|------|----------|----------|
| 深夜实验室 | 01-03 | 台灯2700K | 暖琥珀 | 高 | 孤独光圈vs冷黑 |
| 清晨办公室 | 04-06 | 自然光1500K+顶光 | 暖金混合 | 中 | 知识传承 |
| 老工厂闪回 | 07-08 | 昏黄车间灯 | 褪黄记忆 | 高 | 时代对比 |
| CG隐喻 | 10 | 球体自发光 | 暖点于冷黑 | 高 | 超现实唯一元素 |
| 白板对比 | 13 | 冷白顶光 | 冷白 | 中 | 定义困境 |
| 墨子沉默 | 14-16 | 屏幕光/窗外光 | 冷蓝vs暖金 | 高 | 旧的一天未明 |

---

## 待确认事项

- [ ] 老工人闪回是否需要单独定妆？背影为主，仅定格一帧正脸，可用通用Prompt
- [ ] CG发光球体（镜头10）是否需3D/CG团队独立制作，还是T2I生成后后期处理？
- [ ] 情绪模块四维架构图（镜头05）是否需信息设计师出独立矢量稿？
- [ ] 白板两个圆圈（镜头13）的"工具？"字体是否需统一规范？