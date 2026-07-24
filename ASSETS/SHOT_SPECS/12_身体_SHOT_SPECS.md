# 第12集《身体》— T2I SHOT_SPECS

> **场景数**：8 | **镜头数**：11（核心镜头） | **预估时长**：8-10分钟  
> **参考分镜**：`SCENES/12_身体.md`  
> **风格锚点**：`ASSETS/视觉总纲.md` — 章节色 `#FFD700`（暖金）  
> **核心张力**：暖（赵淑芬/晨光/棉布）vs 冷（小暖/金属/指示灯）

---

## 场景1：清晨·卧室

> **场景编号**：SC-12-01  
> **情绪基调**：身体衰退的日常、机器人的首次出现  
> **环境**：老年公寓卧室，晨光半明半暗  
> **色调**：暖灰+晨光金

### SHOT-12-01

| 字段 | 内容 |
|------|------|
| **镜号** | 1.1 |
| **类型** | 特写 |
| **情绪** | "又要经历一遍"的平静无奈 |
| **核心主体/意象** | 赵淑芬左手放在左膝盖上，指节粗大变形，皮肤松弛 |
| **角色出场** | 赵淑芬（72岁，浅蓝旧睡衣，棕红色老花镜滑到鼻尖） |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`赵淑芬/01_床边`。开场第一个镜头。左手关节炎特写——指节粗大、变形、皮肤松弛。晨光照在半边手上，另半边在阴影里。背景虚化——床单、药瓶隐约可见。 |

**参考Prompt**

```
Extreme close-up of a 72-year-old Chinese woman's left hand resting on left knee,
knuckles swollen and deformed from arthritis, skin loose and thin,
age spots on back of hand—irregular brown patches,
faint blue veins visible through translucent skin,
morning light from window casting on half the hand, other half in shadow,
light blue worn pajama sleeve visible,
bedside table in background blurred—medicine bottles, reading glasses,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm grey and soft ochre, 焦墨 for knuckle shadows,
淡赭 for age spots, emphasis on skin transparency,
extreme shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn hand,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry entire image, watermark, text, logo, oversaturated,
anime, cartoon, illustration, 3D render,
young hand, smooth skin, manicured nails, perfect hand,
bright neon, saturated colors, Western oil painting, CGI look
```

---

### SHOT-12-02

| 字段 | 内容 |
|------|------|
| **镜号** | 1.5 |
| **类型** | 全景 |
| **情绪** | 警惕、未知、晨光中的白色轮廓 |
| **核心主体/意象** | 小暖站在卧室门口，晨光勾勒轮廓，胸口蓝色指示灯缓慢脉动 |
| **角色出场** | 小暖（165cm护理机器人，白色哑光金属外壳） |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`小暖/01_门口站立`。小暖首次出场。晨光从背后照来，勾勒出白色哑光轮廓。胸口淡蓝色指示灯是唯一颜色。赵淑芬的床在前景（虚化）。小暖站姿笔直，面部光学传感器暗的。 |

**参考Prompt**

```
A 165cm humanoid care robot standing in bedroom doorway,
white matte metal shell, female-shaped but not human,
morning backlight creating white silhouette outline,
chest center: circular pale blue indicator light pulsing slowly,
top of head: white flexible cable hanging like braid,
two dark optical sensors for eyes—not glowing,
standing perfectly straight, arms at sides,
bedroom interior in foreground blurred—bed with quilt, nightstand,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
white and pale blue dominant, 淡花青 for indicator,
clean geometric lines, no human softness,
morning dust particles in light beam,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated,
anime, cartoon, illustration, 3D render,
human face, human skin, human expression, smiling,
glossy chrome, reflective metal, neon lights, LED strips, cyberpunk,
bright neon, saturated colors, Western oil painting, CGI look
```

---

## 场景2：客厅·视频通话

> **场景编号**：SC-12-02  
> **情绪基调**：抗拒、妥协、发现轨道的隐忧  
> **环境**：普通城市公寓客厅  
> **色调**：室内暖光+屏幕冷光

### SHOT-12-03

| 字段 | 内容 |
|------|------|
| **镜号** | 2.6 |
| **类型** | 中景（主观视角） |
| **情绪** | 静默的发现、系统的无处不在 |
| **核心主体/意象** | 天花板轨道——银白色细轨嵌在天花板边缘，沿走廊延伸，经过卧室、浴室 |
| **角色出场** | 无（纯环境） |
| **尺寸** | 1280×720 |
| **技术备注** | 赵淑芬的主观视角：抬头看天花板。细轨是"小暖不是独立个体"的证据。银白色金属轨道嵌在白色天花板边缘，不显眼但一旦被注意到就无法忽视。沿走廊延伸，在床头和马桶上方各有一个接口。冷硬的技术感与温馨的家居环境形成对比。 |

**参考Prompt**

```
Interior ceiling view of elderly apartment,
silver-white thin metal track embedded along ceiling edge,
track extending down hallway, turning toward bedroom and bathroom doors,
two interface ports visible—one above bed area, one above toilet area,
track is unobtrusive but once noticed, impossible to ignore,
white ceiling with track as cold metallic line against warm domestic space,
soft indoor ambient light,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm grey walls with cold silver track accent,
淡墨 for ceiling, 焦墨 for track shadows,
subtle tension between domestic warmth and technological surveillance,
1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry entire image, watermark, text, logo, oversaturated,
anime, cartoon, illustration, 3D render,
exposed wires, industrial conduit, broken ceiling, exposed beams,
bright neon, saturated colors, Western oil painting, CGI look
```

---

## 场景3：卧室·翻身

> **场景编号**：SC-12-03  
> **情绪基调**：抗拒→接受，身体的诚实  
> **环境**：卧室，赵淑芬在床上看书  
> **色调**：室内暖光，被子暖黄

### SHOT-12-04

| 字段 | 内容 |
|------|------|
| **镜号** | 3.8-3.11 |
| **类型** | 全景→特写 |
| **情绪** | 紧张→缓慢放松、"几乎不可察觉地放松" |
| **核心主体/意象** | 小暖机械臂托肩扶腰，赵淑芬肩膀从绷紧到缓慢放松 |
| **角色出场** | 赵淑芬、小暖 |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`赵淑芬/02_被推身` + `小暖/02_翻身动作`。核心双人镜头。小暖辫子接入床头轨道，机械臂伸出——一只手托肩，一只手扶腰。赵淑芬侧躺，肩膀起初绷紧（肩胛骨凸起），然后缓慢放松。灯光柔和，被子的暖黄与机械臂的冷白形成质感对比。 |

**参考Prompt**

```
A 72-year-old Chinese woman lying on side in bed,
wearing light blue pajamas, scapula protruding through thin fabric,
shoulders initially tense, then slowly relaxing,
white care robot beside bed, braid cable connected to wall track,
robot's mechanical arms extended—one supporting shoulder, one at waist,
movement stable and precise, black rubber joint seals visible,
pale grey silicone palm surfaces touching human skin,
woman's eyes closed, lips pressed then gradually softening,
warm quilt texture, soft indoor bedroom light,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm ochre quilt vs cool white robot shell,
焦墨 for tense muscle lines, soft wash for relaxation,
contrast between organic human and geometric machine,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn face,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated, plastic skin,
heavy makeup, beauty filter, anime, cartoon, illustration, 3D render,
smiling, cheerful, relaxed immediately, no tension,
bright neon, saturated colors, Western oil painting, CGI look
```

---

## 场景4：厨房/餐厅·喂饭

> **场景编号**：SC-12-04  
> **情绪基调**：尊严与现实的冲突  
> **环境**：餐桌，两个菜一碗米饭，红烧排骨冒着热气  
> **色调**：食物暖色+室内光

### SHOT-12-05

| 字段 | 内容 |
|------|------|
| **镜号** | 4.9-4.14 |
| **类型** | 特写→中景 |
| **情绪** | 手抖、肉掉桌上、沉默、被喂食时闭眼 |
| **核心主体/意象** | 赵淑芬手抖夹不住肉，汤汁溅出，小暖喂食，她张嘴闭眼 |
| **角色出场** | 赵淑芬、小暖（机械臂） |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`赵淑芬/01_床边`。核心冲突镜头。赵淑芬右手夹菜，手微抖但稳住——吃到一半，手开始抖，一块肉掉在桌上，汤汁溅出。她看着汤汁，没有说话。然后小暖舀一勺饭送到嘴边，她张嘴，闭上眼睛。重点：她的手抖、汤汁溅出的瞬间、闭眼的表情。 |

**参考Prompt**

```
A 72-year-old Chinese woman seated at dining table,
right hand holding chopsticks, trembling slightly,
a piece of braised pork falling from chopsticks onto table,
sauce splattering on table surface,
woman's expression: silent resignation, looking at spilled sauce,
then a white robotic arm extending spoon with rice toward her mouth,
woman opens mouth and closes eyes—accepting but not yielding,
warm indoor dining light, steam rising from dishes,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm ochre food tones contrasting with cool white robot arm,
focus on hand tremor and facial expression transition,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn face,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated, plastic skin,
heavy makeup, beauty filter, anime, cartoon, illustration, 3D render,
smiling, cheerful, happy eating, enthusiastic,
bright neon, saturated colors, Western oil painting, CGI look
```

---

## 场景5：客厅·擦身

> **场景编号**：SC-12-05  
> **情绪基调**：脆弱、身体记忆的唤醒  
> **环境**：客厅，傍晚，只开台灯，昏黄  
> **色调**：昏黄台灯+冷白机械臂

### SHOT-12-06

| 字段 | 内容 |
|------|------|
| **镜号** | 5.13-5.15 |
| **类型** | 特写→近景 |
| **情绪** | 温毛巾接触、机械臂绕过肩胛、眉头慢慢松开 |
| **核心主体/意象** | 温毛巾接触松弛皮肤，白色机械臂从后颈到腰际，赵淑芬闭眼眉头松开 |
| **角色出场** | 赵淑芬（背部）、小暖（机械臂） |
| **尺寸** | 1280×720 |
| **技术备注** | 核心温情镜头。赵淑芬背对镜头，露出后背——肩胛骨突出，皮肤松弛。小暖的白色机械臂拿着温毛巾，从后颈开始，向下绕过肩胛骨直到腰际。水珠、松弛的皮肤、白色机械臂三者同框。然后切到赵淑芬的脸——闭着眼，眉头的皱纹慢慢松开。台灯昏黄，与机械臂的冷白形成对比。 |

**参考Prompt**

```
Close-up of an elderly Chinese woman's bare back,
scapula protruding, skin loose and translucent,
white robotic arm holding warm damp towel,
wiping from back of neck down around scapula to waist,
water droplets on skin surface,
soft warm lamplight from side,
then close-up of woman's face—eyes closed, eyebrow wrinkles slowly releasing,
expression: remembering something distant, almost peaceful,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm amber lamp light vs cool white robot arm,
焦墨 for skin texture and wrinkles, soft wash for relaxation,
intimate but not invasive, dignified vulnerability,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated,
anime, cartoon, illustration, 3D render,
bright lighting, cold clinical atmosphere, hospital setting,
young body, perfect skin, muscular back,
bright neon, saturated colors, Western oil painting, CGI look
```

---

## 场景6：客厅·视频通话

> **场景编号**：SC-12-06  
> **情绪基调**：清醒的认知、"它是不是人？不是。"  
> **环境**：客厅，白天  
> **色调**：自然光+屏幕光

### SHOT-12-07

| 字段 | 内容 |
|------|------|
| **镜号** | 6.10-6.11 |
| **类型** | 近景 |
| **情绪** | 平静但坚定、女儿的沉默 |
| **核心主体/意象** | 赵淑芬说出"它是不是人？不是。它有没有感情？没有。"然后看向小暖方向 |
| **角色出场** | 赵淑芬 |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`赵淑芬/01_床边`。核心对白镜头。赵淑芬拿着手机，表情平静但坚定。说出"它是不是人？不是"时的眼神是清醒的——不是被欺骗，是主动选择。然后她看向厨房方向（小暖的背影在背景中虚化）。光线是自然窗光。 |

**参考Prompt**

```
A 72-year-old Chinese woman, retired teacher,
holding smartphone, looking slightly off-camera toward kitchen direction,
expression: calm, resolute, clear-eyed—she knows exactly what she's saying,
brown-red plastic reading glasses on nose,
grey-white short hair, pale yellowish complexion,
light grey cotton top,
kitchen area visible in background blurred—white robot figure washing dishes,
natural daylight from window,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm grey and soft natural light,
淡墨 for subtle facial shadows,
expression of active choice, not delusion,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn face,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated, plastic skin,
heavy makeup, beauty filter, anime, cartoon, illustration, 3D render,
angry, shouting, crying, emotional breakdown,
confused, delusional, dreamy, romantic,
bright neon, saturated colors, Western oil painting, CGI look
```

---

## 场景7：浴室·摔倒与救援

> **场景编号**：SC-12-07  
> **情绪基调**：紧张→控制、90秒的精确、"你受伤了"  
> **环境**：浴室，深夜，地砖有水迹  
> **色调**：冷白浴室光+指示灯绿光

### SHOT-12-08

| 字段 | 内容 |
|------|------|
| **镜号** | 7.5 |
| **类型** | 全景 |
| **情绪** | 高速进入、紧急、3秒的精确 |
| **核心主体/意象** | 小暖高速进入画面，辫子在空中划弧，无声滑入天花板轨道接口，指示灯从蓝变绿 |
| **角色出场** | 小暖、赵淑芬（趴在地上） |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`小暖/02_翻身动作`。全片动作高潮。小暖从画面外高速进入，头顶辫子在空中划出弧线，无声滑入浴室天花板轨道接口。胸口指示灯从蓝色变为绿色（快速闪烁后稳定）。赵淑芬趴在地上，表情痛苦。浴室地砖有水迹，灯光白亮冷硬。动作要体现"精确"而非"慌乱"。 |

**参考Prompt**

```
A white care robot in high-speed emergency entry,
braid cable arcing through air, sliding into ceiling track interface,
chest indicator light changing from blue to green—fast flash then steady,
robot positioned over elderly woman lying on wet bathroom floor,
woman: 72 years old, grey-white hair, expression of pain,
white tiled bathroom, water stains on floor,
bright cold bathroom lighting,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
cool white and green dominant, 淡花青 for blue, 石绿 for green indicator,
geometric precision of robot movement,
tension between still human and active machine,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated,
anime, cartoon, illustration, 3D render,
human rescuer, paramedic, doctor, nurse,
glossy chrome, neon lights, cyberpunk,
chaotic, blurry motion, falling apart,
bright neon, saturated colors, Western oil painting, CGI look
```

---

### SHOT-12-09

| 字段 | 内容 |
|------|------|
| **镜号** | 7.14-7.16 |
| **类型** | 特写→中景 |
| **情绪** | 90秒的精确、呼吸平缓、指节发白但不晃动 |
| **核心主体/意象** | 进度数字跳动，赵淑芬的手抓住机械臂——指节发白，小暖没有晃动 |
| **角色出场** | 赵淑芬（手部+脸）、小暖（机械臂+界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 双焦点镜头。特写：小暖界面上的进度数字（"00:32"→"00:33"→"01:12"→"01:13"）。中景：赵淑芬的手本能地抓住小暖的机械臂——指节发白，但小暖没有晃动。她的呼吸从急促到平缓。界面数字用后期合成，T2I生成界面光感和机械臂质感即可。 |

**参考Prompt**

```
Close-up of white robotic arm being gripped by elderly human hand,
human hand: knuckles white from tight grip, age spots, trembling slightly,
robot arm: stable, no vibration, matte white metal,
in background: robot interface display with progress numbers glowing faintly,
elderly woman's face partially visible—breathing slowing down,
bathroom setting, cold white light,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
cool white dominant, 焦墨 for hand tension,
contrast between organic grip strength and inorganic stability,
extreme focus on hand-arm contact point,
1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn hand,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry entire image, watermark, text, logo, oversaturated,
anime, cartoon, illustration, 3D render,
young hand, smooth skin, perfect grip, no tension,
bright warm lighting, sunny, outdoor,
bright neon, saturated colors, Western oil painting, CGI look
```

---

### SHOT-12-10

| 字段 | 内容 |
|------|------|
| **镜号** | 7.25 |
| **类型** | 特写 |
| **情绪** | "你受伤了"——关心一个不会痛的机器 |
| **核心主体/意象** | 赵淑芬用手指擦小暖外壳上的血迹。擦不掉，干了一半凝在上面 |
| **角色出场** | 赵淑芬（手）、小暖（外壳局部） |
| **尺寸** | 1280×720 |
| **技术备注** | 核心情感镜头。赵淑芬的手指（老年斑、皱纹）在小暖的白色哑光外壳上擦拭——试图擦掉血迹但擦不掉。血迹是暗红褐色，干了一半，凝在金属表面。小暖的指示灯在背景中正常脉动。这个动作是"她把小暖当人关心"的第一证据。 |

**参考Prompt**

```
Extreme close-up of elderly Chinese woman's fingers touching white matte metal surface,
fingers: age spots, wrinkles, short nails—wiping at a stain,
dark red-brown dried blood stain on white metal shell—partially smeared, not removable,
woman's fingers moving back and forth trying to wipe it clean,
faint pale blue indicator light pulsing in background,
bathroom ambient light, slightly humid atmosphere,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
white shell with dark red-brown stain, pale blue accent,
extreme focus on fingers and stain interaction,
touching something that cannot feel but bears marks,
1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn hand,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry entire image, watermark, text, logo, oversaturated,
anime, cartoon, illustration, 3D render,
young hand, smooth skin, perfect nails,
bright neon, saturated colors, Western oil painting, CGI look,
wet fresh blood, gore, horror, violent
```

---

## 场景8：客厅·尾声

> **场景编号**：SC-12-08  
> **情绪基调**：信任、不确定但选择相信、"我决定当它有"  
> **环境**：客厅，一个月后，窗外梧桐叶黄了  
> **色调**：暖金+冷白，秋日的平和

### SHOT-12-11

| 字段 | 内容 |
|------|------|
| **镜号** | 8.12 |
| **类型** | 特写→主观视角 |
| **情绪** | 沉默的对话、"我决定当它有" |
| **核心主体/意象** | 赵淑芬的手搭在小暖机械臂上。手是旧的，机械臂是新的（有擦不掉的旧血迹）。窗外梧桐叶黄，风声 |
| **角色出场** | 赵淑芬（手+侧脸）、小暖（机械臂） |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`赵淑芬/03_手搭机械臂` + `小暖/03_带血迹`。全片结尾核心画面。赵淑芬的手（老年斑、皱纹、不握紧）搭在小暖的白色哑光机械臂上。机械臂上有擦不掉的旧血迹痕迹。窗外梧桐树叶黄了，暖金色光线。她的手没有离开，就一直搭在那里。这是全书对"信任"最简洁的视觉定义。 |

**参考Prompt**

```
Close-up of elderly Chinese woman's hand resting on white matte robotic arm,
hand: covered with age spots and wrinkles, fingers not gripping—just resting,
robot arm: matte white metal with faint dried blood stain痕迹,
warm golden afternoon light from window,
yellowed pagoda tree leaves visible outside window,
woman's face partially visible—expression: complex serenity,
not smiling but accepting, "I decide it matters",
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm gold and soft grey, 焦墨 for hand wrinkles, 淡赭 for age spots,
contrast between organic aged skin and inorganic smooth metal,
window light creating rim glow on both hand and arm,
bittersweet quiet acceptance,
1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated,
anime, cartoon, illustration, 3D render,
smiling, cheerful, triumphant, celebratory,
young hand, perfect skin, manicured nails,
bright neon, saturated colors everywhere, Western oil painting, CGI look,
cute grandma, cartoonish, caricature
```

---

## 角色定妆交叉引用

| 角色 | 定妆文件 | 本集使用镜头 | 备注 |
|------|----------|-------------|------|
| 赵淑芬 | `ASSETS/CHARACTERS/赵淑芬/定妆规格.md` | SHOT-12-01, 04, 05, 06, 07, 09, 10, 11 | 核心角色，3张定妆照全覆盖 |
| 小暖 | `ASSETS/CHARACTERS/小暖/定妆规格.md` | SHOT-12-02, 04, 08, 09, 10, 11 | 核心角色，3张定妆照全覆盖 |
| 女儿 | — | SHOT-12-07（手机中/提及） | 仅声音/提及，无需定妆 |

---

## 核心视觉符号落实

| 符号 | 出现镜头 | T2I落实方式 |
|------|----------|-------------|
| 左手放在左膝盖上 | SHOT-12-01 | 开场特写，关节炎的手 |
| 天花板轨道 | SHOT-12-03 | 主观视角，银白色细轨 |
| 机械臂翻身 | SHOT-12-04 | 双人镜头，肩膀从绷紧到放松 |
| 手抖夹不住肉 | SHOT-12-05 | 手部特写，汤汁溅出 |
| 温毛巾擦背 | SHOT-12-06 | 背部+面部特写，眉头松开 |
| 小暖背影洗碗 | SHOT-12-07 | 背景虚化中的白色机器人 |
| 辫子接入轨道+绿灯 | SHOT-12-08 | 动作镜头，指示灯变色 |
| 90秒进度数字 | SHOT-12-09 | 界面光感+手部抓握 |
| 外壳上的血迹 | SHOT-12-10 | 手指擦拭血迹特写 |
| 手搭机械臂（结尾） | SHOT-12-11 | 全片结尾核心画面 |
| 窗外梧桐叶黄 | SHOT-12-11 | 背景环境，秋日暖金 |

---

## 生成记录

| 日期 | 镜头 | 生成工具 | 输出文件 | 结果 |
|------|------|----------|----------|------|
| | | | | ⏳ 待生成 |