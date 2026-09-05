# 第14集《副作用》T2I SHOT SPECS

> **对应分镜**：`SCENES/14_副作用.md`  
> **核心角色**：莎拉·赵（自动驾驶工程师+业余脱口秀演员）、李晖、未来学家、脱口秀老板  
> **视觉基调**：双空间交替——开放麦酒吧暖黄琥珀暗酒红 vs 公司冷白荧光蓝。闪回用"意识漂移"过渡（不是传统滤镜，是灯光/环境音的渐变）。半写实半水墨风格统一。  
> **总镜头数**：约55  
> **尺寸统一**：1280×720（16:9）

---

## 角色IP-Adapter交叉引用

| 角色 | 定妆规格路径 | 备注 |
|------|-------------|------|
| 莎拉·赵 | `ASSETS/CHARACTERS/08_莎拉·赵/定妆规格.md` | 28岁，深色T恤/简约外套+牛仔裤，台上台下同一套衣服——这是细节 |
| 李晖 | 待创建 | 27岁，黑眼圈，咖啡杯不离手 |
| 未来学家 | 待创建 | 50岁左右，西装+激光笔，不是坏人——是相信自己在说真话的人 |
| 脱口秀老板 | 待创建 | 40多岁，吧台旁，啤酒起子 |

---

## 双空间视觉规范

| 元素 | 开放麦酒吧 | 公司（茶水间/会议室/工位） |
|------|-----------|---------------------------|
| 色调 | 暖黄+琥珀+暗酒红，所有灯光暖 | 冷白+荧光蓝，白色墙壁+工业照明 |
| 氛围 | 亲密、暴露、自由但脆弱 | 冰冷、结构化、压制的疑问 |
| 光 | 舞台灯只照亮莎拉——身后更暗，完全暴露 | 均匀冷白，没有阴影可躲 |
| 转场 | — | "意识漂移"：莎拉在台上说，背景灯光褪色、环境音变为办公室声 |

---

## 镜头00：开放麦后台

| 属性 | 内容 |
|------|------|
| **镜号** | 00.1-00.6 |
| **类型** | 远景→特写→近景→黑屏 |
| **情绪** | 犹豫→决定→"有些话不说出来会一直在脑子里转" |
| **核心主体** | 地下酒吧后台狭窄过道，墙上贴满脱口秀海报。莎拉靠着墙看手机段子草稿，决定换主题 |
| **角色出场** | 莎拉·赵（犹豫→决定）、大学生（远景模糊） |
| **尺寸** | 1280×720 |
| **技术备注** | 手机屏幕显示段子草稿备忘录。墙上海报质感——纸+胶带。酒吧过道暖黄灯光。决定性瞬间：她把手机放进口袋、拿起话筒——这个动作要慢一拍 |

**参考Prompt**：
```
Wide shot, basement open-mic bar backstage narrow corridor, warm amber lighting, walls covered with comedy posters taped unevenly, young Chinese woman 28 years old leaning against wall holding smartphone with Chinese text on screen, looking at phone hesitantly, dark casual t-shirt jeans, photorealistic base with Chinese ink wash aesthetic, warm amber and dark burgundy palette, ink bleeding at corridor edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, modern luxury bar, cocktail lounge, smiling, glamorous
```

---

## 镜头01：茶水间（闪回·白天）

| 属性 | 内容 |
|------|------|
| **镜号** | 01.1-01.9 |
| **类型** | 中景→近景→特写→中景 |
| **情绪** | 日常→被一句话击中→"微波炉又开始转了" |
| **核心主体** | 公司茶水间——冷白荧光、微波炉嗡嗡转、冰箱。李晖端着咖啡进来，黑眼圈，说BCI宣讲会的事 |
| **角色出场** | 莎拉·赵、李晖 |
| **尺寸** | 1280×720 |
| **技术备注** | 冷白荧光是茶水间的"签名"。微波炉转动的嗡声——日常但压迫。李晖说"意念接管"时莎拉筷子停半空——这个瞬间要冻结一拍。水墨晕染从荧光灯边缘渗入。 |

**参考Prompt**：
```
Medium shot, Chinese tech company break room, cold white fluorescent light, white refrigerator, microwave humming, two young Chinese colleagues in casual tech attire, woman holding lunch box with chopsticks paused mid-air, man with dark circles holding coffee mug with company logo, conversation scene, photorealistic base with Chinese ink wash aesthetic, cold white and steel blue palette, ink bleeding from fluorescent tube edges, sterile corporate atmosphere, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, warm lighting, cozy cafe, smiling, laughter
```

---

## 镜头02：开放麦·开场（现在）

| 属性 | 内容 |
|------|------|
| **镜号** | 02.1-02.5 |
| **类型** | 远景→近景→中景→近景 |
| **情绪** | 从日常到"今天换主题了" |
| **核心主体** | 莎拉站在舞台灯光下，台下三十多人。她抬了抬话筒支架："今天不讲自动驾驶了。" |
| **角色出场** | 莎拉·赵 |
| **尺寸** | 1280×720 |
| **技术备注** | 从舞台视角看台下——三十多张脸，有人在喝啤酒，有人在嗑瓜子。灯光暖黄但不太亮——刚好够照到舞台。莎拉身后比常规脱口秀场馆更暗——给人完全暴露的感觉。话筒是有线的——不是无线。 |

**参考Prompt**：
```
Wide shot from stage perspective, small underground comedy club in Shenzhen, warm amber stage light illuminating single Chinese woman 28 on stage holding wired microphone, audience of about 30 people in dim warm lighting drinking beer eating sunflower seeds, dark intimate atmosphere, stage light only illuminates performer everything behind darker than normal comedy club, photorealistic base with Chinese ink wash aesthetic, warm amber and dark burgundy palette, ink bleeding from stage edges into darkness, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, wireless microphone, large venue, bright stage, spotlight, glamorous, Hollywood, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts
```

---

## 镜头03：会议室（闪回·去年）

| 属性 | 内容 |
|------|------|
| **镜号** | 03.1-03.9 |
| **类型** | 远景→中景→近景→特写→中景→特写→黑屏 |
| **情绪** | 权威宣讲→被一个简单问题刺穿→被"不需要回答这个"压下去 |
| **核心主体** | 大投影前未来学家讲"2035年脑控汽车将成为主流"，台下掌声。莎拉举手问"您戴过EEG头环吗？"——被微笑略过 |
| **角色出场** | 未来学家、莎拉·赵（台下举手）、百多名员工 |
| **尺寸** | 1280×720 |
| **技术备注** | 投影内容：2035年脑控汽车概念图——蓝色曲线、箭头、"万亿市场"。未来学家的微笑——"这个问题很有趣但不重要"的微笑。莎拉把举着的手放下来——这个动作是核心。水墨晕染在屏幕蓝光区域。 |

**参考Prompt**：
```
Wide shot, corporate all-hands meeting in Chinese tech company, large projection screen showing futuristic brain-controlled car concept with blue curves and trillion-market text, middle-aged male futurist in suit with laser pointer speaking confidently, audience of about 100 employees applauding, cold white fluorescent lighting, photorealistic base with Chinese ink wash aesthetic, cold white and projection blue palette, ink bleeding from screen edges, sterile corporate atmosphere, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, warm lighting, cozy, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry
```

---

## 镜头04：开放麦·BCI段子（现在）

| 属性 | 内容 |
|------|------|
| **镜号** | 04.1-04.13 |
| **类型** | 近景→近景→中景→近景→特写→中景 |
| **情绪** | 笑话节奏加快→"你愿意为了不用动手切歌在头上开个洞吗？"→突然变重："外卖小哥的意念呢？谁来听？" |
| **核心主体** | 莎拉在台上讲BCI——从医疗奇迹到消费级荒谬，从HR玩笑到那个让人安静的问题 |
| **角色出场** | 莎拉·赵 |
| **尺寸** | 1280×720 |
| **技术备注** |节奏变化：4.1-4.5轻快→4.6-4.9逐渐沉→4.11停在"元年永远在明年"→4.12致命一击——"外卖小哥的意念呢？"这个停顿要真实时间（不是喜剧节奏——是她真的在犹豫要不要问）。台下一瞬间安静。有人在转啤酒杯。 |

**参考Prompt**：
```
Close-up, young Chinese woman 28 on comedy club stage, warm amber spotlight, speaking into wired microphone, expression shifting from humorous to genuine concern, dark casual t-shirt, beads of sweat barely visible on temple, stage light isolating her against dark background, intimate vulnerable moment mid-performance, photorealistic base with Chinese ink wash aesthetic, warm amber palette with deep shadows, ink bleeding from spotlight edges, cinematic shallow depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, smiling broadly, comedian costume, makeup, jewelry, wireless mic, large stage, Hollywood, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts
```

---

## 镜头05：工位（闪回·去年）

| 属性 | 内容 |
|------|------|
| **镜号** | 05.1-05.7 |
| **类型** | 中景→特写→近景→特写→近景→特写→中景 |
| **情绪** | 亲身验证→物理不适→在笔记本上写"紧箍咒。不是比喻。" |
| **核心主体** | 莎拉戴EEG头环——白色塑料发箍式。额头红了，手指不自觉在挠。屏幕上是路口场景——她用力"想"刹车，有滞后。摘下头环，头发压平了 |
| **角色出场** | 莎拉·赵 |
| **尺寸** | 1280×720 |
| **技术备注** | EEG头环细节：传感器位置有汗渍造成的微小水痕。桌面有半盒打开的藿香正气水——细节。测试笔记本上写满"滞后0.8s"、"注意力消耗高"。显示器上自动驾驶模拟器——实用型工程界面。把头环放回包装盒——盒子上模特笑得很开心——这个对比是核心。 |

**参考Prompt**：
```
Medium shot, Chinese woman 28 at office desk wearing white plastic EEG headband like hairband, two monitors showing autonomous driving simulator interface, forehead reddened under headband sensors, fingers unconsciously scratching temple, wilted potted plant on desk half-open box of Chinese medicine, late afternoon light from window, photorealistic base with Chinese ink wash aesthetic, cold office fluorescent mixed with warm window light, ink bleeding at edges, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, smiling, happy, high-tech futuristic office, Apple products, MacBook, luxury, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts
```

---

## 镜头06：开放麦·量子计算段子（现在）

| 属性 | 内容 |
|------|------|
| **镜号** | 06.1-06.8 |
| **类型** | 近景→中景→近景→特写→中景→近景→中景 |
| **情绪** | 从物理尺寸的荒诞→"破解你所有密码"的寒意→"他们现在忙着算别的东西——没空看你的聊天记录"不安的笑 |
| **核心主体** | 莎拉切换话题——量子计算。压低声音说"它能在一秒钟内破解你所有的密码"。台下有人把啤酒杯放下了 |
| **角色出场** | 莎拉·赵 |
| **尺寸** | 1280×720 |
| **技术备注** |量子计算段子的音效设计：说"绝对零度"时——微弱的低温感应音。说"破解你所有的密码"时——不引人注目但可感的低沉电子音。台下不安的笑——不是被逗笑，是后怕。 |

**参考Prompt**：
```
Medium shot, Chinese woman 28 on comedy club stage, leaning slightly forward, voice lowered, warm amber light creating intimate tension, audience silhouettes in foreground with beer glasses still on tables, some audience members exchanging uncomfortable glances, moment of collective unease in comedy club, photorealistic base with Chinese ink wash aesthetic, warm amber palette with deep shadows, ink bleeding from darkness edges, dramatic chiaroscuro, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, laughter, smiling audience, comedy club bright, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts
```

---

## 镜头07：自动驾驶模拟器（闪回）

| 属性 | 内容 |
|------|------|
| **镜号** | 07.1-07.6 |
| **类型** | 中景→特写→近景→特写→近景→特写 |
| **情绪** | 五年的经验压缩进一个画面——模拟器里的成功和真实道路之间隔着一条河 |
| **核心主体** | 莎拉在模拟器前。虚拟道路完美→切换真实道路录影——车经过水坑时传感器乱了，塑料袋→急刹。训练集统计：小孩追球: 400样本 |
| **角色出场** | 莎拉·赵 |
| **尺寸** | 1280×720 |
| **技术备注** | 模拟器UI：左侧虚拟道路+车辆模型，右上角错误日志，底部训练集统计面板。关键数据："小孩追球: 400"vs"正常驾驶: 8,200,000"——数字本身是戏剧。真实道路录影的急刹——声音、震动、安全带勒进肩膀。桌面壁纸——她自己开车去西北的照片。 |

**参考Prompt**：
```
Medium shot, Chinese woman 28 at office desk staring at monitors, two screens showing split view: left screen autonomous driving simulator with PERFECT road conditions green test-passed banner, right screen real dashcam footage of car emergency braking plastic bag floating across rainy road, training data statistics panel visible showing stark numbers "SCENE: CHILD CHASING BALL: 400 SAMPLES", early evening light through window, expression of deep contemplation not frustration, photorealistic base with Chinese ink wash aesthetic, muted blue-gray palette with screen glow, ink bleeding from monitor edges, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, futuristic UI, hologram, sci-fi, Apple products, smiling, happy, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts
```

---

## 镜头08：开放麦·收尾（现在）

| 属性 | 内容 |
|------|------|
| **镜号** | 08.1-08.9 |
| **类型** | 近景→特写→近景→中景→近景→中景→近景 |
| **情绪** | 声音沉下来→"河的名字叫物理"→台下一秒钟安静→掌声比平时响一点 |
| **核心主体** | 莎拉回到自动驾驶的真问题——不是算力不够，是物理世界太脏。小孩突然冲出来——训练集里永远稀缺 |
| **角色出场** | 莎拉·赵 |
| **尺寸** | 1280×720 |
| **技术备注** |她说"河的名字叫物理"时——一秒纯静，然后微微钢琴进入。这是全片核心台词。掌声不是爆笑后热烈——是"你说得有点道理"的礼貌。她把话筒放回支架——这个动作比上台时轻。 |

**参考Prompt**：
```
Close-up, young Chinese woman 28 on comedy club stage, warm amber spotlight, expression earnest and vulnerable, speaking final words with weight of five years experience, slight smile not of happiness but of acceptance, wired microphone in hand about to place back on stand, stage light isolating her against deep darkness, intimate cinematic moment, photorealistic base with Chinese ink wash aesthetic, warm amber and soft gold palette, ink bleeding softly from edges, shallow depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright smile, triumphant, victory pose, large stage, glamorous, Hollywood ending, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts
```

---

## 镜头09：吧台（现在·之后）

| 属性 | 内容 |
|------|------|
| **镜号** | 09.1-09.11 |
| **类型** | 中景→近景→特写→远景→近景→特写→近景→远景→黑屏 |
| **情绪** | 老板递啤酒→"你今天讲的不像脱口秀"→"像你在公司没说完的话"→手机扣在桌上→啤酒是凉的 |
| **核心主体** | 吧台暗光下，莎拉喝了一口啤酒。窗外深圳夜色——数据中心的蓝光沉下去。手机屏幕亮——李晖消息。她不回 |
| **角色出场** | 莎拉·赵、脱口秀老板 |
| **尺寸** | 1280×720 |
| **技术备注** | 啤酒瓶起子打开的细节——泡沫涌上来。瓶底在吧台上留下的凉水环印在木纹上。手机屏幕朝下扣在吧台——一个"不再看了"的手势。黑屏字幕："你以为的技术局限——其实是你身体里的每条血管在说：'慢一点'。" |

**参考Prompt**：
```
Medium shot, bar counter in underground Shenzhen comedy club, warm dim amber lighting, Chinese woman 28 sitting at bar holding cold beer bottle with condensation, middle-aged bar owner wiping hands with towel nearby, smartphone placed face-down on wooden bar counter, water ring from bottle base on wood grain, window in background showing Shenzhen night cityscape with data center blue lights fading into darkness, intimate quiet post-performance atmosphere, photorealistic base with Chinese ink wash aesthetic, warm amber and dark navy palette, ink bleeding from window edges, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, crowd, party, celebration, luxury bar, cocktail, smiling broadly, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts
```

---

## 全片音效与配乐设计

| 段落 | 音效 | 配乐 |
|------|------|------|
| 后台（00.1-00.6）| 远处演员说话声、暖气管微响、手机按键 | 极简电子——偶尔音符，像在思考中漂浮的念头 |
| 茶水间（01.1-01.9）| 微波炉嗡嗡、咖啡机、冷白荧光电流声、杯子放桌子 | 无配乐——让办公室声音和对话主导 |
| 开场（02.1-02.5）| 吧台啤酒瓶碰撞、椅子移动、背景聊天 | 无配乐——脱口秀是最干净的舞台声音 |
| 会议室（03.1-03.9）| 投影仪风扇、翻笔记本、掌声 | 微弱低沉嗡声——在掌声时，营销话语的背景震动 |
| BCI段子（04.1-04.13）| 纯脱口秀音效——莎拉声音、台下反应、啤酒杯放桌上 | 无配乐——依赖莎拉节奏 |
| 工位（05.1-05.7）| EEG头环电流、键盘、模拟器环境声、远处深圳车流 | 极简合成器——微弱不和谐频率，对应头环发痒感 |
| 量子段子（06.1-06.8）| 脱口秀音效+说"绝对零度"时微弱低温感应音+说"破解密码"时低沉电子音 | 无配乐——用声音设计做质感，不用音乐 |
| 模拟器（07.1-07.6）| 模拟器环境声、真实道路录影雨声急刹、小孩远处笑声 | 极简钢琴——几个低音键，安静的、持续的差距 |
| 收尾（08.1-08.9）| 脱口秀音效、台下安静、莎拉更放松的声音 | "河的名字叫物理"时一秒纯静，然后微微钢琴进入 |
| 吧台（09.1-09.11）| 啤酒瓶起子、倒啤酒、远处下一场脱口秀、深圳夜交通声 | 温暖吉他——短小、不间断，比背景音乐更私密 |

---

## 制作说明（供ComfyUI参考）

| 项目 | 说明 |
|------|------|
| 片长 | 约6-8分钟 |
| 总镜头数 | 约55个 |
| 需AI生图的核心镜头 | 约12-15个（角色定妆、场景图、关键帧），其余为脱口秀现场/闪回对话/黑屏字幕等 |
| 角色定妆图需求 | 莎拉·赵（已完成——见`ASSETS/CHARACTERS/08_莎拉·赵/定妆规格.md`）、李晖（1个——27岁、黑眼圈、咖啡杯）、未来学家（1个——50岁、西装+激光笔）、脱口秀老板（1个——40多岁、吧台旁） |
| 场景图需求 | 开放麦酒吧（地下室式、暖黄灯、小舞台、吧台、墙上贴海报、约30人观众席）、公司茶水间（冷白荧光、微波炉、冰箱、白色墙壁）、公司会议室（大投影、明亮、百人规模）、莎拉工位（两台显示器、自动驾驶模拟器界面、快死的绿植） |
| 关键道具 | 有线话筒（不是无线——增加酒吧质感）、莎拉手机（屏幕显示段子草稿备忘录）、EEG头环（白色塑料发箍式、传感器有汗渍）、自动驾驶模拟器UI（实用工程工具——左侧虚拟道路+车辆，右上角错误日志，底部训练集统计面板——关键数据"小孩追球: 400"）、啤酒瓶+起子、藿香正气水半盒（工位细节） |
| 闪回转场设计 | 不是传统"闪回滤镜"。用"意识漂移"——莎拉在台上说，背景灯光逐渐褪色，环境音变为办公室声音。回到舞台时，反方向过渡。两种空间的光温差异本身就是转场语言 |
| 色彩风格 | 开放麦酒吧：暖黄+琥珀+暗酒红（所有灯光暖）。公司：冷白+荧光蓝（白色墙壁+工业照明）。闪回切换用调色区分——不需要文字"去年"，冷白色本身就是"公司"语言 |
| 莎拉表演笔记 | 脱口秀不是"讲笑话"——是"把心里的石头翻过来给你们看"。台上比公司更自由但更脆弱。4.12节关键停顿——不是喜剧节奏，是"她真的在犹豫要不要问"。所有停顿保持真实时间 |