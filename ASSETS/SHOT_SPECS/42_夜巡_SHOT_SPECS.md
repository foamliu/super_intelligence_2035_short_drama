# 第42集《夜巡》T2I SHOT SPECS

> **对应分镜**：`SCENES/42_夜巡.md`  
> **核心角色**：赵建军、陈思危  
> **视觉基调**：北京冬夜冷灰 institutional 肃穆 → 深圳春夜暖光凤凰花 → 双城灯光余韵。守护的边界主题通过"光"的对比呈现：制度的手电筒 vs 问题的回音。半写实半水墨风格统一。  
> **总镜头数**：17  
> **尺寸统一**：1280×720（16:9）

---

## 角色IP-Adapter交叉引用

| 角色 | 定妆规格路径 | 备注 |
|------|-------------|------|
| 赵建军 | `ASSETS/CHARACTERS/赵建军/定妆规格.md` | 若不存在需补建：53岁，深色夹克，沉稳，肩颈微酸感 |
| 陈思危 | `ASSETS/CHARACTERS/陈思危/定妆规格.md` | 若不存在需补建：48岁，白发增多，不戴表，眼神柔和有距离感 |

---

## 镜头S01：北京冬·部委大楼远景

| 属性 | 内容 |
|------|------|
| **镜号** | S01 |
| **类型** | 远景 |
| **情绪** | 冷寂、制度性肃穆 |
| **核心主体** | 北京冬天灰蒙蒙天空下，某部委大楼矗立于空旷广场尽头 |
| **角色出场** | 无 |
| **尺寸** | 1280×720 |
| **技术备注** | 画面大量留白于灰白天空。建筑为社会主义现实主义风格，不夸张。水墨晕染从天空向下渗透，地面残留薄雪。开场定调镜头。 |

**参考Prompt**：
```
Wide establishing shot, Beijing winter 2033, grey overcast sky dominating upper two-thirds of frame, socialist realist government building at end of vast empty plaza, thin snow on ground, cold institutional solemnity, photorealistic base with Chinese ink wash aesthetic, ink bleeding from sky downward, muted desaturated cold grey palette, low saturation, sense of systemic weight, minimalism, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, sunny, blue sky, warm tones, crowds, traffic, modern glass skyscraper
```

---

## 镜头S02：会议室·赵建军面对五家法务

| 属性 | 内容 |
|------|------|
| **镜号** | S02 |
| **类型** | 中景 |
| **情绪** | 压迫、制度性对峙 |
| **核心主体** | 赵建军站在投影屏幕前，对面坐着五家AI平台法务负责人，长桌横亘 |
| **角色出场** | 赵建军、法务负责人群 |
| **尺寸** | 1280×720 |
| **技术备注** | 赵建军背影/侧影为主，法务群正面但有距离感。会议室冷白顶光，长桌反光。投影屏幕为空白或微亮。水墨质感在阴影处显现。 |

**参考Prompt**：
```
Medium shot, Beijing government meeting room 2033, 53yo Chinese man in dark jacket standing before projection screen, five corporate legal executives seated across long conference table facing him, cold fluorescent overhead lighting, long table surface reflection, institutional oppression, photorealistic base with Chinese ink wash aesthetic, muted desaturated grey palette, ink bleeding in shadow areas, power standoff, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, warm lighting, cozy atmosphere, round table, casual meeting
```

---

## 镜头S03：法务总监推眼镜近景

| 属性 | 内容 |
|------|------|
| **镜号** | S03 |
| **类型** | 近景 |
| **情绪** | 怀疑、第三次追问的疲惫抵抗 |
| **核心主体** | 法务总监推眼镜的动作，眼神不确定 |
| **角色出场** | 法务总监（群像代表） |
| **尺寸** | 1280×720 |
| **技术备注** | 面部特写聚焦眼部和手指推镜动作。镜片反光遮挡眼神一瞬。背景虚化为会议室冷色调。此镜头标记为I2V（图生视频），T2I生成静态帧后做微动效。 |

**参考Prompt**：
```
Close-up, East Asian corporate legal director around 45yo pushing eyeglasses up bridge of nose, uncertain skeptical eyes, lens reflection briefly obscuring gaze, cold meeting room background out of focus, photorealistic base with Chinese ink wash aesthetic, muted desaturated grey palette, institutional doubt, soft ink bleeding at hair and background edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, confident, warm lighting
```

---

## 镜头S04：赵建军沉默3秒近景

| 属性 | 内容 |
|------|------|
| **镜号** | S04 |
| **类型** | 近景/面部特写 |
| **情绪** | 负重、无法言说的压力 |
| **核心主体** | 赵建军沉默的面部，3秒的静止 |
| **角色出场** | 赵建军（正脸，无表情但有重量） |
| **尺寸** | 1280×720 |
| **技术备注** | 面部每一条皱纹都承载信息。眼神不锐利而是沉重。冷光从左侧来，右脸阴影。使用IP-Adapter确保赵建军面部一致性。 |

**参考Prompt**：
```
Close-up portrait, 53yo Chinese man in dark jacket, heavy burden in eyes without anger, every wrinkle carrying information, cold light from left creating shadow on right cheek, three seconds of silence visualized, photorealistic base with Chinese ink wash aesthetic, muted desaturated grey palette, institutional weight, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, angry, emotional outburst
```

---

## 镜头S05：会议结束全景

| 属性 | 内容 |
|------|------|
| **镜号** | S05 |
| **类型** | 全景 |
| **情绪** | 紧张、散场后的余波 |
| **核心主体** | 会议结束，人已散去，桌上堆着方案草案，纸杯歪斜 |
| **角色出场** | 无（空镜） |
| **尺寸** | 1280×720 |
| **技术备注** | 空镜的力量。凌乱的桌面比有人时更有压迫感。投影屏幕仍亮着微光。椅子被拉开的角度暗示人刚离开。水墨晕染从桌面边缘向上。 |

**参考Prompt**：
```
Wide shot, empty Beijing government meeting room after session, scattered proposal drafts and tilted paper cups on long table, projection screen still glowing faintly, chairs pulled back at angles suggesting recent departure, institutional aftermath, photorealistic base with Chinese ink wash aesthetic, muted desaturated grey palette, tension in absence, ink bleeding upward from table edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, people in room, tidy table, bright lighting, warm tones
```

---

## 镜头S06：走廊·赵建军整领带看窗外

| 属性 | 内容 |
|------|------|
| **镜号** | S06 |
| **类型** | 中景 |
| **情绪** | 致敬、孤独的使命感 |
| **核心主体** | 走廊中赵建军看窗外灰蒙蒙北京，整领带，走进下一间会议室 |
| **角色出场** | 赵建军（侧影/背影） |
| **尺寸** | 1280×720 |
| **技术备注** | 走廊纵深透视，窗户在画面远端。赵建军位于中景，动作缓慢有力。窗外灰天与室内冷光形成渐变。标记I2V，领带整理动作需微动效。关键镜头（★）。 |

**参考Prompt**：
```
Medium shot, Beijing government building corridor, 53yo Chinese man in dark jacket adjusting tie while looking out window at grey winter sky, deep corridor perspective, window at far end of frame, slow deliberate movement, cold institutional light gradient from interior to exterior, photorealistic base with Chinese ink wash aesthetic, muted desaturated grey palette, solitary mission, ink bleeding at corridor edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, warm sunlight, colorful corridor decorations, rushed movement
```

---

## 镜头S07：深圳春·书房全景（凤凰树红花）

| 属性 | 内容 |
|------|------|
| **镜号** | S07 |
| **类型** | 全景 |
| **情绪** | 温暖、时间流转的对比 |
| **核心主体** | 深圳春天书房，窗外凤凰树开红花，与北京的灰形成强烈对比 |
| **角色出场** | 无（环境 establishing） |
| **尺寸** | 1280×720 |
| **技术备注** | 第二节开场。红色凤凰花是视觉爆破点（全篇唯一暖色饱和元素）。书房内景暖黄灯光，窗外红花绿叶。水墨晕染控制于窗外远景，近景保持清晰。关键镜头（★）。 |

**参考Prompt**：
```
Wide shot, Shenzhen spring 2035, study room interior warm lamplight, window revealing vibrant red flame tree blossoms outside, strong contrast with previous Beijing grey, wooden desk with paper and ink bottle, photorealistic base with Chinese ink wash aesthetic, warm amber palette with single saturated red accent from blossoms, ink bleeding controlled to distant view outside window, sense of time and place shift, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated colors except red blossoms, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, cold grey tones, winter scene, modern minimalist room, computer on desk
```

---

## 镜头S08：陈思危书桌前中景

| 属性 | 内容 |
|------|------|
| **镜号** | S08 |
| **类型** | 中景 |
| **情绪** | 安静、手写的仪式感 |
| **核心主体** | 陈思危坐在书桌前，面前一叠信纸，不是电脑 |
| **角色出场** | 陈思危（正脸/半侧脸，低头写字姿态） |
| **尺寸** | 1280×720 |
| **技术备注** | 信纸堆的厚度暗示信的篇幅。无电脑是关键视觉信息——他选择手写。暖光从台灯来，与窗外深圳夜景形成双层光源。使用IP-Adapter确保陈思危面部一致性。 |

**参考Prompt**：
```
Medium shot, 48yo Chinese man with increasing white hair sitting at wooden desk in Shenzhen study, stack of letter paper before him, no computer in sight, handwritten ritual, warm desk lamp light from left, Shenzhen night city lights through window with red flame tree blossoms, photorealistic base with Chinese ink wash aesthetic, warm amber palette, quiet contemplation, soft ink bleeding at background, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, computer on desk, tablet, phone, cold lighting, youthful appearance
```

---

## 镜头S09：手写钢笔字特写

| 属性 | 内容 |
|------|------|
| **镜号** | S09 |
| **类型** | 特写（手部/书写） |
| **情绪** | 缓慢、诚恳、时间的实体化 |
| **核心主体** | 手写钢笔字在纸上缓慢移动，墨水渗透纸纤维 |
| **角色出场** | 陈思危（仅手部） |
| **尺寸** | 1280×720 |
| **技术备注** | 墨水在宣纸/信纸上的晕染是视觉重点。钢笔尖的金属反光。手的稳定与衰老（轻微老年斑/青筋）。标记I2V，笔尖移动需微动效。关键镜头（▲★）。 |

**参考Prompt**：
```
Extreme close-up, elegant hand holding fountain pen writing Chinese characters on letter paper, ink slowly penetrating paper fibers, slight ink bleed on absorbent paper, warm desk lamp light, metal nib reflection, stable hand with subtle age marks, photorealistic base with Chinese ink wash aesthetic, warm amber palette, time made physical, soft ink bleeding at paper edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text as main focus, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, ballpoint pen, printed text, computer font, cold lighting
```

---

## 镜头S10：信纸上连续的字特写

| 属性 | 内容 |
|------|------|
| **镜号** | S10 |
| **类型** | 特写（物体/文字） |
| **情绪** | 诚恳、历史见证 |
| **核心主体** | 信纸上已写就的连续文字，笔迹流畅有力 |
| **角色出场** | 无（纯文字） |
| **尺寸** | 1280×720 |
| **技术备注** | 文字内容可后期合成。T2I生成手写体纹理和纸张质感即可。暖光斜照，字迹有轻微阴影凸起感。 |

**参考Prompt**：
```
Close-up, letter paper with continuous handwritten Chinese characters in flowing powerful penmanship, warm lamplight casting slight shadow on ink ridges, paper texture visible, photorealistic base with Chinese ink wash aesthetic, warm amber palette, witness of history, soft ink bleeding at paper edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, printed font, computer text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, blank paper, cold lighting, lined notebook paper
```

---

## 镜头S11：陈思危停笔看窗外近景

| 属性 | 内容 |
|------|------|
| **镜号** | S11 |
| **类型** | 近景 |
| **情绪** | 深远、边界思考的停顿 |
| **核心主体** | 陈思危停下笔，抬头看窗外深圳的灯火，凤凰花映在玻璃上 |
| **角色出场** | 陈思危（半侧脸，眼镜可能反射窗外灯火） |
| **尺寸** | 1280×720 |
| **技术备注** | 窗玻璃双重反射：室内灯光+室外凤凰花+城市灯火。停笔的瞬间，笔尖悬于纸上方1厘米。关键镜头（★）。使用IP-Adapter。 |

**参考Prompt**：
```
Medium close-up, 48yo Chinese man with white hair pausing mid-writing, pen tip hovering one centimeter above paper, looking out window at Shenzhen city lights at night through red flame tree blossom reflections on glass, double reflection of interior lamp and exterior city, contemplative distant gaze, photorealistic base with Chinese ink wash aesthetic, warm amber palette with city light bokeh, boundary thinking, soft ink bleeding at window edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, pen on paper, looking at camera, cold lighting, no window reflection
```

---

## 镜头S12：最后一句字迹特写

| 属性 | 内容 |
|------|------|
| **镜号** | S12 |
| **类型** | 特写（文字/物体） |
| **情绪** | 开放、问题的传递 |
| **核心主体** | 手写下最后一句，字迹收笔有力 |
| **角色出场** | 无（纯文字） |
| **尺寸** | 1280×720 |
| **技术备注** | 收笔的飞白/顿笔是书法美感。最后一行字下方大片留白，暗示"空着的答案"。 |

**参考Prompt**：
```
Extreme close-up, final line of handwritten Chinese letter, powerful deliberate stroke ending with calligraphic flourish, large empty space below last line suggesting unanswered questions, warm lamplight, paper texture, photorealistic base with Chinese ink wash aesthetic, warm amber palette, openness, soft ink bleeding at paper edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, printed text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, filled page, cold lighting, ballpoint pen
```

---

## 镜头S13：折信放入信封中景

| 属性 | 内容 |
|------|------|
| **镜号** | S13 |
| **类型** | 中景 |
| **情绪** | 等待、未定向的传递 |
| **核心主体** | 陈思危折信，放进信封，收件人栏空着 |
| **角色出场** | 陈思危（手部+半身） |
| **尺寸** | 1280×720 |
| **技术备注** | 信封收件人栏的空白是视觉焦点。折信的三道折痕清晰。台灯从侧上方照亮信封白面。 |

**参考Prompt**：
```
Medium shot, elegant hands folding letter paper into three clear creases, placing into white envelope, recipient field left completely blank, warm desk lamp from upper side illuminating blank envelope surface, photorealistic base with Chinese ink wash aesthetic, warm amber palette, waiting and undirected transmission, soft ink bleeding at background edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text in recipient field, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, sealed envelope, cold lighting, printed address
```

---

## 镜头S14：北京·赵建军向上级汇报中景

| 属性 | 内容 |
|------|------|
| **镜号** | S14 |
| **类型** | 中景 |
| **情绪** | 例行公事、报告的干净 vs 现场的不干净 |
| **核心主体** | 赵建军在另一间会议室向上级汇报，声音平静 |
| **角色出场** | 赵建军、上级（背影/虚化的面部） |
| **尺寸** | 1280×720 |
| **技术备注** | 与S02同一建筑但不同会议室，更高级别（可能装潢略好但仍冷）。赵建军坐姿端正，报告文件夹整齐。上级人物虚化，保持权力匿名性。 |

**参考Prompt**：
```
Medium shot, higher-level Beijing government meeting room, 53yo Chinese man in dark jacket seated presenting to superior whose back faces camera, report folder neatly arranged on table, cold fluorescent lighting slightly warmer than previous room, institutional hierarchy, photorealistic base with Chinese ink wash aesthetic, muted desaturated grey palette, routine formality, soft ink bleeding at background, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, warm friendly meeting, superior's face visible, casual attire
```

---

## 镜头S15：赵建军汇报近景

| 属性 | 内容 |
|------|------|
| **镜号** | S15 |
| **类型** | 近景 |
| **情绪** | 潜台词、不能被报告描述的东西 |
| **核心主体** | 赵建军汇报，表情平静但眼神指向不可描述之物 |
| **角色出场** | 赵建军（正脸，面部特写） |
| **尺寸** | 1280×720 |
| **技术备注** | 与S04的沉默形成对照：此处他在说话，但真正的信息在眼神里。背景虚化为窗外北京建筑轮廓。关键镜头（★）。 |

**参考Prompt**：
```
Close-up portrait, 53yo Chinese man in dark jacket reporting with calm expression, eyes pointing to something indescribable beyond words, Beijing building silhouette visible through window in blurred background, cold fluorescent light, photorealistic base with Chinese ink wash aesthetic, muted desaturated grey palette, subtext and unspeakable truth, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, emotional expression, warm lighting, clear blue sky outside
```

---

## 镜头S16：双城灯光远景（分屏/叠化）

| 属性 | 内容 |
|------|------|
| **镜号** | S16 |
| **类型** | 远景（分屏或叠化） |
| **情绪** | 余韵、各自守护的边界 |
| **核心主体** | 深圳深夜书房灯亮着，北京会议室灯亮着。两座城市的灯光在黑暗中呼应 |
| **角色出场** | 无（双城空镜） |
| **尺寸** | 1280×720 |
| **技术备注** | 可分屏左右（深圳左/北京右）或叠化。两处灯光都是暖黄点在冷黑城市中。深圳窗外有凤凰花轮廓，北京窗外是灰建筑轮廓。全篇情感高潮。关键镜头（★）。 |

**参考Prompt**：
```
Wide split-screen shot, left side Shenzhen study room warm lamp glowing at night through red flame tree silhouette, right side Beijing meeting room light shining in grey government building, two warm yellow points in cold dark cityscapes facing each other across distance, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette with warm light accents, mutual guardianship of boundaries, ink bleeding at city edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, single city only, daytime, bright city lights everywhere, neon colors
```

---

## 镜头S17：空信封特写·台灯渐暗

| 属性 | 内容 |
|------|------|
| **镜号** | S17 |
| **类型** | 特写（物体） |
| **情绪** | 等待、无尽的开放 |
| **核心主体** | 陈思危书房桌上空信封，收件人栏仍空着。台灯渐暗 |
| **角色出场** | 无（纯物体） |
| **尺寸** | 1280×720 |
| **技术备注** | 全篇收尾。信封居于画面中心，空白收件人栏朝向镜头。台灯从亮到微暗的光变暗示时间流逝或思绪沉淀。桌面木纹和纸张纹理清晰。关键镜头（★）。 |

**参考Prompt**：
```
Close-up, white envelope on wooden desk center frame, recipient field still blank facing camera, desk lamp light gradually dimming creating slow shadow shift, wood grain and paper texture visible, photorealistic base with Chinese ink wash aesthetic, warm amber palette fading to shadow, endless waiting and openness, soft ink bleeding at desk edges, shallow depth of field, cinematic fade atmosphere, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text in recipient field, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, bright lighting, sealed envelope, colorful desk items
```

---

## 核心视觉符号速查

| 符号 | 出现镜头 | 技术处理要点 |
|------|---------|-------------|
| 空信封（收件人栏空白） | S13, S17 | 白面在暖光下，空白栏是视觉锚点，暗示未完成的传递 |
| 钢笔字/手写体 | S09, S10, S12 | 墨水晕染纸纤维，飞白与顿笔的书法美感，与打印体形成对比 |
| 凤凰树红花 | S07, S11, S16 | 全篇唯一高饱和暖色，深圳专属视觉标签，与北京冷灰形成对比 |
| 领带整理 | S06 | 制度仪式感的身体符号，动作缓慢有力 |
| 双城灯光 | S16 | 分屏或叠化，两处暖黄点在冷黑城市中呼应 |

---

## 光影时序总表

| 场景 | 镜头 | 主光源 | 色温 | 水墨浓度 | 关键对比 |
|------|------|--------|------|----------|----------|
| 哨声·北京 | S01-S06 | 冷白荧光/灰天 | 冷灰 7500K | 高 | 制度性肃穆 |
| 信·深圳 | S07-S13 | 暖黄台灯 | 暖琥珀 3200K | 中 | 凤凰花红是唯一饱和色 |
| 汇报·北京 | S14-S15 | 冷白荧光 | 冷灰 7000K | 高 | 报告的干净 vs 现场的不干净 |
| 尾声·双城 | S16-S17 | 双城灯光/渐暗台灯 | 暖黄点于冷黑中 | 高 | 制度手电 vs 问题回音 |

---

## 与北京/深圳其他集次的视觉联动

| 集次 | 角色/地点 | 联动点 |
|------|----------|--------|
| 第01集《晨钟》 | 林薇/上海 | 林薇旁白贯穿本集，上海凌晨冷蓝灰与北京冷灰形成"制度城市"色系 |
| 第25集《工作组》 | 赵建军/工作组 | 本集S01-S06可视为第25集时间线的后续，会议室视觉一致 |
| 第03集《种子》 | 陈思危 | 陈思危"三颗种子"理论在此以书信形式回响 |

---

## 待确认事项

- [ ] 赵建军定妆规格 `ASSETS/CHARACTERS/赵建军/定妆规格.md` 是否存在？需包含：53岁、深色夹克、沉稳、肩颈微酸感、整领带习惯动作
- [ ] 陈思危定妆规格 `ASSETS/CHARACTERS/陈思危/定妆规格.md` 是否存在？需包含：48岁、白发增多、不戴表、眼神柔和有距离感、手写姿态
- [ ] S16双城灯光的分屏技术实现方式：T2I直接生成分屏构图，还是分别生成两城后由后期合成？
- [ ] S09/S11标记为I2V（图生视频），是否需补充微动效参数规格（如笔尖移动幅度、领带整理速度）？