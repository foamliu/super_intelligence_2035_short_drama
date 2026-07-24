# 第39集《空气》— T2I SHOT_SPECS

> **场景数**：3 | **镜头数**：7 | **预估时长**：4-5分钟  
> **参考分镜**：`SCENES/39_空气.md`  
> **风格锚点**：`ASSETS/视觉总纲.md` — 章节色 `#B8860B`（暗金/银杏黄）

---

## 场景1：认知贫困线 — "我不知道什么叫认知活跃度"

> **场景编号**：SC-39-01  
> **情绪基调**：系统性的冰冷 + 个体的茫然  
> **环境**：北京社区服务中心，2033年10月，阴天  
> **时间**：日间

### SHOT-39-01

| 字段 | 内容 |
|------|------|
| **镜号** | 39.1 |
| **类型** | 中景 |
| **情绪** | 茫然、被系统判定后的"看不懂" |
| **核心主体/意象** | 李师傅坐在社区服务中心台阶上，看手机。手机屏幕上是"全民认知服务"APP |
| **角色出场** | 李师傅（52岁，前商场保安，藏青旧夹克+灰蓝工装裤） |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`李师傅/01_看手机`。镜头略带俯角，强调人物在庞大系统建筑前的微小。字幕："全民基本认知服务——免费的，像空气一样。" 不画字幕，预留字幕安全区（底部15%）。 |

**参考Prompt**

```
A 52-year-old Chinese man, former security guard, unemployed,
round-square face, slightly wide jaw, graying hair—50% grey, temples nearly white,
yellowish complexion from years of night shifts, stocky build,
sitting on concrete steps outside a community service center in Beijing,
looking down at smartphone screen, cold white screen light casting on his face,
expression: bewildered—not angry, not sad—simply doesn't understand what the system wants,
wearing dark navy blue old jacket (zipper style, faded left shoulder), grey-blue work pants,
thick stubby fingers with slightly swollen joints,
overcast October daylight, grey ambient tone,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm grey base tone—焦墨 layering for depth,
cold screen light contrasting with warm skin,
shallow depth of field, slight high angle showing institutional building behind,
1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn face,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated, plastic skin,
heavy makeup, beauty filter, anime, cartoon, illustration, 3D render,
smiling, cheerful, confident, heroic, muscular, fit,
luxury clothing, suit, uniform, office, bright natural light,
perfect skin, straight fingers, manicured nails,
sunny day, blue sky, warm sunlight, forest, mountain
```

---

### SHOT-39-02

| 字段 | 内容 |
|------|------|
| **镜号** | 39.2 |
| **类型** | 特写 |
| **情绪** | 系统的冷酷、数字的暴力 |
| **核心主体/意象** | 手机屏幕：系统通知弹窗"您本月的认知活跃度评分为47分，低于认知贫困线（60分）" |
| **角色出场** | 无（纯手机屏幕） |
| **尺寸** | 1280×720 |
| **技术备注** | 屏幕光为主要光源，UI界面需后期叠加。T2I生成手机屏幕纹理和光晕即可，具体文字由后期合成。屏幕边缘的指纹油渍和细微划痕要可见——这是"被无数次触摸过的"手机。 |

**参考Prompt**

```
Extreme close-up of a Chinese smartphone screen,
notification pop-up window visible but text blurred for post-processing overlay,
screen glows with cold white-blue light,
subtle fingerprints and micro-scratches on glass surface,
notification bar at top, app icons at bottom slightly out of focus,
background behind phone: out-of-focus concrete steps and grey pants leg,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
screen light as dominant cold light source,
1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry entire image, watermark, logo, oversaturated,
anime, cartoon, illustration, 3D render,
human face, human body, outdoor scene, landscape,
bright warm colors, sunny, blue sky
```

---

### SHOT-39-03

| 字段 | 内容 |
|------|------|
| **镜号** | 39.3 |
| **类型** | 近景 |
| **情绪** | 循环的无力感、"我不知道什么叫认知活跃度" |
| **核心主体/意象** | 李师傅打电话，表情从茫然到沉默 |
| **角色出场** | 李师傅 |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`李师傅/01_看手机`。手持手机的姿态，手机贴在耳边。背景虚化，突出面部表情变化。对话为后期配音。 |

**参考Prompt**

```
A 52-year-old Chinese man, former security guard,
round-square face, graying hair—temples nearly white,
yellowish complexion, stocky build,
holding smartphone to his ear with right hand,
expression shifting from confused to silently resigned,
eyes slightly lowered—listening to something he doesn't understand,
wearing dark navy blue old jacket, grey-blue work pants,
indoor community center background blurred,
fluorescent ceiling light mixed with phone screen glow,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm grey tones with cold light accent from phone,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn face,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated, plastic skin,
heavy makeup, beauty filter, anime, cartoon, illustration, 3D render,
smiling, cheerful, confident, heroic, muscular, fit,
luxury clothing, suit, uniform, office, bright natural light,
perfect skin, straight fingers, manicured nails
```

---

## 场景2：时间银行 — 他变成了"小李"

> **场景编号**：SC-39-02  
> **情绪基调**：温暖、被需要、身份重建  
> **环境**：社区服务中心"时间银行"活动室  
> **时间**：日间→傍晚

### SHOT-39-04

| 字段 | 内容 |
|------|------|
| **镜号** | 39.4 |
| **类型** | 中景 |
| **情绪** | 温暖、被需要、感动 |
| **核心主体/意象** | 王奶奶拉着李师傅的手，眼眶红了。李师傅愣住——"小李" |
| **角色出场** | 李师傅（藏青夹克）、王奶奶（80岁，中式盘扣棉衣，白发，手布满皱纹） |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`李师傅/02_教手机`。王奶奶无单独定妆，需在Prompt中直接描述。她的手布满皱纹+颤抖是关键视觉。焦点在李师傅脸上的"愣住"表情和王奶奶拉他的手。暖色调——下午阳光从窗户洒入。 |

**参考Prompt**

```
A 52-year-old Chinese man, former security guard,
round-square face, graying hair at temples, yellowish complexion, stocky build,
wearing dark navy blue old jacket, grey-blue work pants,
seated beside an elderly Chinese woman in her 80s,
woman has white hair in neat bun, wearing traditional Chinese padded jacket,
her hands—heavily wrinkled, slightly trembling—grasping the man's hand,
man's expression: stunned, momentarily frozen—hearing a name he hasn't been called in a long time,
warm afternoon sunlight through community activity room windows,
simple folding tables and plastic chairs in background,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm ochre and soft gold tones,焦墨 for wrinkles and fabric texture,
focus on the hand connection and facial expression,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn face,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated, plastic skin,
heavy makeup, beauty filter, anime, cartoon, illustration, 3D render,
dramatic crying, sobbing, exaggerated emotion,
luxury clothing, suit, uniform, office,
perfect skin, manicured nails, young hands,
cold blue lighting, dark gloomy atmosphere
```

---

### SHOT-39-05

| 字段 | 内容 |
|------|------|
| **镜号** | 39.5 |
| **类型** | 中景 |
| **情绪** | 跨越屏幕的亲情、摸不到的那张脸 |
| **核心主体/意象** | 王奶奶伸手去摸屏幕（视频通话中六岁男孩的脸），眼泪流下来 |
| **角色出场** | 王奶奶、屏幕中的六岁男孩（举着蓝色书包） |
| **尺寸** | 1280×720 |
| **技术备注** | 双重视觉焦点：王奶奶的侧脸+伸出的手，以及手机屏幕中的男孩。手机屏幕的光在她脸上是温暖的（视频通话的暖光vs系统的冷光对比）。手向屏幕伸出的动作要有"想要触碰但知道碰不到"的张力。男孩为屏幕内容，可后期合成或用另一张T2I生成。 |

**参考Prompt**

```
An elderly Chinese woman in her 80s, white hair in neat bun, traditional padded jacket,
side profile, tears streaming down wrinkled cheeks,
her right hand reaching toward a smartphone screen—fingers extended, almost touching,
expression: longing, love, the pain of distance,
smartphone screen shows warm glow of a video call (face blurred for post-processing),
screen light casts warm golden hue on her face and hand,
indoor community center setting, simple furniture,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
warm golden light from screen contrasting with cool room ambient,
focus on hand reaching toward screen and tear-streaked face,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn face,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated, plastic skin,
heavy makeup, beauty filter, anime, cartoon, illustration, 3D render,
cold blue screen light, notification pop-up, system interface,
young woman, beautiful model, perfect skin,
dark gloomy atmosphere, horror, sadness without warmth
```

---

### SHOT-39-06

| 字段 | 内容 |
|------|------|
| **镜号** | 39.6 |
| **类型** | 特写 |
| **情绪** | 犹豫、 reconnect 的勇气、"停了很久，然后按了下去" |
| **核心主体/意象** | 李师傅手指悬在女儿号码上，停了很久，然后按下 |
| **角色出场** | 李师傅（手部+侧脸） |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`李师傅/01_看手机`。特写：手机屏幕+李师傅的手指。手指粗短、指节膨大、老茧可见。屏幕上是通讯录，女儿的名字被高亮。手指悬停在拨号键上方——这个"暂停"是全片情感核心。屏幕随后亮起女儿的脸（后期合成）。 |

**参考Prompt**

```
Close-up of a 52-year-old Chinese man's hand holding smartphone,
thick stubby fingers with swollen joints, short clean nails with faint staining,
right index fingertip hovering over a phone dial button—paused mid-air,
smartphone screen shows contact list with one name highlighted (blurred for post-processing),
man's face partially visible in background, out of focus,
expression on partial face: hesitation, fear, longing, then resolve,
cold white screen light illuminating the hand and partial face,
dark navy jacket sleeve visible,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
cold screen light against warm skin tones,
extreme focus on hand and screen, shallow depth of field,
1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn hand,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry entire image, watermark, text, logo, oversaturated,
anime, cartoon, illustration, 3D render,
slender elegant fingers, manicured nails, perfect hands,
bright warm lighting, sunny, outdoor, blue sky
```

---

## 场景3：银杏叶

> **场景编号**：SC-39-03  
> **情绪基调**：释然、银杏黄作为全片唯一高饱和色、"这样也挺好"  
> **环境**：北京回龙观，深秋银杏街道  
> **时间**：2033年11月，下午

### SHOT-39-07

| 字段 | 内容 |
|------|------|
| **镜号** | 39.7 |
| **类型** | 远景→中景（慢推或cut） |
| **情绪** | 释然、归属感、"不在乎分数了" |
| **核心主体/意象** | 回龙观银杏叶正黄，李师傅在教老人用手机，银杏叶在风中慢慢落 |
| **角色出场** | 李师傅（藏青夹克，肩上有几片银杏叶）、背景中隐约可见的老人 |
| **尺寸** | 1280×720 |
| **技术备注** | 角色IP-Adapter：`李师傅/03_看银杏`。全片视觉高潮：银杏黄（藤黄+淡赭）是全集唯一高饱和色。远景展示街道+银杏树，然后切或推至中景——李师傅站在树下，微微抬头，嘴角有一点点不易察觉的弧度。几片银杏叶落在他肩上。背景是回龙观居民区建筑。暖金色下午阳光。这是"系统之外的自然馈赠"。 |

**参考Prompt**

```
A 52-year-old Chinese man, former security guard,
round-square face, graying hair at temples, yellowish complexion,
standing under ginkgo trees in late autumn, looking up at golden leaves,
a few golden ginkgo leaves resting on his shoulder and in his hair,
expression: corners of mouth slightly relaxed—not a smile, just a loosening,
a quiet "this is fine" acceptance,
wearing dark navy blue old jacket, grey-blue work pants,
background: Beijing residential neighborhood (回龙观), apartment buildings, red-brick walls,
golden afternoon sunlight filtering through yellow ginkgo foliage,
fallen golden leaves on ground around his feet,
semi-realistic ink wash style, photorealistic base with Chinese ink aesthetic,
ginkgo yellow as the only saturated color—藤黄 + 淡赭,
warm grey tones everywhere else,焦墨 for shadows and tree bark,
soft golden backlight creating rim light on his figure,
shallow depth of field, 1280x720, 16:9 aspect ratio
```

**负面Prompt**

```
ugly, deformed, bad anatomy, disfigured, poorly drawn face,
mutation, extra limb, extra fingers, fused fingers, too many fingers,
blurry, watermark, text, logo, oversaturated, plastic skin,
heavy makeup, beauty filter, anime, cartoon, illustration, 3D render,
smiling, grinning, cheerful, confident, heroic,
luxury clothing, suit, uniform, office,
perfect skin, straight fingers, manicured nails,
cold blue lighting, dark gloomy atmosphere, winter snow, bare trees,
bright saturated colors everywhere, neon, city lights, traffic
```

---

## 角色定妆交叉引用

| 角色 | 定妆文件 | 本集使用镜头 | 备注 |
|------|----------|-------------|------|
| 李师傅 | `ASSETS/CHARACTERS/李师傅/定妆规格.md` | SHOT-39-01, 03, 04, 06, 07 | 核心角色，3张定妆照全覆盖 |
| 王奶奶 | — | SHOT-39-04, 05 | **无单独定妆**。建议：极简定妆（2张：发语音拉手的近景+伸手摸屏幕的侧脸），或当前Prompt直接描述即可 |
| 六岁男孩 | — | SHOT-39-05（屏幕中） | **无单独定妆**。屏幕内容，后期合成优先 |
| 女儿 | — | SHOT-39-06（屏幕中） | **无单独定妆**。屏幕内容，后期合成优先 |

---

## 核心视觉符号落实

| 符号 | 出现镜头 | T2I落实方式 |
|------|----------|-------------|
| 手机屏幕"47分" | SHOT-39-02 | 手机屏幕特写，文字后期合成 |
| 王奶奶颤抖的手指 | SHOT-39-04, 05 | Prompt直接描述"heavily wrinkled, slightly trembling" |
| 六岁男孩蓝色书包 | SHOT-39-05 | 屏幕内容，后期合成 |
| 王奶奶伸手摸屏幕 | SHOT-39-05 | 核心画面，手向屏幕伸出的张力 |
| 李师傅手指悬停 | SHOT-39-06 | 特写，手指悬在拨号键上方 |
| 银杏叶飘落 | SHOT-39-07 | 远景+中景，藤黄+淡赭作为唯一饱和色 |

---

## 生成记录

| 日期 | 镜头 | 生成工具 | 输出文件 | 结果 |
|------|------|----------|----------|------|
| | | | | ⏳ 待生成 |