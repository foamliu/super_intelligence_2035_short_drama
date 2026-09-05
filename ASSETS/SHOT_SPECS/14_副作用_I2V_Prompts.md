# 第14集《副作用》— I2V/T2V 视频生成 Prompt 规格

> **配合 Workflow**：`workflows/Wan 2.2 图生视频.json`（I2V 高质量，国产优先）、`workflows/Image to Video (LTX-2.3).json`（I2V 备选）
> **输入图像来源**：`ASSETS/SHOT_SPECS/14_副作用_T2I_Prompts.md` 生成的静态图
> **输出分辨率**：Wan 2.2: 640×640 @ 16fps | LTX-2.3: 1280×720 @ 25fps（仅备选）
> **视频时长**：每个镜头 5-10 秒
> **⚠️ 模型策略**：任何情况下优先使用国产模型（Z-Image-Turbo / Wan 2.2），LTX-2.3 / Flux.1 Dev 仅作备选

---

## Workflow 使用策略（国产优先）

| Workflow | 适用场景 | 优势 | 限制 |
|----------|---------|------|------|
| **Wan 2.2 I2V** | 高质量人物表演、微表情、对话镜头（首选） | 14B 模型，动作自然度最高 | 640×640，需后期放大 |
| **Wan 2.2 T2V** | 纯文本生成场景（备选T2V方案） | 无需输入图，灵活 | 角色一致性弱 |
| **LTX-2.3 I2V** | 仅作备选——屏幕内容/UI动画/群像 | 1280×720 | 质量不如 Wan |

---

## 镜头01：莎拉台上讲"塑料袋识别成障碍物"（核心表演段）

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **Wan 2.2 I2V**（人物表演，质量优先） |
| **输入图像** | `14_sarah_02_stage_pause.png`（莎拉在聚光灯下握话筒的静态） |
| **视频时长** | 10 秒 |
| **视频 Prompt（中文）** | 电影级视频，一位28岁中国女性脱口秀演员站在地下小剧场舞台上，暖黄聚光灯只照亮她的脸，身后极暗。她握着有线话筒的手微微收紧，嘴唇从半开的停顿状态慢慢合上又张开——她在讲关于自动驾驶把塑料袋识别成障碍物导致安全带勒人的段子。她的眼神认真，不是笑，是揭露真实问题时的严肃。额角微汗在灯光下反光。话筒的金属网反射暖黄光。台下黑暗中有模糊的啤酒杯。半写实半水墨风格，水墨晕染从聚光灯边缘慢慢洇入黑暗。自然的人物微表情，流畅的动作，电影级光影。 |
| **负面 Prompt** | `smile, laughing, happy, comedy club bright, wireless mic, large venue, Hollywood, makeup, jewelry, bright stage, cartoon, anime, 3D render, static, still, frozen, no movement, deformed face, bad hands` |
| **Seed** | 5401 |
| **输出文件** | `14_sarah_stage_speech.mp4` |

---

## 镜头02：莎拉在工位看BCI模拟器滞后演示（关键道具动画）

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **LTX-2.3 I2V**（需屏幕内容变化） |
| **输入图像** | `14_office_03_desk_simulator.png`（工位双显示器） |
| **视频时长** | 8 秒 |
| **视频 Prompt** | Cinematic video, Chinese woman 28 at office desk, focused expression staring at dual monitors. On left monitor: an autonomous driving simulator showing a virtual road with a car - the car reacts with a visible 0.8 second delay between obstacle detection and braking, the delay highlighted by a pulsing red warning indicator. On right monitor: real dashcam footage paused mid-rain. She tilts her head slightly, a subtle realization dawning - not shock, but the quiet moment of confirming something she suspected. Cold fluorescent office light mixed with warm afternoon window light. Subtle Chinese ink wash bleeding from monitor edges. Natural micro-expressions, smooth motion, cinematic lighting, photorealistic base. |
| **负面 Prompt** | `cartoon, anime, 3D render, static, frozen, still, Apple products, MacBook, hologram, sci-fi, futuristic UI, smiling, happy, makeup, fast motion, jumping, dancing` |
| **Seed** | 5402 |
| **输出文件** | `14_sarah_desk_simulator.mp4` |

---

## 镜头03：观众席反应——台下安静/笑/困惑的混合

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **LTX-2.3 T2V**（纯文本，无需角色一致性） |
| **输入图像** | 无（T2V 模式） |
| **视频时长** | 6 秒 |
| **视频 Prompt** | Cinematic medium shot, small underground comedy club audience of about 30 Chinese young professionals in Shenzhen, warm amber dim lighting. A range of subtle reactions rippling through the crowd: some people shifting in their seats uncomfortably as they realize the comedian is not joking about the BCI lag being dangerous, one person slowly putting down their beer glass with a thoughtful expression, another person's slight nod of recognition. Not laughing - processing. Warm yellow spotlight edge catching faces in the dark. Watercolor ink bleeding at the edges of the frame - the unease seeping into the visual. Natural human micro-movements, breathing, blinking, weight shifting. Documentary realism. |
| **负面 Prompt** | `laughing, smiling, happy, party, celebration, bright, large venue, Hollywood, cartoon, anime, 3D render, static, frozen, still, deformed faces, duplicate people, bad hands` |
| **Seed** | 5403 |
| **输出文件** | `14_audience_reaction.mp4` |

---

## 镜头04：李晖在茶水间倒咖啡、说话

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **Wan 2.2 I2V**（人物对话表演） |
| **输入图像** | `14_lihui_01_breakroom_coffee.png`（李晖端咖啡） |
| **视频时长** | 8 秒 |
| **视频 Prompt** | 电影级视频，27岁中国年轻程序员在科技公司茶水间，手里端着公司logo咖啡杯，眼下有明显的黑眼圈。他靠在白色冰箱旁边，侧着头跟画外的莎拉说话——嘴唇在动，做出"宣讲会是下午三点"的口型。他耸肩了一下，对BCI脑控汽车这件事不以为然——嘴角微撇。冷白荧光从天花板直射，微波炉在背景嗡嗡运转。他吸了一口咖啡。自然的人物动作，说话时的微表情，疲惫但不颓废的程序员日常感。半写实风格。 |
| **负面 Prompt** | `smile, happy, energetic, well-rested, luxury office, modern cafe, Apple products, warm lighting, bright daylight, cartoon, anime, 3D render, static, frozen, still, deformed face, bad hands` |
| **Seed** | 5404 |
| **输出文件** | `14_lihui_breakroom_talk.mp4` |

---

## 镜头05：未来学家在投影前微笑略过问题

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **LTX-2.3 I2V** |
| **输入图像** | `14_futurist_01_presentation.png`（未来学家在大投影前） |
| **视频时长** | 6 秒 |
| **视频 Prompt** | Cinematic video, Chinese man 50s in dark business casual suit standing before a large projection screen showing "2035 Brain-Controlled Cars Will Be Mainstream" concept graphics in blue. He holds a laser pointer. His mouth moves in a polished corporate cadence - the practiced rhythm of someone who has given this presentation dozens of times. He gives a slight professional smile and gestures to the next slide, smoothly sidestepping a question from off-screen. The projection blue light reflects on half his face. Cold white conference room fluorescent. His expression is sincere - he genuinely believes what he's saying, which makes it more unsettling. Subtle ink wash bleeding from projection edges. Natural speaking movements. |
| **负面 Prompt** | `evil, villain, sinister, angry, threatening, cartoon, anime, 3D render, static, frozen, still, warm lighting, cozy, hologram, sci-fi` |
| **Seed** | 5405 |
| **输出文件** | `14_futurist_presentation.mp4` |

---

## 镜头06：莎拉在吧台——脱口秀讲完后的安静

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **Wan 2.2 I2V**（人物情感表演，最高质量） |
| **输入图像** | `14_sarah_03_bar_beer.png`（莎拉吧台啤酒手机朝下） |
| **视频时长** | 10 秒 |
| **视频 Prompt** | 电影级视频，28岁中国女性侧身坐在深夜酒吧吧台前，暖暗灯光。她慢慢转动手中冰啤酒瓶——瓶底在深色木纹吧台上留下一小圈水印。手机屏幕朝下扣在旁边，屏幕亮了一下（微信消息），但她没有翻过来看——她注意到了但选择忽略。她抬起眼看着窗外——深圳夜景，远处数据中心恒蓝的灯光沉在夜幕中。她呼了一口气——不重，不是说完了就轻松了，是说完了就完了。嘴角没有上扬。呼吸使肩膀微微起伏。窗外蓝色冷光与吧台暖黄灯光在她侧脸上微妙交锋。半写实半水墨，水墨晕染从窗外渗入。极安静的视频——动作是"几乎不动"。 |
| **负面 Prompt** | `smiling, laughing, crowd, party, celebration, cocktail, bright, daytime, stage, performing, cartoon, anime, 3D render, static, frozen, fast motion, dramatic, crying` |
| **Seed** | 5406 |
| **输出文件** | `14_sarah_bar_aftermath.mp4` |

---

## 镜头07：道具特写——EEG头环上的汗渍（微距慢推）

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **LTX-2.3 I2V**（微距物体） |
| **输入图像** | `14_prop_01_eeg_headband.png`（EEG头环汗渍特写） |
| **视频时长** | 5 秒 |
| **视频 Prompt** | Cinematic macro video, slow push-in on a white plastic EEG headband on a dark desk surface. The green LED on the sensor blinks at a steady rhythm - once every 2 seconds, like a quiet heartbeat of the machine. Visible sweat residue and skin oil marks on the inner contact surface - traces of long wear. The camera slowly pushes in closer, revealing the texture of the plastic and the sweat marks in intimate detail. Cold white office light with subtle green LED pulse. Ink wash bleeding slowly from the edges. The headband lies still - only the LED blinks and the camera moves. Minimal, meditative, unsettling. |
| **负面 Prompt** | `futuristic, sci-fi, glowing, neon, high-tech, clean, brand new, shiny, hologram, cyberpunk, cartoon, anime, fast motion, camera shake, handheld` |
| **Seed** | 5407 |
| **输出文件** | `14_eeg_headband_push.mp4` |

---

## 镜头08：道具特写——有线话筒放回支架

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **LTX-2.3 I2V** |
| **输入图像** | `14_prop_02_mic_beer.png`（话筒+啤酒双联构图） |
| **视频时长** | 5 秒 |
| **视频 Prompt** | Cinematic video, split composition. Upper half: a wired microphone being gently placed back onto its black stand on a small dark stage - the thick black cable uncoiling slightly on the stage floor. Spotlight reflects warm amber off the metal mesh. Lower half: on a dark wooden bar counter, a freshly opened beer bottle - foam slowly rising then settling at the neck, condensation droplet slowly sliding down the glass, leaving a trail. Next to it, a stainless steel bottle opener. The warmth of the stage above, the quiet of the bar below. Ink wash bleeding slowly between the two halves. Slow, contemplative pacing. |
| **负面 Prompt** | `wireless mic, modern, fancy, champagne, wine, cocktail, bright, daylight, cartoon, anime, 3D render, static, frozen, fast motion, people` |
| **Seed** | 5408 |
| **输出文件** | `14_mic_beer_transition.mp4` |

---

## 镜头09：模拟器 UI 概念动画——训练集统计面板的"400"

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **LTX-2.3 T2V**（UI 动画，纯文本生成更可控） |
| **输入图像** | 无（T2V 模式），可选参考 `14_ui_01_sim_training_stats.png` |
| **视频时长** | 8 秒 |
| **视频 Prompt** | Cinematic screen recording of an autonomous driving simulator interface - practical engineering tool, not sci-fi HUD. The screen scrolls slowly through training dataset statistics: "Normal driving: 8,200,000" highlighted green, then "Sunny car-following: 3,500,000" in green, then "Pedestrian sudden dash-out: 12,000" in yellow, and finally stopping at "Child chasing ball: 400" - this last number is dim white-gray, not red, just insufficient. The cursor hovers over "400" for a moment. A subtle pulsing amber indicator blinks next to it. The scroll pauses here - letting the number sit. Gray-blue engineering interface with green status lights. Realistic software UI animation - no flashy transitions, no sci-fi elements. |
| **负面 Prompt** | `sci-fi, hologram, neon, cyberpunk, futuristic, game UI, entertainment, Apple, Tesla, dark mode, colorful, fast scrolling, 3D, cartoon, anime, people, human` |
| **Seed** | 5409 |
| **输出文件** | `14_sim_ui_scroll_400.mp4` |

---

## 镜头10：开放麦酒吧环境建立——台下视角

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **LTX-2.3 I2V** |
| **输入图像** | `14_bar_01_audience_view.png`（从舞台看观众席） |
| **视频时长** | 6 秒 |
| **视频 Prompt** | Cinematic video, first-person view from a small underground comedy club stage in Shenzhen looking out at about 30 audience members at small round tables. Warm amber dim lighting. Natural ambient motion: someone sips beer (golden liquid level drops slightly), another person cracks sunflower seeds (small hand movement), a beer glass is set down on a wooden table with a soft clink. A person shifts in their chair. The room breathes. Dust particles floating in the spotlight beam. Ink wash bleeds slowly from the dark edges of the room. Live recorded atmosphere, not staged. Documentary realism. |
| **负面 Prompt** | `large venue, bright stage, Hollywood, modern bar, cocktail lounge, crowded, empty, daytime, windows, natural light, cartoon, anime, 3D render, static, frozen, dancing, party, celebration` |
| **Seed** | 5410 |
| **输出文件** | `14_bar_ambient.mp4` |

---

## 镜头11：窗外深圳夜景——数据中心蓝光沉入夜色

| 属性 | 内容 |
|------|------|
| **使用 Workflow** | **LTX-2.3 I2V** |
| **输入图像** | `14_bar_02_window_night.png`（吧台窗外夜景） |
| **视频时长** | 7 秒 |
| **视频 Prompt** | Cinematic video, view through a bar window at night in Shenzhen. City skyline with glass skyscrapers reflecting neon lights. In the distance, several buildings glow with the steady blue light of data centers - real server room LED blue, not cyberpunk. The blue lights pulse very subtly - not dramatic, just the natural variation of server activity. Clouds move slowly across the night sky. The warm amber reflection of the bar interior subtly visible on the window glass surface. The city breathes - millions of people and machines, both alive. Ink wash bleeding at the very edges only - the city is real, the metaphor is the bleeding. |
| **负面 Prompt** | `cyberpunk, neon, futuristic, sci-fi, Hong Kong, Tokyo, Times Square, daylight, flying cars, hologram, cartoon, anime, 3D render, static, frozen, fast motion, timelapse` |
| **Seed** | 5411 |
| **输出文件** | `14_window_shenzhen_night.mp4` |

---

## 制作优先级（ComfyUI 走视频顺序）

| 优先级 | 镜头 | Workflow | 时长 | 说明 |
|--------|------|----------|------|------|
| **P0** | 镜头01·莎拉台上讲段子 | Wan 2.2 I2V | 10s | **全片核心表演**——脱口秀节奏+微表情 |
| **P0** | 镜头06·莎拉吧台安静 | Wan 2.2 I2V | 10s | **全片情感落点**——几乎不动的表演 |
| P1 | 镜头02·工位看BCI滞后 | LTX-2.3 I2V | 8s | 屏幕动画+角色反应 |
| P1 | 镜头04·李晖茶水间 | Wan 2.2 I2V | 8s | 主要配角对话 |
| P2 | 镜头03·观众席反应 | LTX-2.3 T2V | 6s | 群体微反应（不需角色一致） |
| P2 | 镜头05·未来学家宣讲 | LTX-2.3 I2V | 6s | 配角讲话 |
| P3 | 镜头09·UI滚动到"400" | LTX-2.3 T2V | 8s | UI概念动画 |
| P3 | 镜头10·酒吧环境 | LTX-2.3 I2V | 6s | 场景氛围 |
| P3 | 镜头07·EEG头环慢推 | LTX-2.3 I2V | 5s | 微距道具 |
| P4 | 镜头08·话筒放回支架 | LTX-2.3 I2V | 5s | 过渡镜头 |
| P4 | 镜头11·窗外夜景 | LTX-2.3 I2V | 7s | 氛围结尾 |

---

## 文件命名规范

```
14_{内容}_{简短描述}.mp4

表演: 14_sarah_stage_speech.mp4
      14_sarah_bar_aftermath.mp4
      14_lihui_breakroom_talk.mp4
      14_futurist_presentation.mp4

场景: 14_audience_reaction.mp4
      14_bar_ambient.mp4
      14_window_shenzhen_night.mp4

道具: 14_sarah_desk_simulator.mp4
      14_eeg_headband_push.mp4
      14_mic_beer_transition.mp4

UI:   14_sim_ui_scroll_400.mp4