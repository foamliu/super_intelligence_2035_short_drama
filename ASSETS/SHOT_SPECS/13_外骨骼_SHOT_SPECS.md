# 第13集《外骨骼》T2I SHOT SPECS

> **对应原著**：`BOOK/13-exoskeleton.md`  
> **核心角色**：莎拉·赵（自动驾驶工程师+脱口秀演员）、师兄（公司老板/实验室传奇）、林薇（声音出场/微信消息）  
> **视觉基调**：四个空间交替——开放麦酒吧后台/舞台（暖黄+暗酒红）、公司工位（冷白荧光+屏幕蓝）、上海地铁早高峰（惨白荧光+暖灰）、2017实验室闪回（怀旧暖黄+CRT蓝）。核心视觉符号是"虚拟观众"——模型渲染出来的不存在的脸。半写实半水墨风格统一。  
> **总镜头数**：约55-65  
> **尺寸统一**：1920×1080（16:9），部分特写/关键图用 1920×1920 或 1920×2560

---

## 角色IP-Adapter交叉引用

| 角色 | 定妆规格路径 | 备注 |
|------|-------------|------|
| 莎拉·赵 | `ASSETS/CHARACTERS/08_莎拉·赵/定妆规格.md` | 28岁，深色简约T恤+牛仔裤，台上台下同一套衣服——这是细节 |
| 师兄 | 待创建 | 31岁，瘦高、黑框眼镜、深色卫衣——技术创业者风格，实验室传奇有黑眼圈 |
| 林薇 | `ASSETS/CHARACTERS/05_林薇/定妆规格.md`（如有） | 本集仅电话声音和微信消息，不直接出场 |
| 小周 | 待创建（可选） | 场务，托儿，大学生年龄，棒球帽 |

---

## 四空间视觉规范

| 元素 | 开放麦酒吧 | 公司工位 | 上海地铁 | 2017实验室（闪回） |
|------|-----------|---------|---------|-------------------|
| 色调 | 暖黄+琥珀+暗酒红 | 冷白荧光+屏幕蓝+灰蓝工程色 | 惨白荧光+暖灰+隧道灯扫过 | 怀旧暖黄+CRT蓝+台灯暖 |
| 氛围 | 亲密、暴露、说完后的安静 | 专注、屏幕光映脸、双显示器的世界 | 拥挤但日常、观察而非参与 | 记忆的质感——灰尘在光中浮动 |
| 光 | 舞台灯只照亮莎拉，其余更暗 | 双显示器冷光+午后阳光混合 | 均匀惨白+窗外隧道灯光扫过 | 只有台灯照亮工作区，其余暗 |
| 水墨 | 从舞台边缘和暗处渗入 | 从显示器边缘洇出 | 仅在车窗反射中浮现 | 从画面边缘渗入——记忆被时间漂过 |

---

## 镜头01：开放麦后台·等待上场

| 属性 | 内容 |
|------|------|
| **镜号** | 01.1-01.8 |
| **类型** | 中景→特写→近景→特写→近景→中景→特写→黑屏过渡 |
| **情绪** | 后台等待的日常→师兄消息打破→"明天九点"→把手机翻过去扣在桌上 |
| **核心主体** | 地下酒吧后台狭窄过道，莎拉坐在折叠椅上低头看手机。前面大学生在台上讲租房面试猫——台下笑声。师兄的消息："明天那个模型的上线评审，你准备一下。"她回"在准备"。师兄追问"你在开放麦后台吧？"——她没回。手机扣桌上。 |
| **角色出场** | 莎拉·赵（后台等待状态）、大学生（远景/声音）、师兄（手机消息） |
| **尺寸** | 1920×1080 |
| **技术备注** | 手机屏幕是核心道具——师兄消息的绿色气泡。荧光灯管——刺眼的开放麦后台光。扣手机的动作是决定性瞬间——不是愤怒，是"他说对了但我今晚不想被他说对"。墙上贴满脱口秀海报——纸+胶带质感。 |

**参考Prompt**：
```
Medium shot, backstage of a small underground open-mic comedy club in Shanghai, narrow corridor with comedy posters taped unevenly on walls, harsh fluorescent lighting overhead, Chinese woman 28 sitting on folding chair holding smartphone with screen glowing - WeChat message visible, expression calm but holding something back, medium-short dark hair natural look, dark casual top, cables and mic stands in background clutter, photorealistic base with Chinese ink wash aesthetic, warm amber shadows and cool fluorescent key light, ink bleeding from corridor edges, cinematic depth of field, 16:9, 8k
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, smiling, happy, makeup, jewelry, modern luxury bar, cocktail lounge, glamorous
```

---

## 镜头01B：大学实验室闪回·2026年夏天

| 属性 | 内容 |
|------|------|
| **镜号** | 01B.1-01B.5 |
| **类型** | 远景→中景→近景→特写→近景 |
| **情绪** | 怀旧→"端到端自动驾驶的可能性"→全行业在追他的方向 |
| **核心主体** | 旁白闪回——莎拉2026年硕士毕业，师兄面试她："你觉得自动驾驶最难的是什么？"她说"让车开得像人"。师兄说"不对。最难的是让别人相信你的车开得像人。" |
| **角色出场** | 莎拉·赵（年轻版，24岁）、师兄（年轻版，27岁） |
| **尺寸** | 1920×1080 |
| **技术备注** | 面试场景——不是正式会议室，是实验室角落或小办公室。师兄的这句话是整集的种子。2026年视觉参考——显示器不是现在的超薄LED，边框更宽。 |

**参考Prompt**：
```
Medium shot, 2026-era Chinese university lab corner used as informal interview room, young Chinese woman 24 in simple clothes sitting across from young Chinese man 27 with black-framed glasses in hoodie, old LCD monitors with warm blue glow in background, whiteboard with handwritten formulas visible, afternoon light through window, the man is speaking seriously - not judging but assessing, woman listening intently, slightly dated tech aesthetic (2026 not futuristic), photorealistic base with Chinese ink wash aesthetic, warm afternoon light and CRT blue, cinematic, 16:9, 8k
```

**负面Prompt**：
```
cartoon, anime, 3D render, futuristic, modern Apple products, MacBook, luxury office, suit, tie, smiling, laughing, bright, clean, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头02：公司工位·向林薇解释"外骨骼"

| 属性 | 内容 |
|------|------|
| **镜号** | 02.1-02.12 |
| **类型** | 中景→特写→近景→特写→中景→特写→近景→中景→特写→近景→特写→中景 |
| **情绪** | 解释一件对她很重要但不确定别人能否理解的事→"它在想象观众"→"它不是大脑不是心脏，是骨架" |
| **核心主体** | 莎拉坐在公司工位，双显示器亮着——左侧播放自己讲段子的视频，右侧展示世界模型界面：渲染出的虚拟观众脸+笑声强度热力图。她拿着手机跟林薇打电话（有线耳机——不是AirPods）。一边说一边用手指向屏幕上的热力图区域。"我给它起了个名字：外骨骼。" |
| **角色出场** | 莎拉·赵、林薇（电话声音） |
| **尺寸** | 1920×1080 |
| **技术备注** | 双显示器内容是核心——左侧视频窗口+右侧虚拟观众热力图。这是"外骨骼"概念的视觉锚点。莎拉的手势——从自己胸口往屏幕方向划——"我做的这个模型，是我的外挂，不是要代替我"。午后深圳光线从窗口混合屏幕光。水墨晕染从显示器边缘慢慢洇出。 |

**参考Prompt**：
```
Medium shot, Chinese woman 28 at office desk in tech company, dual monitors glowing - left screen playing video of herself on stage holding mic, right screen showing AI world model interface with rendered virtual audience faces and laugh intensity heat map (green/yellow/red zones), she holds smartphone to ear with wired earphones talking earnestly, other hand gesturing toward screen, afternoon Shenzhen light through window mixing with cold screen glow, dark casual t-shirt, no heavy makeup, explaining something important, photorealistic base with Chinese ink wash aesthetic, cold office fluorescent and warm screen light, ink bleeding from monitor bezels, cinematic, 16:9, 8k
```

**负面Prompt**：
```
smile, happy, sci-fi, hologram, Iron Man, robot suit, futuristic UI, makeup, jewelry, wireless, AirPods, Bluetooth, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality
```

---

## 镜头03：核心视觉·虚拟观众——不存在的脸在笑

| 属性 | 内容 |
|------|------|
| **镜号** | 03.1-03.7 |
| **类型** | 特写→极近特写→特写→中景→特写→近景→特写 |
| **情绪** | 不安的美——这张脸不存在，但模型"相信"它会在0.82的强度笑 |
| **核心主体** | 一张"渲染出来但不存在"的人脸特写——25-35岁中性观众，在笑。皮肤纹理太过完美，笑容有一两帧的延迟感，眼神深处没有"被逗到"的光。绿色AI标注框："第三排左侧·预测笑声强度0.82"。背景其他渲染脸有的在笑有的没有——全部有类似的"微妙不对"。观众席叠加绿/黄/红热力区域。 |
| **角色出场** | 虚拟观众（AI渲染的人脸——不是真实人物） |
| **尺寸** | 1920×1080 |
| **技术备注** | **全片视觉心脏**。这张脸是"统计上的笑不是体验到的笑"的视觉化。灰蓝渲染色滤镜——不是照片，是渲染。水墨晕染在"皮肤纹理"区域——暗示这脸不是真的。0.82的标注框是绿色AI风格（淡绿矩形+白色机器字体）。 |

**参考Prompt**：
```
Extreme close-up of a human face that is NOT real - an AI world model rendering predicting audience reaction, the face is laughing with mouth open and eyes crinkled, but something subtly wrong: skin texture too uniform, laugh reaches mouth but not eyes, barely perceptible delay between emotion and expression, green AI annotation box overlay reading "Row 3 Left · Predicted Laugh Intensity: 0.82", background has other rendered faces in soft focus, green/yellow/red heat map zones faintly overlaid on audience seats, gray-blue render tint - clearly not a photograph, photorealistic base with Chinese ink wash aesthetic, ink bleeding through skin texture areas - the face is dissolving at edges, unsettling not because ugly but because almost perfect, cinematic, 16:9, 8k
```

**负面Prompt**：
```
real photo, real person, photograph, recognizable person, celebrity, camera photo, selfie, horror, scary, monster, zombie, glitch, deepfake, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality
```

---

## 镜头04：渲染vs真实·两张脸的对比

| 属性 | 内容 |
|------|------|
| **镜号** | 04.1-04.6 |
| **类型** | 特写→近景→特写→中景→特写→近景 |
| **情绪** | 上半：统计上对但肉体上假。下半：有毛孔有牙缝但真正在觉得好笑。上半消融→下半继续。 |
| **核心主体** | 双联构图。上半：渲染虚拟脸在笑，标注"0.82"，绿色AI框，皮肤太完美——微蓝灰渲染色。下半：同机位同角度——真实观众席，小周（场务，大学生年龄，戴棒球帽，举啤酒杯）在笑——真实的、不完美的笑，暖黄真实灯光。水墨晕染仅在上半。 |
| **角色出场** | 虚拟观众脸（上）、小周（下） |
| **尺寸** | 1920×1080（上下各540px） |
| **技术备注** | 这是"模型盲区"的视觉化——模型学到"A位置有笑声"但学不到"为什么笑"（托儿）。上半微蓝灰渲染色，下半暖黄真实灯光。过渡：上半逐渐像素化消融→水墨洇开→下半全屏继续。 |

**参考Prompt**：
```
Split-screen composition, upper half: AI-rendered human face laughing slightly off - skin too perfect, eyes not fully committed to laugh, green AI box "0.82" overlay, blue-gray render tint, lower half: real young Chinese man early 20s wearing baseball cap holding beer in small comedy club audience laughing genuinely - eyes crinkle irregularly, teeth show unevenly, skin has pores and expression lines, warm amber real light, same angle same framing same lighting temperature upper and lower but utterly different, upper half pixelating at edges with ink wash bleeding through dissolving pixels, lower half continues real imperfect alive, photorealistic, cinematic, 16:9, 8k
```

**负面Prompt**：
```
same face, identical, deepfake label, split screen line visible, cartoon, anime, surreal, photoshopped, horror, scary, glitch, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头05：师兄·"合法吗？"

| 属性 | 内容 |
|------|------|
| **镜号** | 05.1-05.8 |
| **类型** | 中景→近景→特写→近景→特写→中景→特写→近景 |
| **情绪** | 知道她在搞什么→问"合法吗"→嘴角微弧度→"你别把我的代码写进段子里"→"第147行，括号错了"→没说话端起咖啡 |
| **核心主体** | 师兄在公司工位区——半侧面，单手端公司logo咖啡杯。眼下黑眼圈——实验室出来的人熬的夜。问"合法吗"时嘴角有一丝"果然如此"的微弧度。听到"第147行括号错了"时看着她——"那是真的"——"真的才好笑"。 |
| **角色出场** | 师兄 |
| **尺寸** | 1920×1080 |
| **技术备注** | 师兄的表情是核心——不是赞许不是反对，是认识她十年的人看到她又搞出东西来了。咖啡杯有公司logo。冷白荧光照在脸上——皮肤不是二十岁出头了，毛孔眼纹。 |

**参考Prompt**：
```
Medium shot, Chinese man 31 in tech company office area, slim tall wearing black-framed glasses and dark hoodie - technical founder style not corporate suit, holding coffee mug with company logo, dark circles under eyes - the legend of the lab also gets tired, half-profile looking at someone off-screen, slight micro-expression at corner of mouth - not quite a smile not disapproval, cold white fluorescent lighting on face showing skin pores and eye lines - not 20 anymore, ink wash aesthetic bleeding from office edges, photorealistic base with Chinese ink wash, cold white and steel blue palette, cinematic, 16:9, 8k
```

**负面Prompt**：
```
smile, laughing, happy, suit, tie, CEO, luxury office, young, handsome, energetic, muscular, romantic, makeup, warm lighting, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头06：2017实验室闪回·咖啡杯冒气

| 属性 | 内容 |
|------|------|
| **镜号** | 06.1-06.5 |
| **类型** | 远景→中景→特写→近景→远景 |
| **情绪** | 怀旧→"有些事不能备份"→记忆的质感——灰尘在光中浮动 |
| **核心主体** | 中国大学计算机实验室（2017年视觉）。灰色地板，旧台式机箱堆叠，CRT/LCD旧显示器，白板有手写"端到端自动驾驶？"。深夜——只有台灯暖黄光照亮工作区。两张椅子挨着——一张空（人刚走），另一张前坐着（只有背影和屏幕蓝光）。咖啡杯放在空椅子前的桌面上——还在冒气。 |
| **角色出场** | 无正面人物（莎拉背影+师兄背影/不出现） |
| **尺寸** | 1920×1080 |
| **技术备注** | 2017年视觉参考——显示器不是现在的LED宽屏，边框更宽、色彩更暖的蓝。灰尘颗粒在台灯光中浮动。水墨晕染从画面边缘渗入——记忆是被时间漂过的。咖啡杯冒气的特写是情感锚点。 |

**参考Prompt**：
```
Wide shot, 2017-era Chinese university computer lab at midnight, gray floor, old desktop PC cases stacked under desks, CRT/LCD monitors with warm blue glow - thicker bezels warmer color not modern LED, whiteboard with handwritten formulas and "End-to-End Autonomous Driving?" in marker, one desk lamp casting warm yellow light on work area, two chairs pushed close together - one empty one with back-lit silhouette, coffee cup on desk in front of empty chair with steam rising, dust particles floating in lamp beam, warm nostalgia tones with CRT blue, photorealistic base with Chinese ink wash aesthetic, ink bleeding from room edges - memory bleeds, cinematic, 16:9, 8k
```

**负面Prompt**：
```
modern, Apple products, MacBook, bright, clean, luxury, spacious, daytime, people faces visible, smiling, trendy, startup, co-working, exposed brick, Edison bulbs, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头07：外骨骼工具主界面（双显示器）

| 属性 | 内容 |
|------|------|
| **镜号** | 07.1-07.5 |
| **类型** | 远景→中景→特写→近景→中景 |
| **情绪** | 工程的冷静→但屏幕上那些脸是"想象"出来的→一行小字："模型知道'笑'是什么，但不知道'为什么笑'" |
| **核心主体** | 工位双显示器特写（无人物）。左侧：视频输入窗口——莎拉在开放麦台上（有线话筒），画面边缘有播放时间码。中央：虚拟观众渲染——一组"想象"出来的观众脸。其中一张脸标注"第三排左侧·预测笑声强度0.82"（绿色AI框）。右侧：笑声强度热力图——绿色（安全）、黄色（可能响）、红色（大概率会响）。上方一行小字。灰蓝工程色+绿黄红热力色。 |
| **角色出场** | 无（界面特写） |
| **尺寸** | 1920×1080 |
| **技术备注** | 工程化界面——不是科幻HUD。灰蓝工程色+绿黄红热力色。实用工具感。上方小字是灵魂："模型在数百万小时视频数据上预训练——它知道'笑'是什么，但不知道'为什么笑'。" |

**参考Prompt**：
```
Close-up of dual monitors on a Chinese tech worker's desk, left monitor: video player window showing woman on small stage holding wired mic - playback timecode at edge, right monitor: engineering tool interface showing AI world model output - set of rendered virtual audience faces one circled with green AI annotation "Row 3 Left · Predicted Laugh Intensity: 0.82", heat map overlay on audience seats with green (safe) yellow (maybe) red (likely) zones, top text reads "Model pre-trained on millions of hours of video data - it knows 'laugh' but not 'why laugh'", gray-blue engineering palette with green/yellow/red heat map colors, practical tool interface not sci-fi HUD, photorealistic, cinematic, 16:9, 8k
```

**负面Prompt**：
```
sci-fi, hologram, neon, cyberpunk, futuristic, game UI, entertainment, Apple, Tesla, dark mode, glowing, Iron Man, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头08：双标注·小周（机器的绿框 vs 人手的红字）

| 属性 | 内容 |
|------|------|
| **镜号** | 08.1-08.4 |
| **类型** | 特写→极近特写→特写→近景 |
| **情绪** | 同一组数据两种注解→机读世界（绿色矩形框+统计概率）vs 人心世界（红色圆体字+名字） |
| **核心主体** | 外骨骼工具界面局部特写——虚拟观众席第三排。一张渲染的观众脸——绿色AI标注框"第三排左侧·90%有笑声"（机器标注风格：淡绿色矩形框+白色字体）。旁边叠一个红色手写（像在数位板上手写的）"小周"——圆体字、不规整。 |
| **角色出场** | 无（UI特写） |
| **尺寸** | 1920×1080 |
| **技术备注** | 这是"模型盲区"的UI级视觉化：模型看到相关性（A位置有笑声），莎拉看到因果性（小周认识她）。绿框vs红字=机器学习vs人类认知。 |

**参考Prompt**：
```
Close-up of engineering tool UI showing rendered AI audience member face, green AI annotation rectangle around face reading "Row 3 Left · 90% Confidence: Laugh Present" in clean machine font, superimposed red handwritten annotation reading "小周" (Xiao Zhou) in rounded uneven handwriting as if drawn on graphics tablet, two annotation systems coexisting - machine reads statistical probability human reads a name a person, gray-blue engineering interface with green machine annotation and red human handwriting, photorealistic, cinematic, 16:9, 8k
```

**负面Prompt**：
```
sci-fi, hologram, neon, cyberpunk, futuristic, print, typeset, calligraphy, clean, digital-only, Apple, Tesla, dark mode, game UI, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头09：上海地铁早高峰·不在训练数据里的人

| 属性 | 内容 |
|------|------|
| **镜号** | 09.1-09.6 |
| **类型** | 远景→中景→近景→中景→特写→远景 |
| **情绪** | 真实日常→这些人的笑容模型没见过→他们不在任何训练数据集里 |
| **核心主体** | 上海地铁2号线式车厢早高峰7-8点。长条不锈钢座椅+蓝色塑料椅面、天花板扶手环、车门上方红色LED信息屏。车厢拥挤但不窒息——中年女人拎着买菜布袋、学生戴着漏音耳机、老人坐在角落打盹、有人看手机有人发呆。惨白荧光灯管+窗外隧道灯光扫进来。车窗玻璃反射出模糊人影。 |
| **角色出场** | 无特定角色（群像——"不在训练数据里的人"） |
| **尺寸** | 1920×1080 |
| **技术备注** | 真实日常——不是末日、不是科幻、是你我都能认出的地铁。水墨晕染仅在车窗反射中若隐若现——隐喻但不染人。这是全片的"道德核心"镜头——这些人才是莎拉想为之讲段子的人。 |

**参考Prompt**：
```
Wide shot, inside packed Shanghai Metro Line 2-style train during morning rush hour 7-8am, long stainless steel seats with blue plastic surfaces, overhead handrail rings, red LED information display above doors, crowded but not suffocating - middle-aged woman carrying vegetable shopping bag, student with leaky earphones head bobbing slightly, elderly man dozing in corner seat, some on phones some staring into space, cold white fluorescent tube lights, tunnel lights sweeping past through windows, window glass reflecting blurred human figures, real normal unremarkable daily Chinese life, warm gray and cold fluorescent palette, photorealistic base with Chinese ink wash aesthetic, ink bleeding only in window reflections - the people remain real, cinematic, 16:9, 8k
```

**负面Prompt**：
```
empty, futuristic, cyberpunk, neon, fashion, models, selfie, posing, luxury, clean, bright, tourist, Hollywood, disaster, action, fight, dancing, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头10：地铁·莎拉观察·不玩手机的人

| 属性 | 内容 |
|------|------|
| **镜号** | 10.1-10.6 |
| **类型** | 中景→近景→特写→近景→中景→远景 |
| **情绪** | 安静观察→"我学得比它快，因为我有身体"→她想看看那些不在训练数据里的人 |
| **核心主体** | 莎拉站在拥挤早高峰地铁车厢里，一手拉着吊环。她不玩手机——周围所有人都在看手机，几块亮着的屏幕在她周围形成冷白光点阵。她微微转头——目光从买菜袋中年女人扫到漏音耳机的学生、再到打盹的老人。不是盯着看——就是"收进来"。 |
| **角色出场** | 莎拉·赵 |
| **尺寸** | 1920×1080 |
| **技术备注** | 不玩手机是核心细节——在2020年代地铁里不玩手机的人本身就是"不在训练数据里"的。周围手机屏幕的冷白光点阵是视觉锚点。她的目光是"观察"不是"注视"——极安静。水墨晕染仅在她身后的车窗玻璃上浮现。 |

**参考Prompt**：
```
Medium shot, Chinese woman 28 standing in packed morning rush hour subway car, one hand holding overhead handrail ring, she is NOT looking at phone - everyone around her is on their phones forming a matrix of cold white screen glows, her head turns very slightly scanning from middle-aged woman with shopping bag to student with leaky earphones to elderly man dozing, not staring - just taking them in, dark casual clothes, natural look, cold fluorescent and tunnel lights sweeping across, photorealistic base with Chinese ink wash aesthetic, ink bleeding only in window reflection behind her - she is the observer but ink is not on her, extremely quiet composition, cinematic, 16:9, 8k
```

**负面Prompt**：
```
phone, smartphone, scrolling, texting, selfie, posing, smiling, happy, makeup, fashion, tired, sleeping, yawning, empty train, futuristic, cyberpunk, fast motion, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头11：开放麦·台上·0.52的结尾

| 属性 | 内容 |
|------|------|
| **镜号** | 11.1-11.11 |
| **类型** | 中景→近景→特写→近景→特写→中景→特写→近景→特写→中景→近景 |
| **情绪** | 她选了模型预测只有0.52的位置→台下安静零点五秒→然后笑了→不是爆笑是"这个转折我没想到"的笑 |
| **核心主体** | 莎拉站在开放麦舞台上，手持有线麦克风。讲自动驾驶段子："我们公司的自动驾驶升级了…车说'我认识十二种便利店。这是第三种。'…"——安静零点五秒——然后台下笑了。她看到小周在第三排左侧——那个模型标注过的位置——笑了。不是因为他是托，是因为他真的觉得好笑。 |
| **角色出场** | 莎拉·赵、小周（台下）、观众 |
| **尺寸** | 1920×1080 |
| **技术备注** | 0.52是核心数字——模型预测笑声强度0.52，她偏偏选了这个做结尾。零点五秒的安静是真实的停顿（不是喜剧节奏——是她自己也悬着）。随后笑声不是爆笑——是"这个转折我没想到"的密集的轻笑。暖黄聚光灯只照亮莎拉——身后更暗。水墨晕染从舞台边缘渗入暗处。 |

**参考Prompt**：
```
Close-up, Chinese woman 28 on small comedy club stage, warm amber spotlight isolating her against dark background, holding wired microphone mid-delivery, expression shifting in that 0.5 second pause - suspended between joke and response, slight tension in eyes watching audience, dark casual t-shirt, sweat barely visible on temple, intimate vulnerable moment on stage, audience in deep shadow beyond spotlight, photorealistic base with Chinese ink wash aesthetic, warm amber palette with deep shadows, ink bleeding from stage edges into darkness, cinematic, 16:9, 8k
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, smiling broadly, laughing, comedian costume, makeup, jewelry, wireless mic, large stage, Hollywood, crowd visible, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头12：吧台散场·收到林薇的"0.52"

| 属性 | 内容 |
|------|------|
| **镜号** | 12.1-12.7 |
| **类型** | 中景→近景→特写→近景→特写→中景→远景 |
| **情绪** | 散场后的安静→手机亮了→"今天那个结尾，0.52？"→手指在发送键上停了一拍→呼了一口气 |
| **核心主体** | 莎拉侧身坐在打烊后的开放麦酒吧吧台角落。暖暗灯光。舞台上话筒支架空着。手机屏幕亮起冷白光——林薇的微信消息："今天那个结尾，0.52？"冷白屏幕光映在下半张脸。手指已打好回复还未点发送。嘴唇微动——对自己说话/无声复读0.52。然后发送。呼了一口气——不重。 |
| **角色出场** | 莎拉·赵 |
| **尺寸** | 1920×1080 |
| **技术备注** | 这是情感落点。散场后的状态——观众已走、椅子推到桌下。吧台木纹上有啤酒杯水印、空啤酒瓶。手机冷白屏幕光是画面中唯一高亮——其余是暗酒红+暖黄。窗外远处深圳数据中心恒蓝灯光透过玻璃。窗外冷蓝与吧台暖黄在侧脸上微妙交锋。 |

**参考Prompt**：
```
Medium shot, Chinese woman 28 sitting sideways at corner of bar counter in closed comedy club after show, warm dim amber and dark burgundy lighting, stage visible in background with empty mic stand, smartphone screen glowing cold white light illuminating lower half of face - WeChat message visible: "今天那个结尾，0.52？", thumb hovering over send button - reply already typed, lips slightly parted as if silently mouthing "0.52", just finished performing, expressions softer than when on stage, empty beer bottle and water rings on wooden bar counter, distant blue server lights visible through window - cold blue outside vs warm amber inside playing across her profile, photorealistic base with Chinese ink wash aesthetic, ink bleeding from window into darkness, extremely quiet, cinematic, 16:9, 8k
```

**负面Prompt**：
```
smiling, laughing, crowd, party, celebration, cocktail, bright, daytime, stage, performing, dramatic, crying, emotional breakdown, makeup, jewelry, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头13：微信对话·十秒沉默→"好"

| 属性 | 内容 |
|------|------|
| **镜号** | 13.1-13.4 |
| **类型** | 特写→极近特写→特写→近景 |
| **情绪** | 十秒沉默的重量→"对方正在输入..."出现又消失→一个"好"字 |
| **核心主体** | 手机屏幕特写（放在工位桌面上）。微信对话界面——绿色气泡（莎拉）："我想看看那些人""不在训练数据里的人"。白色气泡区域空——"对方正在输入..."三个点跳动→三秒后消失→沉默→约十秒→一个白色气泡："好。"（一个字、有句号）。屏幕上有细小指纹。凌晨蓝灰暗色。 |
| **角色出场** | 无人物（手机屏幕特写） |
| **尺寸** | 1920×1080 |
| **技术备注** | "好"字的句号是关键——不是"好的"不是"好呀"不是"OK"。是师兄听懂了。十秒沉默是真实时间——不是剪辑省略。手机屏幕冷白光唯一光源。水墨晕染从手机边缘渗入桌面暗处。 |

**参考Prompt**：
```
Extreme close-up of smartphone screen on dark desk in blue-gray pre-dawn light, WeChat chat interface: green message bubble reads "我想看看那些人" (I want to see those people), another green bubble "不在训练数据里的人" (The ones not in the training data), white message bubble area empty, "对方正在输入..." typing indicator pulsing three dots, faint fingerprint smudges on screen glass, cold white phone light only illumination - rest is deep blue-gray darkness, photorealistic, intimate minimal, Chinese ink wash aesthetic bleeding from phone edges into dark desk, cinematic, 16:9, 8k
```

**负面Prompt**：
```
bright, daytime, colorful, many messages, group chat, emoji, stickers, GIF, typing fast, notification, iPhone, Apple logo, luxury, clean, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头14：笔记本标签·"段子：不可迁移"

| 属性 | 内容 |
|------|------|
| **镜号** | 14.1-14.4 |
| **类型** | 特写→极近特写→特写→中景 |
| **情绪** | 她想起林薇的话→"有些东西可以备份，有些东西不能。不能备份的那些，才是你。"→合上笔记本 |
| **核心主体** | 深色A5硬壳笔记本封面特写。封面贴着一张白色纸胶带——手写"段子：不可迁移"。字迹不算漂亮——是写代码的人的手写。胶带有微微起翘的角，边缘能看到透明度。桌面上一角隐约有显示器蓝光反射。冷白办公光+一颗台灯暖光打在本子上。水墨晕染从胶带边缘微微洇出——"不可迁移"几个字比别的字洇得更重。 |
| **角色出场** | 无人物（道具特写） |
| **尺寸** | 1920×1080 |
| **技术备注** | "不可迁移"是本集主题词的最终落点——有些东西不能被数字化、不能被模型学到、不能被备份。"段子"也是"人"。胶带质感——普通美工胶带不是高档品牌贴纸。 |

**参考Prompt**：
```
Close-up of dark A5 hardbound notebook cover on office desk, a piece of white masking tape affixed to cover - slightly translucent at edges one corner beginning to lift, handwritten in ballpoint pen in handwriting of someone who writes code not calligraphy: "段子：不可迁移" (Jokes: Not Transferable), slight pressure variations in ballpoint ink, faint blue monitor reflection dancing on desk surface behind, desk lamp casting warm light on one corner, cold office fluorescent overall, photorealistic base with Chinese ink wash aesthetic, ink bleeding from tape edges - "不可迁移" characters bleed slightly more than others, intimate, quiet, cinematic, 16:9, 8k
```

**负面Prompt**：
```
brand, luxury, Moleskine, leather, gold lettering, print, clean, digital, tablet, iPad, bright, colorful, handwriting perfect, calligraphy, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 镜头15：尾声·窗外的黎明

| 属性 | 内容 |
|------|------|
| **镜号** | 15.1-15.5 |
| **类型** | 中景→远景→特写→远景→黑屏 |
| **情绪** | "不是算法预测的下一个窗口。是今天。是现在。"→她不想预测→想坐地铁→拿起包走出剧场 |
| **核心主体** | 莎拉站在剧场窗边。窗外——上海的冬天天亮得很慢。东方的光从楼宇之间漏出来。她看着那些光——不是看数据，是看天。然后拿起包，走出剧场。 |
| **角色出场** | 莎拉·赵 |
| **尺寸** | 1920×1080 |
| **技术备注** | 黎明光是暖金色——从楼宇缝隙漏出来，不是均匀的。窗框在莎拉身上形成剪影。这个画面是"不想预测"的视觉化——她选择去看，而不是被算法告知。水墨晕染从窗外光线中微微渗入——但光比她更亮。 |

**参考Prompt**：
```
Medium shot, Chinese woman 28 standing by window inside small comedy club, looking out at Shanghai winter dawn - the sky lightens very slowly, golden morning light bleeding through gaps between buildings, not a uniform sunrise but fractured by urban skyline, her silhouette against window, she picks up her bag from nearby chair, photorealistic base with Chinese ink wash aesthetic, warm golden dawn light and cool blue-gray pre-dawn shadows, ink bleeding from window frame edges but the light is brighter than the ink, cinematic, 16:9, 8k
```

**负面Prompt**：
```
smiling, happy, sunset, night, dark, dramatic, silhouette only, cartoon, anime, 3D render, oversaturated, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality
```

---

## 全片音效与配乐设计

| 段落 | 音效 | 配乐 |
|------|------|------|
| 后台等待（01.1-01.8）| 台上大学生讲段子（远景笑声）、后台荧光灯微弱嗡鸣、手机消息提示音（短）、扣手机——塑料碰折叠椅的闷响 | 无配乐——后台的声音就够了 |
| 工位·解释外骨骼（02.1-02.12）| 键盘敲击、显示器微弱的电流声、有线耳机里林薇的声音（电话质感）、手指敲屏幕 | 极简电子——不是旋律，是持续的、中性的嗡鸣——像机器在想 |
| 虚拟观众（03.1-04.6）| 微弱的AI渲染声——细微的、合成的环境音（像布料摩擦但太规律）、绿色标注框出现时的UI微音效 | 渐渐加入的不和谐低音——不恐怖，是"不对" |
| 师兄对话（05.1-05.8）| 咖啡杯落桌、办公室空调低频、偶尔远处有人走过 | 无配乐 |
| 实验室闪回（06.1-06.5）| 旧电脑风扇、灰尘——极细微的粒子声、咖啡杯放下——陶瓷碰木桌 | 极简钢琴——中低音区，单一旋律、极慢——记忆的速度 |
| 地铁（09.1-10.6）| 车厢行进声（有节奏的铁轨接缝）、报站广播（女声普通话）、隧道风声、手机屏幕触感——周围人的拇指滑动声 | 无配乐——地铁的声音就是配乐 |
| 开放麦·0.52（11.1-11.11）| 有线话筒的细微近讲效应、0.5秒安静（真正的安静——不是无声）、然后笑声——密的轻的、啤酒杯放回木桌 | 无配乐——台上只有她的声音 |
| 吧台散场（12.1-12.7）| 手机微信消息提示（短）、手指点发送——微弱的触感、远处有人收拾椅子——金属轻碰、呼气 | 极简电子——回到镜头02的嗡鸣主题，但更轻更远 |
| 微信"好"（13.1-13.4）| "对方正在输入..."——三个点的UI微音效、手指在屏幕上的触感、时间——十秒 | 无配乐——沉默是声音 |
| 笔记本（14.1-14.4）| 合上笔记本——纸+硬壳的闷响、胶带角微翘——极其细微 | 极简钢琴——同镜头06的旋律，但只弹一半 |
| 黎明（15.1-15.5）| 窗外远处早班公交的引擎、鸟叫——上海冬天的鸟叫是稀的、包拿起——布摩擦 | 极简钢琴——旋律完成，最后一个音符延音→淡出 |

---

## 制作说明（供ComfyUI参考）

| 项目 | 说明 |
|------|------|
| 片长 | 约8-10分钟 |
| 总镜头数 | 约55-65个 |
| 角色定妆图需求 | 莎拉·赵（3张本集专属状态变体——工位·地铁·吧台，详见T2I Prompts）、师兄（1张——咖啡杯·实验室传奇） |
| 场景图需求 | 开放麦后台（过道+海报墙）×1、公司工位（双显示器）×1、上海地铁车厢（早高峰）×1、大学实验室（2017年）×1、开放麦酒吧吧台（散场后）×1、酒吧窗外黎明×1 |
| 关键道具 | 有线麦克风（不是无线！）、外骨骼工具UI（双显示器界面——虚拟观众渲染+热力图）、手机（微信对话界面）、笔记本+纸胶带（"段子：不可迁移"）、师兄的公司logo咖啡杯 |
| UI界面需求 | 外骨骼AI工具——工程化界面（灰蓝工程色调+绿黄红热力图色）。不是科幻HUD——是实用工具。核心元素：视频播放窗口、虚拟观众渲染区（多张脸+绿框标注）、笑声强度热力图叠加层、数据面板（安全段位/可能笑/大概率不响） |
| 核心视觉需求 | **虚拟观众——不存在的脸在笑**（本集视觉心脏）。渲染vs真实对比——双联构图（上半渲染脸+下半真实小周）。水墨晕染仅在渲染侧——现实不需要洇墨 |
| 动态镜头需求 | 虚拟观众脸渲染动画（I2V——LTX-2.3）、渲染脸→真实脸过渡（I2V——LTX-2.3）、外骨骼UI界面慢推动画、地铁车厢群像微动作、笔记本慢推微距 |
| 旁白录制 | 28岁女性声线（莎拉——北京/普通话，有自嘲的节奏感）、31岁男性声线（师兄——平静、不多话但有重量）、28岁女性声线（林薇——电话/微信，仅声音） |
| 色彩风格 | 四个空间的严格区分：开放麦（暖黄+暗酒红）、公司（冷白+屏幕蓝）、地铁（惨白+暖灰）、实验室（怀旧暖黄+CRT蓝）。全片统一半写实半水墨——水墨晕染程度因空间而异（实验室和虚拟观众侧最多，地铁人群最少） |
| 0.52的数字 | 全片核心数字——模型预测笑声强度0.52。这个数字在UI界面、微信消息、莎拉独白中反复出现。0.52不是"不行"，是"模型不知道"——那是莎拉要去试的地方 |

---

## T2I/I2V交叉引用

| 镜头编号 | T2I Prompt文件 | I2V Prompt镜头编号 |
|---------|---------------|-------------------|
| 镜头01·后台等待 | `13_sarah_01_desk_explaining.png` | 此镜头静态+配音，不需I2V |
| 镜头02·工位解释外骨骼 | `13_sarah_01_desk_explaining.png` + `13_office_01_exoskeleton_ui.png` | 镜头01（Wan 2.2 I2V） |
| 镜头03·虚拟观众脸 | `13_virtual_audience_01_imaginary_face.png` | 镜头07（LTX-2.3 I2V） |
| 镜头04·渲染vs真实 | `13_virtual_audience_02_render_vs_real.png` | 镜头08（LTX-2.3 I2V） |
| 镜头05·师兄 | `13_shixiong_01_coffee.png` | 镜头03（Wan 2.2 I2V） |
| 镜头06·实验室闪回 | `13_lab_01_2017_night.png` | 镜头04（LTX-2.3 I2V） |
| 镜头07·外骨骼UI | `13_office_01_exoskeleton_ui.png` + `13_ui_01_exoskeleton_clean.png` | 镜头02（LTX-2.3 I2V） |
| 镜头08·双标注 | `13_ui_02_double_annotation_xiaozhou.png` | 镜头12（LTX-2.3 T2V） |
| 镜头09·地铁车厢 | `13_subway_01_rush_hour.png` | 镜头05（LTX-2.3 I2V） |
| 镜头10·莎拉地铁观察 | `13_sarah_02_subway_observing.png` | 镜头06（Wan 2.2 I2V） |
| 镜头11·台上0.52 | 动态表情需I2V单独处理 | 对应T2I `13_sarah_03_bar_aftermath.png` 的舞台版本 |
| 镜头12·吧台散场 | `13_sarah_03_bar_aftermath.png` | 镜头11（Wan 2.2 I2V） |
| 镜头13·微信"好" | `13_prop_02_wechat_hao.png` | 镜头10（LTX-2.3 I2V） |
| 镜头14·笔记本标签 | `13_prop_01_notebook_label.png` | 镜头09（LTX-2.3 I2V） |
| 镜头15·黎明 | `13_bar_01_aftermath.png`（部分参考）| 需单独T2I或I2V |

---

## 制作优先级

| 优先级 | 镜头 | 说明 |
|--------|------|------|
| **P0** | 镜头03·虚拟观众脸 | **全片视觉心脏**——不存在的脸在笑 |
| **P0** | 镜头04·渲染vs真实 | **全片道德核心过渡**——上半消融下半继续 |
| **P0** | 镜头02·工位解释外骨骼 | **全片核心思维**——"外骨骼"概念的视觉锚点 |
| **P0** | 镜头12·吧台散场 | **全片情感落点** |
| P1 | 镜头05·师兄 | 主要配角对话 |
| P1 | 镜头10·莎拉地铁观察 | 主要角色微表演——"不玩手机的人" |
| P1 | 镜头11·台上0.52 | 核心表演——那个0.5秒的安静 |
| P2 | 镜头07·外骨骼UI | 关键界面展示 |
| P2 | 镜头08·双标注 | 哲学概念UI——绿框vs红字 |
| P2 | 镜头06·实验室闪回 | 诗意氛围——咖啡杯冒气 |
| P2 | 镜头09·地铁车厢 | 全片道德铺垫——不在训练数据里的人 |
| P3 | 镜头13·微信"好" | 关键道具动画——十秒沉默 |
| P3 | 镜头14·笔记本标签 | 微距诗意——"不可迁移" |
| P3 | 镜头01·后台等待 | 开场建立——静态+配音为主 |
| P3 | 镜头15·黎明 | 尾声氛围 |