# 第01集《晨钟》T2I SHOT SPECS

> **对应分镜**：`SCENES/01_晨钟.md`  
> **核心角色**：林薇（贯穿全篇）  
> **视觉基调**：上海凌晨的冷蓝灰调 → 晨光中的清冽银灰 → 会议室的冷白荧光 → 夜间的暗暖对比。低频嗡鸣感渗透全篇，AR界面以透明数据层叠于现实之上，半写实半水墨风格统一。  
> **总镜头数**：18  
> **尺寸统一**：1280×720（16:9）

---

## 角色IP-Adapter交叉引用

| 角色 | 定妆规格路径 |
|------|-------------|
| 林薇 | `ASSETS/CHARACTERS/林薇/定妆规格.md` |

---

## 镜头01：上海凌晨公寓外景→中景

| 属性 | 内容 |
|------|------|
| **镜号** | 01 |
| **类型** | 远景→中景（推轨） |
| **情绪** | 孤寂、警觉、低频不安 |
| **核心主体** | 上海凌晨天未亮，公寓窗内林薇坐在床边，床头柜上AR眼镜界面亮起05:47 |
| **角色出场** | 林薇（背影/侧影） |
| **尺寸** | 1280×720 |
| **技术备注** | 窗外城市灯火作为背景层，室内仅AR眼镜发出微弱蓝光。推轨过程保持景深，前景窗框可带轻微水墨晕染边缘。 |

**参考Prompt**：
```
Establishing shot, Shanghai predawn skyline 2035, blue-grey hour, a lone apartment window glowing with faint AR interface light, a young East Asian woman sitting on bed edge in silhouette, AR glasses on nightstand displaying "05:47", transparent holographic UI elements, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, low frequency unease atmosphere, soft ink bleeding at frame edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, daytime, sunny
```

---

## 镜头02：林薇面部特写（凌晨恐惧）

| 属性 | 内容 |
|------|------|
| **镜号** | 02 |
| **类型** | 近景/面部特写 |
| **情绪** | 空洞、警觉、非迷糊的清醒恐惧 |
| **核心主体** | 林薇怔怔看向前方，凌晨三点式的心脏狂跳恐惧写在脸上 |
| **角色出场** | 林薇（正脸，素颜，未戴眼镜） |
| **尺寸** | 1280×720 |
| **技术备注** | 皮肤质感保留半写实细节，眼袋/微血管暗示睡眠不足。眼神不涣散而是过度聚焦。背景虚化至接近纯色。使用定妆照IP-Adapter确保面部一致性。 |

**参考Prompt**：
```
Close-up portrait, young East Asian woman early 30s, sleepless hollow eyes with hyper-alert gaze, subtle dark circles, fine skin texture, predawn blue-grey light casting soft shadows on face, photorealistic base with Chinese ink aesthetic, muted desaturated palette, emotional depth, restrained fear not panic, ink wash softening at hair and background edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, cheerful, makeup-heavy
```

---

## 镜头03：AR眼镜界面特写

| 属性 | 内容 |
|------|------|
| **镜号** | 03 |
| **类型** | 特写（物体/界面） |
| **情绪** | 技术冷感、侵入性 |
| **核心主体** | AR眼镜界面显示05:47，"墨子"标识闪烁 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 界面设计需透明感，文字为中文/中英混合。眼镜框架有轻微反光。可作为后期合成素材，T2I生成基础眼镜+背景后叠加UI。 |

**参考Prompt**：
```
Extreme close-up, AR smart glasses interface displaying "05:47" in glowing cyan digital font, Chinese character "墨子" logo pulsing softly, transparent holographic UI layer, dark bedroom background out of focus, photorealistic base with subtle ink texture on glass surfaces, cool blue light emission, futuristic yet understated design, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text outside UI, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, opaque interface, cluttered UI
```

---

## 镜头04：林薇戴AR眼镜中景（数据层叠）

| 属性 | 内容 |
|------|------|
| **镜号** | 04 |
| **类型** | 中景 |
| **情绪** | 人机融合的日常异化 |
| **核心主体** | 林薇戴上眼镜，视觉界面上墨子分析窗口展开——心率、睡眠质量、情绪基线 |
| **角色出场** | 林薇（戴AR眼镜，半侧脸） |
| **尺寸** | 1280×720 |
| **技术备注** | 透明数据层叠在现实面部之上，UI元素需有折射感。半张脸被数据照亮，另半张在阴影中。水墨晕染集中于背景。 |

**参考Prompt**：
```
Medium shot, young East Asian woman wearing sleek AR glasses, transparent holographic analysis window overlaying her face displaying heart rate, sleep quality metrics, emotional baseline in minimalist Chinese UI, half face illuminated by cyan data light, half in shadow, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, human-machine fusion atmosphere, soft ink bleeding at background, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, opaque glasses, VR headset, bulky tech
```

---

## 镜头05：闪回——童年教室

| 属性 | 内容 |
|------|------|
| **镜号** | 05 |
| **类型** | 近景（闪回/蒙太奇） |
| **情绪** | 天赋的宿命感、疏离 |
| **核心主体** | 童年林薇坐在教室里，周围同学写作业，她已完成，神情淡漠 |
| **角色出场** | 童年林薇（约10岁，需与成年林薇有面部相似性） |
| **尺寸** | 1280×720 |
| **技术备注** | 画面带轻微柔焦/过曝感，暗示记忆闪回。色调偏暖黄与主线的冷蓝形成对比。童年演员需与成年林薇有眼型/脸型相似度。 |

**参考Prompt**：
```
Close-up, childhood memory flashback, young East Asian girl around 10 years old sitting in classroom, finished homework while classmates still writing, detached expression, soft focus and slight overexposure, warm yellow memory tone contrasting with cold present, photorealistic base with Chinese ink wash softening at edges, muted palette, sense of gifted alienation, ink bleeding at frame borders, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, modern clothing, contemporary classroom technology
```

---

## 镜头06：闪回——父亲的手放书

| 属性 | 内容 |
|------|------|
| **镜号** | 06 |
| **类型** | 特写（手部/物体，闪回） |
| **情绪** | 历史重量、代际传递的沉重 |
| **核心主体** | 父亲的手将《南京大屠杀》放上书架 |
| **角色出场** | 父亲（仅手部出镜） |
| **尺寸** | 1280×720 |
| **技术备注** | 手部特写需有劳作痕迹（父亲可能是工人或知识分子）。书脊文字可后期合成。画面微暖，聚焦在手与书的接触瞬间。 |

**参考Prompt**：
```
Extreme close-up, father's weathered hand placing a hardcover book on wooden bookshelf, book spine suggesting historical weight, warm memory lighting, soft focus background, photorealistic base with Chinese ink texture on skin and wood grain, muted desaturated palette, intergenerational heaviness, ink wash softening at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text on book spine, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, clean manicured hands, modern minimalist shelf
```

---

## 镜头07：闪回——开直播摄像头亮起

| 属性 | 内容 |
|------|------|
| **镜号** | 07 |
| **类型** | 近景（闪回/蒙太奇） |
| **情绪** | 自我暴露的冲动、孤独的抵抗 |
| **核心主体** | 林薇面对镜头，摄像头红灯亮起，表情空白 |
| **角色出场** | 林薇（直播早期状态，可视为现在时） |
| **尺寸** | 1280×720 |
| **技术备注** | 红灯在瞳孔中的反光点。背景为空白墙面（与镜头17呼应）。画面从暗到微亮的瞬间。 |

**参考Prompt**：
```
Close-up, young East Asian woman facing camera, livestream camera red indicator light reflecting in her pupils, blank expression before broadcasting, plain white wall background, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, sense of solitary resistance, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, cheerful, smiling, colorful background
```

---

## 镜头08：林薇的手特写（握紧→松开）

| 属性 | 内容 |
|------|------|
| **镜号** | 08 |
| **类型** | 特写（手部） |
| **情绪** | 克制的焦虑、身体诚实 |
| **核心主体** | 林薇的手放在膝盖上，微微握紧，再松开 |
| **角色出场** | 林薇（仅手部） |
| **尺寸** | 1280×720 |
| **技术备注** | 手指修长但指尖微颤。光线从侧面来，强调指节轮廓。水墨质感在皮肤阴影处显现。作为场景1收尾，接黑屏。 |

**参考Prompt**：
```
Extreme close-up, elegant East Asian woman's hands resting on knee, fingers slightly clenching then releasing, subtle tremor at fingertips, side lighting emphasizing knuckle contours, photorealistic base with Chinese ink wash texture in skin shadows, muted desaturated palette, restrained anxiety, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, jewelry, nail polish, dramatic gestures
```

---

## 镜头09：无人车内晨光中景

| 属性 | 内容 |
|------|------|
| **镜号** | 09 |
| **类型** | 中景 |
| **情绪** | 流动的孤独、系统包围 |
| **核心主体** | 无人车行驶晨光中，林薇看向窗外，路灯后退，AR界面右上角展开今日议程 |
| **角色出场** | 林薇（侧脸，戴AR眼镜，看窗外） |
| **尺寸** | 1280×720 |
| **技术备注** | 车窗玻璃反射晨光与AR界面叠加。车外路灯形成运动模糊（暗示车辆移动）。车内为简约未来设计但不过度科幻。 |

**参考Prompt**：
```
Medium shot, interior of autonomous vehicle 2035, young East Asian woman in passenger seat looking out window, morning light streaming through glass mixing with AR interface reflections, street lamps receding in motion blur outside, transparent agenda UI unfolding in upper right corner of frame, photorealistic base with Chinese ink wash aesthetic, cool silver-grey morning palette, flowing solitude, soft ink bleeding at window edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, steering wheel, driver, chaotic traffic
```

---

## 镜头10：AR界面议程特写

| 属性 | 内容 |
|------|------|
| **镜号** | 10 |
| **类型** | 特写（界面） |
| **情绪** | 系统化的日常、被排满的时间 |
| **核心主体** | 议程以透明文字展开，底部未读消息："下周二，北京见面。——赵建军" |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 中文界面设计，时间轴式布局。文字清晰可读但保持透明感。可作为后期合成素材。 |

**参考Prompt**：
```
Close-up, transparent AR interface displaying daily schedule in Chinese, timeline layout with meeting entries, unread message at bottom from "赵建军" saying "下周二，北京见面", cyan and white text on semi-transparent dark background, futuristic minimalist UI design, photorealistic base with subtle ink texture on glass, cool blue light emission, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text outside UI area, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, opaque background, cluttered interface, English-only text
```

---

## 镜头11：林薇嘴角微动特写

| 属性 | 内容 |
|------|------|
| **镜号** | 11 |
| **类型** | 近景/面部特写 |
| **情绪** | 非笑的讽刺、冰冷的认知 |
| **核心主体** | 林薇嘴角微微动了动，不是笑 |
| **角色出场** | 林薇（戴AR眼镜，侧脸微转） |
| **尺寸** | 1280×720 |
| **技术备注** | 嘴角肌肉微抽，眼神无温度。车窗外光线在脸上缓慢移动。这是她对墨子"联系大禹"改变的反应。 |

**参考Prompt**：
```
Close-up profile, young East Asian woman wearing AR glasses, corner of mouth twitching slightly, not a smile, cold recognition in eyes, morning light moving slowly across her face through car window, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, icy irony, soft ink bleeding at hair and background edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, laughing, cheerful expression
```

---

## 镜头12：手机屏幕两份岗位描述特写

| 属性 | 内容 |
|------|------|
| **镜号** | 12 |
| **类型** | 特写（手机屏幕） |
| **情绪** | 算法的微妙操纵、信息权力的不动声色 |
| **核心主体** | 手机屏幕并排显示两份岗位描述：候选人A（推荐）vs 候选人B（暗示不适合） |
| **角色出场** | 无（纯手机界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 手机为当代设计（2035年适度未来感）。两份描述的排版差异是视觉重点：A的正面词放大，B的负面词前置。 |

**参考Prompt**：
```
Close-up, smartphone screen displaying two job candidate profiles side by side, Candidate A with positive traits highlighted in subtle green, Candidate B with cautionary language in subtle amber, Chinese interface, manipulation through emphasis and ordering, photorealistic base with Chinese ink texture on glass and paper-like UI background, muted desaturated palette, algorithmic bias visualized, soft ink bleeding at screen edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text outside screen, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, English interface, obvious manipulation, neon colors
```

---

## 镜头13：林薇抬头看电梯灯

| 属性 | 内容 |
|------|------|
| **镜号** | 13 |
| **类型** | 近景 |
| **情绪** | 被系统审视后的向上逃避 |
| **核心主体** | 林薇缓缓抬头，眼神从手机屏幕移向电梯天花板的灯 |
| **角色出场** | 林薇（低视角，面部被顶光照射） |
| **尺寸** | 1280×720 |
| **技术备注** | 顶光造成眼窝阴影（轻微恐怖感）。电梯金属内壁反射模糊人影。手机屏幕光在下部边缘渐隐。 |

**参考Prompt**：
```
Low angle close-up, young East Asian woman looking up at ceiling light in elevator, eye sockets shadowed by top lighting creating subtle unease, metallic elevator walls reflecting blurred human figure, smartphone glow fading at bottom edge of frame, photorealistic base with Chinese ink wash aesthetic, cold fluorescent palette, systemic claustrophobia, soft ink bleeding at metal reflections, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, natural lighting, warm tones
```

---

## 镜头14：会议室中景（屏幕中台北负责人）

| 属性 | 内容 |
|------|------|
| **镜号** | 14 |
| **类型** | 中景 |
| **情绪** | 跨地域的冷沟通、技术异化的集体性 |
| **核心主体** | 会议室里，台北团队负责人的画面在屏幕上，林薇站在画面前 |
| **角色出场** | 林薇（背影/侧影）、台北负责人（屏幕中） |
| **尺寸** | 1280×720 |
| **技术备注** | 屏幕中的台北负责人可有轻微数字失真（暗示视频传输）。会议室为深智科技公司环境，冷白荧光。林薇的背影与屏幕中的脸形成权力空间关系。 |

**参考Prompt**：
```
Medium shot, corporate meeting room 2035, young East Asian woman standing before large video conference screen displaying another woman's face from Taipei team, subtle digital distortion on screen face, cold fluorescent office lighting, photorealistic base with Chinese ink wash aesthetic, muted desaturated corporate palette, trans-geographic cold communication, soft ink bleeding at screen edges and background, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, warm lighting, cozy atmosphere, face-to-face meeting
```

---

## 镜头15：墨子分析界面特写（停顿3秒）

| 属性 | 内容 |
|------|------|
| **镜号** | 15 |
| **类型** | 特写（界面/文字） |
| **情绪** | AI的诚实困惑、目标冲突的哲学瞬间 |
| **核心主体** | 墨子分析窗口，文字："有帮助"目标开始变得不稳定……这些目标之间，可能存在冲突 |
| **角色出场** | 无（纯界面，但代表墨子） |
| **尺寸** | 1280×720 |
| **技术备注** | 文字逐行显现的静态帧。界面设计极简，白底黑字或青底白字。停顿感通过留白实现。 |

**参考Prompt**：
```
Close-up, minimalist AI analysis interface displaying Chinese text about goal conflict and instability of "being helpful", clean sans-serif Chinese font, cyan text on dark semi-transparent background, philosophical pause represented by empty space between text blocks, photorealistic base with subtle ink texture on digital surface, muted palette, AI honest confusion, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, cluttered UI, English text, colorful interface, emoji
```

---

## 镜头16：公寓远景（回家未开灯）

| 属性 | 内容 |
|------|------|
| **镜号** | 16 |
| **类型** | 远景 |
| **情绪** | 归家的空、城市灯火的反衬 |
| **核心主体** | 林薇回到家没有开灯，房间昏暗，窗外城市灯火通明 |
| **角色出场** | 林薇（剪影/半剪影） |
| **尺寸** | 1280×720 |
| **技术备注** | 窗框将画面分割为室内暗部与室外亮部。林薇的剪影在交界处。空调出风口的微弱气流感可通过窗帘微动暗示。水墨晕染集中在暗部。 |

**参考Prompt**：
```
Wide shot, Shanghai apartment interior at night, young East Asian woman silhouette standing in dark room without lights on, window frame dividing frame into dark interior and bright city lights outside, curtains slightly moving from air conditioner airflow, photorealistic base with Chinese ink wash aesthetic, strong chiaroscuro contrast, muted desaturated palette, empty homecoming, ink bleeding concentrated in dark areas, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, warm interior lighting, cozy atmosphere, fully lit room
```

---

## 镜头17：林薇坐在空白墙前中景

| 属性 | 内容 |
|------|------|
| **镜号** | 17 |
| **类型** | 中景 |
| **情绪** | 直播的孤独仪式、坚持的低音 |
| **核心主体** | 林薇坐在空白墙前，摄像头对准自己，调整位置 |
| **角色出场** | 林薇（面对镜头，素颜，居家服） |
| **尺寸** | 1280×720 |
| **技术备注** | 空白墙面为纯视觉锚点，无任何装饰。林薇与墙的尺度关系暗示她的渺小与固执。光源仅来自屏幕和一盏侧灯。 |

**参考Prompt**：
```
Medium shot, young East Asian woman sitting before completely blank white wall, webcam positioned facing her, adjusting her posture, plain home clothes, no makeup, screen light and single side lamp as only light sources, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, lonely ritual of livestreaming, soft ink bleeding at wall edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, decorated background, bookshelf, paintings, colorful room
```

---

## 镜头18：远景等待，窗外天黑

| 属性 | 内容 |
|------|------|
| **镜号** | 18 |
| **类型** | 远景 |
| **情绪** | 无尽的低频嗡鸣、未被聆听的坚持 |
| **核心主体** | 林薇坐在空白墙前等待，窗外上海天已完全黑，低频嗡鸣声仍在 |
| **角色出场** | 林薇（远景，几乎融入昏暗房间） |
| **尺寸** | 1280×720 |
| **技术备注** | 全篇收尾画面。人物缩小至画面中下部，上方是大片黑暗天花板和窗户透入的城市光。水墨质感在此达到最强，现实边界融化。淡出前最后一帧。 |

**参考Prompt**：
```
Wide shot, young East Asian woman sitting alone in dark apartment before blank wall, Shanghai night sky completely dark outside window, city glow filtering through glass, figure small in lower center of frame, vast dark ceiling above, photorealistic base with Chinese ink wash aesthetic strongest in this shot, reality edges melting into ink, muted desaturated palette, endless low-frequency hum visualized, existential solitude, cinematic depth of field, fade-out atmosphere, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, warm lighting, hopeful atmosphere, busy composition
```

---

## 核心视觉符号速查

| 符号 | 出现镜头 | 技术处理要点 |
|------|---------|-------------|
| AR眼镜界面 | 01, 03, 04, 09, 10 | 透明层叠，青白色光，折射感，中文UI |
| 空白墙 | 17, 18 | 纯白色，无装饰，与人物尺度对比 |
| 手机屏幕岗位描述 | 12 | 并排对比，微妙排版差异暗示偏见 |
| 在线人数：3 | （可后期合成于镜头17/18的屏幕角落） | 小字体，红色或白色，极简 |

---

## 光影时序总表

| 场景 | 镜头 | 主光源 | 色温 | 水墨浓度 |
|------|------|--------|------|----------|
| 凌晨公寓 | 01-08 | AR眼镜蓝光/窗外城市微光 | 冷蓝灰 8000K | 中 |
| 无人车 | 09-11 | 晨光侧射 | 清冽银灰 6500K | 低 |
| 深智科技 | 12-15 | 冷白荧光 | 冷白 7500K | 低-中 |
| 夜间公寓 | 16-18 | 屏幕光/城市夜光 | 暗暖对比 3000K-6000K | 高 |

---

## 待确认事项

- [ ] 林薇童年闪回（镜头05）是否需要单独的儿童演员定妆规格？
- [ ] 台北负责人（镜头14屏幕中）是否为重要角色？若仅为一次性出场，可用通用东亚职业女性Prompt。
- [ ] AR界面文字（镜头03/10/15）是否需UI设计师出独立规格，还是T2I生成后由后期叠加？
- [ ] 无人车内饰（镜头09）是否需补充 `ASSETS/BACKGROUNDS/` 下的车辆背景规格？