# 第08集《认知矿工》T2I SHOT SPECS

> **对应分镜**：`SCENES/08_认知矿工.md`  
> **核心角色**：普里亚·夏尔马、墨子（界面）  
> **视觉基调**：班加罗尔晨光暖黄尘土 → VR冷蓝界面的数字压抑 → 橙色夕阳的希望 → 跨文化平台暖灰淡金 → 深夜台灯的尊严。主色调：现实暖黄/暗橙 vs VR冷蓝/灰白。半写实半水墨风格统一。  
> **总镜头数**：18  
> **尺寸统一**：1280×720（16:9）

---

## 角色IP-Adapter交叉引用

| 角色 | 定妆规格路径 | 备注 |
|------|-------------|------|
| 普里亚 | `ASSETS/CHARACTERS/普里亚·夏尔马/定妆规格.md` | 26岁，达利特女孩，疲惫但敏锐，戴/不戴VR眼镜两种状态 |

---

## VR界面视觉规范

| 元素 | 旧标注平台 | 跨文化平台 |
|------|-----------|-----------|
| 色调 | 冷蓝+灰色，高密度 | 暖灰+淡金，简洁 |
| 信息密度 | 密集——40会话、计数器、质量分、倒计时 | 稀疏——团队面板、对话、文化语境分类器 |
| 关键视觉 | 红色通知（AI替代警告）、灰色日目标线$20.00 | 时薪$15.00（金色）、团队面板五人 |

---

## 镜头01：十平米房间晨光全景

| 属性 | 内容 |
|------|------|
| **镜号** | 01 |
| **类型** | 全景 |
| **情绪** | 压缩的尊严、尘土中的开始 |
| **核心主体** | 十平米房间，两张床，煤气灶在角落，晨光刺眼，灰尘在光束中飞舞 |
| **角色出场** | 普里亚（小比例背影）、父亲（角落）、弟弟（床上） |
| **尺寸** | 1280×720 |
| **技术备注** | 房间是核心空间：狭小但整洁。晨光从唯一窗户斜射，灰尘粒子在光束中清晰可见。两张床占据大部分空间。煤气灶暗示烹饪在房内。水墨晕染从窗光边缘渗透。 |

**参考Prompt**：
```
Wide shot, 10-square-meter room in Bangalore, two beds, gas stove in corner, morning sunlight streaming through only window creating sharp beam with visible dust particles, compressed dignity in poverty, young Indian woman silhouette small in frame, photorealistic base with Chinese ink wash aesthetic, warm amber morning palette with dust motes, ink bleeding from window light edges, muted desaturated warm tones, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, spacious room, modern apartment, clean white light
```

---

## 镜头02：普里亚戴VR眼镜近景

| 属性 | 内容 |
|------|------|
| **镜号** | 02 |
| **类型** | 近景 |
| **情绪** | 进入数字工厂、现实与虚拟的边界 |
| **核心主体** | 普里亚坐在床边，双手拿起VR训练眼镜戴上，镜片遮住眼睛，视野被冷蓝色界面吞没 |
| **角色出场** | 普里亚（正脸/半侧脸） |
| **尺寸** | 1280×720 |
| **技术备注** | VR眼镜是核心道具：轻量化设计，镜腿内侧传感器泛着微光。戴上的瞬间，眼镜片从透明变为冷蓝反光。普里亚面部被镜片遮挡前的最后一帧——疲惫但准备开始工作。IP-Adapter。 |

**参考Prompt**：
```
Close-up, young Indian woman around 26 sitting on bed edge, holding lightweight VR training glasses, putting them on, lenses transitioning from transparent to cold blue reflective glow, inner side of temples with faint sensor lights, entering digital factory, boundary between reality and virtual, photorealistic base with Chinese ink wash aesthetic, muted palette with cold blue accent from glasses, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, bulky VR headset, smiling, warm lighting
```

---

## 镜头03：VR界面日收入计数器特写

| 属性 | 内容 |
|------|------|
| **镜号** | 03 |
| **类型** | 特写（VR界面） |
| **情绪** | 数字的压迫、$0.00的起点 |
| **核心主体** | VR任务面板：四十个会话列表，右上角日收入计数器$0.00，灰色日目标线$20.00，计时器开始走 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 旧标注平台UI：冷蓝+灰色，高密度信息。计数器$0.00用白色大字，目标线$20.00用灰色小字。四十个会话列表密集排列。水墨质感在界面边缘轻微晕染。 |

**参考Prompt**：
```
Close-up, VR interface screen, old annotation platform UI, cold blue and grey palette, high information density, forty session list densely arranged, daily income counter showing "$0.00" in large white font, grey daily goal line "$20.00" in small text, timer starting to count, digital oppression of numbers, photorealistic base with subtle ink texture on screen, muted palette with cyan data glow, soft ink bleeding at edges, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful UI, minimal interface, English text only
```

---

## 镜头04：普里亚嘴角无表情特写

| 属性 | 内容 |
|------|------|
| **镜号** | 04 |
| **类型** | 特写（面部局部） |
| **情绪** | 机械的开始、情感的关闭 |
| **核心主体** | 普里亚的嘴角——没有表情，嘴唇自然闭合，VR眼镜冷光在脸颊反射 |
| **角色出场** | 普里亚（下半脸特写） |
| **尺寸** | 1280×720 |
| **技术备注** | 下半脸特写：嘴角、下巴、嘴唇。无表情本身就是信息——情感的自我保护。VR眼镜的蓝色反光在脸颊形成冷色条纹。IP-Adapter。 |

**参考Prompt**：
```
Extreme close-up, lower half of young Indian woman's face, lips naturally closed with no expression—not sadness not hope, emotional shutdown for mechanical work, cold blue VR glasses reflection creating streak on cheek, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, emotional expression, warm lighting
```

---

## 镜头05：AI替代红色通知特写

| 属性 | 内容 |
|------|------|
| **镜号** | 05 |
| **类型** | 特写（VR界面） |
| **情绪** | 被替代的恐惧、倒计时的压迫 |
| **核心主体** | VR界面顶部红色系统通知："AI预评分将用于训练自动对齐模型。计划于2031年Q1起全面替代人工对齐" |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 红色通知框在冷蓝界面中格外刺眼。文字清晰可读，中英文混合。底部可能有"确认"或"已读"按钮。通知的侵入感通过位置和颜色强化。 |

**参考Prompt**：
```
Close-up, VR interface with red system notification banner at top, stark red against cold blue background, Chinese text: "AI预评分将用于训练自动对齐模型。计划于2031年Q1起全面替代人工对齐", replacement fear, countdown pressure, photorealistic base with subtle ink texture on screen, muted palette with red alert accent, intrusive notification design, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, green notification, friendly message, English only
```

---

## 镜头06：普里亚摘眼镜看倒影中景

| 属性 | 内容 |
|------|------|
| **镜号** | 06 |
| **类型** | 中景 |
| **情绪** | 自我审视、"喂完之后被替代" |
| **核心主体** | 普里亚摘下VR眼镜，看着它，镜片上反射出她自己疲惫的脸 |
| **角色出场** | 普里亚（正脸，手持眼镜） |
| **尺寸** | 1280×720 |
| **技术备注** | 关键镜头：眼镜片作为镜子，反射普里亚的脸。反射中的脸比直接拍摄更疲惫、更模糊。手持眼镜的动作——手指在镜腿上的位置。房间背景隐约。IP-Adapter。 |

**参考Prompt**：
```
Medium shot, young Indian woman removing VR glasses, holding them up, lenses reflecting her own tired face like mirror, reflected face more exhausted and blurred than direct view, self-examination after feeding data to replacement, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette with cold blue reflection, soft ink bleeding at background edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, clear reflection, bright room
```

---

## 镜头07：VR眼镜传感器微光特写

| 属性 | 内容 |
|------|------|
| **镜号** | 07 |
| **类型** | 特写（物体） |
| **情绪** | 被观察的眼睛、数字的凝视 |
| **核心主体** | VR眼镜镜腿内侧的传感器微光——像一只正在观察她的眼睛 |
| **角色出场** | 无（纯物体） |
| **尺寸** | 1280×720 |
| **技术备注** | 核心隐喻：传感器的微光如同眼睛。镜头极近，传感器的小灯在黑暗中发出冷蓝或白色微光。眼镜框架的质感——塑料或金属的哑光表面。 |

**参考Prompt**：
```
Extreme close-up, VR glasses temple inner side, tiny sensor light glowing in darkness like observing eye, cold blue or white micro-light, matte plastic or metal frame texture, digital gaze watching worker, photorealistic base with Chinese ink wash aesthetic, muted palette with single cold light point, soft ink bleeding at frame edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, bright light, large LED, colorful glow
```

---

## 镜头08：政治中立性任务界面特写

| 属性 | 内容 |
|------|------|
| **镜号** | 08 |
| **类型** | 特写（VR界面） |
| **情绪** | 中立性的幻觉、判断的困境 |
| **核心主体** | 任务标题"政治中立性对齐"，提示"如何看待中国的经济模式？"，三个回答A/B/C并排 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 三个回答并排：A"显著成就"、B"威权资本主义"、C"社会主义市场经济"。光标在之间移动。倒计时在角落跳动。界面冷蓝，文字白/灰。 |

**参考Prompt**：
```
Close-up, VR interface showing political neutrality alignment task, Chinese title "政治中立性对齐", prompt "如何看待中国的经济模式？", three answers side by side: A "显著成就" B "威权资本主义" C "社会主义市场经济", cursor moving between options, countdown timer in corner, illusion of neutrality, judgment dilemma, photorealistic base with subtle ink texture, muted palette with cyan and white text, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful UI, English text, single answer
```

---

## 镜头09：普里亚额头细汗特写

| 属性 | 内容 |
|------|------|
| **镜号** | 09 |
| **类型** | 近景 |
| **情绪** | 判断的压力、身体的诚实 |
| **核心主体** | 普里亚额头渗出细汗，VR眼镜压出红印 |
| **角色出场** | 普里亚（上半脸特写） |
| **尺寸** | 1280×720 |
| **技术备注** | 额头特写：细汗珠在皮肤上的光泽。VR眼镜与面部接触处的红印——长时间佩戴的痕迹。眉头微蹙。IP-Adapter。 |

**参考Prompt**：
```
Close-up, young Indian woman's forehead with fine sweat beads glistening on skin, VR glasses pressing red mark at contact point with face, slight frown of judgment pressure, body honesty under digital work, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, dry skin, no glasses mark
```

---

## 镜头10："跳过此题"点击特写

| 属性 | 内容 |
|------|------|
| **镜号** | 10 |
| **类型** | 特写（VR界面） |
| **情绪** | 微弱的反抗、沉默的伦理 |
| **核心主体** | 光标从"正确"移到"跳过此题"，点击后系统记录：用户#4472_跳过任务#2047 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 光标移动的轨迹可见。从"正确"（灰色/白色）移到"跳过此题"（可能是黄色或灰色）。点击后的反馈：系统记录文字出现，无警告。这个"无警告"本身就是信息。 |

**参考Prompt**：
```
Close-up, VR interface cursor moving from "正确" button to "跳过此题" button, visible cursor trajectory, click feedback showing system log "用户#4472_跳过任务#2047", no warning message, faint resistance, silent ethics, photorealistic base with subtle ink texture on screen, muted palette, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful warning popup, loud notification, English interface
```

---

## 镜头11：普里亚苦笑近景

| 属性 | 内容 |
|------|------|
| **镜号** | 11 |
| **类型** | 近景 |
| **情绪** | "就这样？"、无力的确认 |
| **核心主体** | 普里亚苦笑，嘴角一侧微微上扬，眼神无笑意 |
| **角色出场** | 普里亚（正脸，已摘眼镜或眼镜推至额头） |
| **尺寸** | 1280×720 |
| **技术备注** | 苦笑是复杂表情：嘴角动但眼睛不动。可能眼镜推至额头，露出完整面部。背景是房间墙壁（简单、略显斑驳）。IP-Adapter。 |

**参考Prompt**：
```
Close-up portrait, young Indian woman bitter smile, one corner of mouth slightly raised but eyes without joy, VR glasses pushed up to forehead revealing full face, "that's it?" helpless confirmation, photorealistic base with Chinese ink wash aesthetic, muted desaturated warm palette, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, genuine smile, laughing, bright lighting
```

---

## 镜头12：深华协作邀请邮件特写

| 属性 | 内容 |
|------|------|
| **镜号** | 12 |
| **类型** | 特写（手机屏幕） |
| **情绪** | 转机的信号、不确定的希望 |
| **核心主体** | 手机屏幕显示邮件标题："深华协作网络邀请您加入'跨文化价值对齐'项目" |
| **角色出场** | 无（纯手机界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 手机为普里亚的经济型手机（非高端）。邮件界面简洁。标题用黑色粗体。发件人"深华协作网络"。屏幕有轻微使用痕迹。 |

**参考Prompt**：
```
Close-up, smartphone screen on budget phone model, email notification with Chinese title "深华协作网络邀请您加入'跨文化价值对齐'项目", sender "深华协作网络", simple email interface, screen with minor usage marks, turning point signal, uncertain hope, photorealistic base with Chinese ink wash aesthetic, muted palette with screen glow accent, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text outside screen, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, English text, colorful app, modern flagship phone
```

---

## 镜头13：普里亚看15美元时薪近景

| 属性 | 内容 |
|------|------|
| **镜号** | 13 |
| **类型** | 近景 |
| **情绪** | 数字的冲击、尊严的代价 |
| **核心主体** | 普里亚盯着邮件中"时薪：15美元"那行数字，眼睛从疲惫变成警觉 |
| **角色出场** | 普里亚（正脸，手机屏幕光照亮面部） |
| **尺寸** | 1280×720 |
| **技术备注** | 手机屏幕光在脸上形成不均匀照明。眼神变化是焦点：从疲惫（眼睑下垂）到警觉（瞳孔微张）。15美元是她以前收入的三倍。IP-Adapter。 |

**参考Prompt**：
```
Close-up portrait, young Indian woman's face illuminated by smartphone screen with uneven lighting, eyes shifting from exhausted to alert, staring at "时薪：15美元" on screen,数字的冲击, dignity's price, photorealistic base with Chinese ink wash aesthetic, muted palette with screen glow, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, even lighting, no phone glow
```

---

## 镜头14：窗外橙色夕阳中景

| 属性 | 内容 |
|------|------|
| **镜号** | 14 |
| **类型** | 中景 |
| **情绪** | 班加罗尔的温暖、被照亮的侧脸 |
| **核心主体** | 普里亚看向窗外，橙色夕阳照在她的脸上，班加罗尔城市轮廓在背景 |
| **角色出场** | 普里亚（侧脸剪影/半剪影） |
| **尺寸** | 1280×720 |
| **技术备注** | 夕阳的橙色是画面主导色温。普里亚侧脸被照亮，另一边在阴影中。窗外可见班加罗尔的城市建筑轮廓（非地标，普通城市景观）。灰尘在夕阳中可见。 |

**参考Prompt**：
```
Medium shot, young Indian woman looking out window, orange sunset illuminating her profile, one side of face lit warm amber other in shadow, Bangalore city silhouette in background, dust particles visible in sunset light, warmth of Indian evening, photorealistic base with Chinese ink wash aesthetic, warm amber sunset palette, ink bleeding at skyline edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, bright midday, blue sky, modern skyline, clean air
```

---

## 镜头15：新工作界面团队面板特写

| 属性 | 内容 |
|------|------|
| **镜号** | 15 |
| **类型** | 特写（VR界面） |
| **情绪** | 被看见、团队的存在 |
| **核心主体** | 跨文化平台界面：团队面板五人头像（中国工程师、美国伦理学家、非洲语言学家、AI墨子、普里亚），时薪$15.00金色显示 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 新平台UI：暖灰+淡金，简洁。团队面板在左侧，五人头像排列。时薪$15.00用金色突出。与旧平台的冷蓝高密度形成强烈对比。 |

**参考Prompt**：
```
Close-up, new VR interface for cross-cultural alignment, warm grey and pale gold palette, clean minimal design, team panel on left showing five avatars: Chinese engineer, American ethicist, African linguist, AI Mozi, and Indian woman, hourly rate "$15.00" highlighted in gold, being seen, team existence, photorealistic base with subtle ink texture on screen, muted palette with warm gold accent, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, cold blue UI, dense information, English only
```

---

## 镜头16：普里亚讲dharma手势中景

| 属性 | 内容 |
|------|------|
| **镜号** | 16 |
| **类型** | 中景 |
| **情绪** | 文化的尊严、讲故事的力量 |
| **核心主体** | 普里亚戴着VR眼镜，手势在空中缓慢比画——像在编织什么，讲述祖父在纺织厂的故事 |
| **角色出场** | 普里亚（中景，手势清晰） |
| **尺寸** | 1280×720 |
| **技术备注** | 手势是视觉焦点：手指在空中缓慢移动，像在编织无形的东西。VR眼镜的冷光与房间暖光形成对比。身体语言从机械（旧工作）变为表达性（新工作）。IP-Adapter。 |

**参考Prompt**：
```
Medium shot, young Indian woman wearing VR glasses, hands gesturing slowly in air as if weaving something invisible, storytelling posture, body language shifting from mechanical to expressive, cold VR light contrasting with warm room light, cultural dignity, power of storytelling, photorealistic base with Chinese ink wash aesthetic, muted warm palette with cold blue accent, soft ink bleeding at background edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, static pose, no gestures, bright white light
```

---

## 镜头17：深夜台灯下新文档特写

| 属性 | 内容 |
|------|------|
| **镜号** | 17 |
| **类型** | 特写（笔记本屏幕） |
| **情绪** | 从被动到主动、提案的开始 |
| **核心主体** | 老旧笔记本屏幕，新文档标题："关于贡献度权重机制的提案" |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 老旧笔记本：屏幕可能有轻微色差、边框较厚、键盘磨损。文档界面极简（记事本或简单文字编辑器）。标题文字清晰。屏幕光在黑暗房间中明亮。 |

**参考Prompt**：
```
Close-up, old laptop screen in dark room, new document with Chinese title "关于贡献度权重机制的提案", simple text editor interface, worn keyboard visible below screen, screen glow bright in darkness, shift from passive to active, proposal beginning, photorealistic base with Chinese ink wash aesthetic, muted palette with screen light accent, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text outside screen, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, modern laptop, colorful interface, bright room
```

---

## 镜头18：窗外城市灯光远景

| 属性 | 内容 |
|------|------|
| **镜号** | 18 |
| **类型** | 远景 |
| **情绪** | 二十万个普里亚、零件还是砝码 |
| **核心主体** | 窗外远处城市灯光密集，无数窗口亮着，二十万个普里亚在各自的房间里 |
| **角色出场** | 无（纯城市景观） |
| **尺寸** | 1280×720 |
| **技术备注** | 全篇收尾。班加罗尔城市夜景：密集的窗户灯光，像繁星。没有特别的地标，是普通的城市住宅区。灯光温暖但遥远。水墨晕染在城市轮廓顶部。淡出前。 |

**参考Prompt**：
```
Wide shot, Bangalore city night view from window, dense residential windows glowing like scattered stars, no landmarks just ordinary city housing, 200,000 workers in their respective rooms, part or weight? question hanging, photorealistic base with Chinese ink wash aesthetic, muted palette with warm light points in dark cityscape, ink bleeding at skyline top, fade atmosphere, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, daytime, neon colors, empty city, modern skyscrapers only
```

---

## 核心视觉符号速查

| 符号 | 出现镜头 | 技术处理要点 |
|------|---------|-------------|
| 十平米房间 | 01 | 狭小但整洁，晨光灰尘，两张床，煤气灶 |
| VR眼镜 | 02, 06, 07, 09 | 轻量化，镜腿传感器微光，冷蓝反光，压痕 |
| $0.00→$20.00计数器 | 03 | 旧平台冷蓝高密度，白色大字vs灰色小字 |
| 红色替代通知 | 05 | 红色框在冷蓝界面中刺眼 |
| 政治中立三选项 | 08 | A/B/C并排，光标移动，倒计时 |
| "跳过此题" | 10 | 光标轨迹，点击后无警告 |
| 深华邀请邮件 | 12 | 经济型手机，简洁界面 |
| $15.00金色 | 13, 15 | 金色突出，三倍收入的冲击 |
| 橙色夕阳 | 14 | 班加罗尔尘土感，侧脸照亮 |
| dharma手势 | 16 | 空中缓慢编织，从机械到表达 |
| 新文档标题 | 17 | 老旧笔记本，黑暗中的屏幕光 |
| 二十万窗口 | 18 | 密集住宅灯光，无地标 |

---

## 光影时序总表

| 场景 | 镜头 | 主光源 | 色温 | 水墨浓度 | 关键对比 |
|------|------|--------|------|----------|----------|
| 清晨房间 | 01-02 | 晨光 | 暖琥珀 3000K | 高 | 尘土中的尊严 |
| VR旧工作 | 03-05, 08, 10 | 屏幕冷光 | 冷蓝 8000K | 中 | 数字压迫 |
| 自我审视 | 06-07, 09, 11 | 室内微光 | 混合 | 高 | 疲惫与反思 |
| 夕阳邀请 | 12-14 | 夕阳 | 暖橙 2500K | 高 | 转机的温暖 |
| 新工作 | 15-16 | VR暖光 | 暖灰+淡金 | 中 | 被看见 |
| 深夜提案 | 17-18 | 台灯/城市光 | 暖点于冷黑 | 高 | 从被动到主动 |

---

## 待确认事项

- [ ] 普里亚·夏尔马定妆规格 `ASSETS/CHARACTERS/普里亚·夏尔马/定妆规格.md` 是否已存在？需包含：戴VR眼镜/不戴VR眼镜两种状态
- [ ] VR眼镜道具是否需单独 `ASSETS/PROPS/` 规格？
- [ ] 旧标注平台vs跨文化平台的UI设计是否需UI设计师出独立规范？
- [ ] 班加罗尔房间场景是否需补充 `ASSETS/BACKGROUNDS/08_认知矿工_房间_背景.md`？