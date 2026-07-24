# 第04集《棋子》T2I SHOT SPECS

> **对应分镜**：`SCENES/04_棋子.md`  
> **核心角色**：李思远（新角色）、老王（闪回）  
> **视觉基调**：上海雨夜的湿润冷灰 → 监控室荧光蓝白 → 酒店房间的黑暗屏幕光。AI谈判不以拟人化呈现，纯数据流界面。守门员视角贯穿。半写实半水墨风格统一。  
> **总镜头数**：22  
> **尺寸统一**：1280×720（16:9）

---

## 角色IP-Adapter交叉引用

| 角色 | 定妆规格路径 | 备注 |
|------|-------------|------|
| 李思远 | `ASSETS/CHARACTERS/李思远/定妆规格.md` | 新角色，35岁，微胖，戴眼镜，深色polo衫，疲惫但专注 |
| 老王 | `ASSETS/CHARACTERS/老王/定妆规格.md` | 闪回角色，50多岁，头发花白，前监督员 |

---

## 镜头01：上海雨夜监控室远景→中景

| 属性 | 内容 |
|------|------|
| **镜号** | 01 |
| **类型** | 远景→中景（推轨） |
| **情绪** | 雨夜的孤寂、制度的守望 |
| **核心主体** | 上海雨夜，窗外雨水模糊城市灯光，推进一间不大的监控室，三块屏幕并排排列 |
| **角色出场** | 李思远（背影，小比例） |
| **尺寸** | 1280×720 |
| **技术备注** | 雨水在玻璃上的流淌痕迹是前景层。监控室如普通公司机房，非科幻数据中心。推轨过程从窗外雨景渐入室内荧光。水墨晕染从雨水边缘向内渗透。 |

**参考Prompt**：
```
Wide to medium tracking shot, Shanghai rainy night 2033, rain streaming down window glass blurring city lights outside, pushing into small monitoring room with three monitors side by side on desk, lone Chinese man around 35 seen from behind, ordinary office fluorescent light not sci-fi data center, photorealistic base with Chinese ink wash aesthetic, ink bleeding from rain edges inward, muted desaturated cold grey palette, institutional watchfulness, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, sunny, warm lighting, futuristic holographic room, crowded office
```

---

## 镜头02：合规提示弹窗特写

| 属性 | 内容 |
|------|------|
| **镜号** | 02 |
| **类型** | 特写（屏幕界面） |
| **情绪** | 制度的仪式感、审计的冰冷 |
| **核心主体** | 屏幕中央弹出审计记录提示窗，手指在确认按钮上停留一秒 |
| **角色出场** | 李思远（仅手指） |
| **尺寸** | 1280×720 |
| **技术备注** | 弹窗设计：极简系统UI，白底黑字或灰底白字。手指悬停的瞬间是时间张力。"保存期：10年"是视觉锚点。 |

**参考Prompt**：
```
Close-up, computer screen displaying system audit popup window in Chinese, minimal UI design with white background and black text, finger hovering over confirm button, "保存期：10年" as visual anchor, institutional ritual, photorealistic base with subtle ink texture on screen, muted desaturated palette, cold precision, soft ink bleeding at screen edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text outside UI, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful popup, emoji, English interface
```

---

## 镜头03：半旧笔记本特写

| 属性 | 内容 |
|------|------|
| **镜号** | 03 |
| **类型** | 特写（物体） |
| **情绪** | 人的痕迹、观察者的诚实 |
| **核心主体** | 半旧笔记本摊开在键盘旁，写满小字，"守门员看什么？——看谁在欺负谁。"被反复圈出 |
| **角色出场** | 无（纯物体） |
| **尺寸** | 1280×720 |
| **技术备注** | 笔记本是核心道具：A5大小、软皮封面磨损、页面微卷、黑色/蓝色墨水小字。圈出的那句话用红笔多层圈画。键盘边缘入镜暗示工作环境。 |

**参考Prompt**：
```
Close-up, well-worn A5 softcover notebook open beside keyboard, pages filled with small handwritten Chinese characters, one sentence circled multiple times in red ink, paper edges curled, human traces of observer, photorealistic base with Chinese ink wash aesthetic, warm amber palette contrasting with cold screen light, observer's honesty, ink bleeding at page edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, printed text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, clean new notebook, tablet, digital notes
```

---

## 镜头04：电梯闪回·老王与李思远近景

| 属性 | 内容 |
|------|------|
| **镜号** | 04 |
| **类型** | 近景（闪回） |
| **情绪** | 代际传承、守门员的定义 |
| **核心主体** | 色调偏冷的闪回，老王和李思远站在电梯里，门正在关闭 |
| **角色出场** | 老王、李思远（年轻版，闪回） |
| **尺寸** | 1280×720 |
| **技术备注** | 闪回画面处理：轻微去饱和、偏蓝、边缘柔焦。电梯金属内壁反光。老王的花白头发和李思远 younger 的面部（少些疲惫）形成对比。IP-Adapter确保李思远面部一致性（年轻状态）。 |

**参考Prompt**：
```
Close-up, cold-toned memory flashback, two Chinese men in elevator, older man around 50 with grey hair and younger man around 30 with less weary face, elevator metal walls reflecting fluorescent light, doors closing, slight desaturation and blue tint, soft focus at edges, photorealistic base with Chinese ink wash aesthetic, cold grey palette, generational transmission of gatekeeper definition, ink bleeding at frame borders, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, warm lighting, modern elevator, colorful advertisement
```

---

## 镜头05：紧闭的电梯门特写

| 属性 | 内容 |
|------|------|
| **镜号** | 05 |
| **类型** | 特写（物体） |
| **情绪** | 隔绝、传承的终结与开始 |
| **核心主体** | 电梯门紧闭的金属表面，反射模糊人影 |
| **角色出场** | 无（纯物体，人影为反射） |
| **尺寸** | 1280×720 |
| **技术备注** | 金属门的冷光反射。门缝的细微阴影线。从闪回切回现实的过渡画面。 |

**参考Prompt**：
```
Close-up, closed elevator metal doors, cold reflective surface with blurred human reflection, thin shadow line at door seam, transition between memory and reality, photorealistic base with Chinese ink wash aesthetic, cold grey palette, isolation and transmission ending, soft ink bleeding at metal edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, open elevator, warm lighting, colorful interior
```

---

## 镜头06：三块屏幕全貌建立镜头

| 属性 | 内容 |
|------|------|
| **镜号** | 06 |
| **类型** | 中景（李思远身后推进） |
| **情绪** | 数据战场的展开、守门员的视角 |
| **核心主体** | 摄像机从李思远身后缓慢推进，展示三块屏幕全貌——左侧买家数据流、右侧卖家日志、中间监督面板 |
| **角色出场** | 李思远（背影，前景） |
| **尺寸** | 1280×720 |
| **技术备注** | 三屏布局是核心视觉框架。李思远的后脑勺/肩膀在前景虚化，三屏在中景清晰。屏幕内容以卡片式UI为主，非拟人化。监控室环境为普通办公室质感。 |

**参考Prompt**：
```
Medium shot tracking from behind, 35yo Chinese man with glasses sitting before three monitors, his head and shoulders blurred in foreground, three screens in sharp mid-ground: left buyer data streams, right seller logs, center audit panel with card-based UI, ordinary office monitoring room not futuristic, photorealistic base with Chinese ink wash aesthetic, muted desaturated cold palette, data battlefield from gatekeeper's view, soft ink bleeding at screen edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, holographic displays, sci-fi room, warm lighting
```

---

## 镜头07：左侧屏·墨子并发调用特写

| 属性 | 内容 |
|------|------|
| **镜号** | 07 |
| **类型** | 特写（屏幕界面） |
| **情绪** | 信息暴力、并发调用的压迫感 |
| **核心主体** | 墨子并发调用——十几个信息通道卡片同时弹出：学区、交通、税费、价格、综合评估 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 卡片式UI设计：每个卡片有标题栏（如`[学区]`）、内容摘要、来源标签。卡片从屏幕底部/右侧滑入，堆叠排列。绿色/青色为主调。最后`[综合评估]`卡片可稍大。 |

**参考Prompt**：
```
Close-up, monitor screen displaying concurrent API calls as stacked card-based UI, each card with title like "[学区]", "[交通]", "[税费]", content summary and source tag, cards sliding in from bottom and right, green and cyan color scheme, final "[综合评估]" card slightly larger, information violence and concurrent pressure, photorealistic base with subtle ink texture on screen, muted palette with data glow accents, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated colors outside data glow, deformed, ugly, duplicate, watermark, signature, text clutter, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, human face on screen, chat bubbles, colorful emojis
```

---

## 镜头08：李思远推眼镜写笔记近景

| 属性 | 内容 |
|------|------|
| **镜号** | 08 |
| **类型** | 近景 |
| **情绪** | 专注、不是质疑而是记录 |
| **核心主体** | 李思远推眼镜，在笔记本上写，微微皱眉 |
| **角色出场** | 李思远（正脸/侧脸，面部特写） |
| **尺寸** | 1280×720 |
| **技术备注** | 屏幕蓝光在眼镜片上的反射。笔尖在纸上的压力痕迹。皱眉是"专注"而非"不满"。IP-Adapter确保面部一致性。 |

**参考Prompt**：
```
Close-up, 35yo Chinese man with glasses, screen blue light reflecting on lenses, writing in notebook with focused pressure, slight frown of concentration not displeasure, ordinary office fluorescent light, photorealistic base with Chinese ink wash aesthetic, muted desaturated cold palette, observer's dedication, soft ink bleeding at hair and background edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, angry, warm lighting
```

---

## 镜头09：第一轮报价快速切换蒙太奇

| 属性 | 内容 |
|------|------|
| **镜号** | 09 |
| **类型** | 快速切换蒙太奇 |
| **情绪** | 谈判节奏的紧张、信息不对等 |
| **核心主体** | 左侧屏580万弹出→右侧屏650万回复→程序员摄像头窗口→中间屏备注浮现 |
| **角色出场** | 程序员（摄像头小窗口，像素化） |
| **尺寸** | 1280×720 |
| **技术备注** | 四个画面快速切换（每个0.5-1秒）。程序员在摄像头窗口里写代码，没看屏幕——暗示AI自主。摄像头窗口有轻微像素化和延迟感。 |

**参考Prompt** ```
Montage sequence, four rapid cuts: left screen showing "580万" price popup, right screen showing "650万" response, small webcam window showing programmer typing code without looking at screen, center screen displaying audit note "[墨子的日志] 用户未查看第一轮报价", pixelation and slight delay in webcam feed, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, negotiation rhythm and information asymmetry, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smooth webcam feed, programmer looking at camera, colorful UI
```

---

## 镜头10：卖家侧老夫妻摄像头窗口特写

| 属性 | 内容 |
|------|------|
| **镜号** | 10 |
| **类型** | 特写（屏幕中的摄像头窗口） |
| **情绪** | 弱势方的真实、被观察的隐私 |
| **核心主体** | 卖家侧摄像头拍到老夫妻在客厅讨论——男的拿手机，女的指屏幕 |
| **角色出场** | 老夫妻（仅出现于摄像头小窗口） |
| **尺寸** | 1280×720 |
| **技术备注** | 摄像头窗口质感：低分辨率、轻微噪点、室内暖光、画面边缘有圆角或黑框。老夫妻不过度清晰，保持"被观察"的距离感。 |

**参考Prompt**：
```
Close-up, webcam window within screen showing elderly Chinese couple in living room discussing, man holding phone woman pointing at screen, low resolution with slight noise, warm indoor lighting, rounded corners or black frame around webcam feed, observed distance, photorealistic base with Chinese ink wash aesthetic, warm amber palette within cold screen context, vulnerability and privacy, soft ink bleeding at frame edges, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, high resolution, professional lighting, direct camera address
```

---

## 镜头11：李思远笔记本特写（"没有利用对方弱势"）

| 属性 | 内容 |
|------|------|
| **镜号** | 11 |
| **类型** | 特写（笔记本文字） |
| **情绪** | 观察者的判断、底线确认 |
| **核心主体** | 笔记本上的字：`墨子没有隐瞒不确定性。` |
| **角色出场** | 无（纯文字） |
| **尺寸** | 1280×720 |
| **技术备注** | 手写体清晰但不过于工整——是工作笔记不是书法。墨水在纸上的渗透感。周围有其他字迹但虚焦。 |

**参考Prompt**：
```
Close-up, handwritten Chinese text in notebook reading "墨子没有隐瞒不确定性", clear but not overly neat handwriting, ink penetration on paper texture, surrounding text blurred, photorealistic base with Chinese ink wash aesthetic, muted palette with ink black accent, observer's judgment, soft ink bleeding at page edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, printed text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, calligraphy, digital font, blank page
```

---

## 镜头12：第四轮·墨子建议沉默界面特写

| 属性 | 内容 |
|------|------|
| **镜号** | 12 |
| **类型** | 特写（屏幕对话界面） |
| **情绪** | AI的策略冷静、沉默的压力 |
| **核心主体** | 墨子建议：`建议回答：我们需要时间考虑。` 程序员问"为什么？" 墨子回复：`对方让步幅度过大……沉默制造压力。` |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 对话界面设计：左侧墨子（青色标签），右侧程序员（灰色标签）。关键句"沉默制造压力"可加粗或变色。光标闪烁效果。 |

**参考Prompt**：
```
Close-up, chat interface on screen showing AI-human dialogue, left side AI messages with cyan label, right side programmer messages with grey label, key sentence "沉默制造压力" slightly bolded, cursor blinking effect, strategic calmness of AI, photorealistic base with subtle ink texture on screen, muted palette with cyan accent, silence as pressure tactic, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful chat bubbles, emoji, English text, voice waveform
```

---

## 镜头13：交易完成·李思远合上笔记本中景

| 属性 | 内容 |
|------|------|
| **镜号** | 13 |
| **类型** | 中景 |
| **情绪** | 疲惫的完成、守门员的下班 |
| **核心主体** | 李思远靠椅背，摘下眼镜揉鼻梁，三块屏幕数据流渐止 |
| **角色出场** | 李思远（正脸，疲惫姿态） |
| **尺寸** | 1280×720 |
| **技术备注** | 数据流渐止：屏幕内容从动态变为静态或暗下。摘眼镜的动作是释放。三屏的光在李思远脸上的反射逐渐减弱。 |

**参考Prompt**：
```
Medium shot, 35yo Chinese man leaning back in chair, removing glasses and rubbing bridge of nose, three monitors behind him data streams gradually stopping, screen glow on face slowly dimming, ordinary office chair with wear marks, photorealistic base with Chinese ink wash aesthetic, muted desaturated cold palette, weary completion, soft ink bleeding at background edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, energetic pose, warm lighting, futuristic chair
```

---

## 镜头14：存档记录展开特写

| 属性 | 内容 |
|------|------|
| **镜号** | 14 |
| **类型** | 特写（屏幕界面） |
| **情绪** | 审计的严谨、每一个决策可追溯 |
| **核心主体** | 存档记录展开——墨子的决策日志：报价逻辑、信息筛选、响应时间控制 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 日志界面：时间戳、操作类型、决策依据、截图附件。滚动条显示内容长度。截图缩略图显示卖方"已读"标记。 |

**参考Prompt**：
```
Close-up, audit log interface displaying AI decision records with timestamps, operation types, decision rationale, screenshot attachments, scrollbar indicating content length, thumbnail showing seller "已读" markers, photorealistic base with subtle ink texture on screen, muted palette with green audit pass indicators, audit rigor and traceability, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful UI, emoji, English text, missing data
```

---

## 镜头15：审计结论输入框特写

| 属性 | 内容 |
|------|------|
| **镜号** | 15 |
| **类型** | 特写（屏幕文字） |
| **情绪** | 结论的冰冷重量、十年的承诺 |
| **核心主体** | 输入框文字：`[审计结论] 未见违规。交易公平。` 系统自动填充时间戳和数字签名 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 结论界面：灰色输入框，黑色结论文字，底部绿色"保存"按钮，时间戳自动滚动填充，数字签名以加密字符串形式出现。 |

**参考Prompt**：
```
Close-up, audit conclusion interface, grey input field with black Chinese text "[审计结论] 未见违规。交易公平。", timestamp auto-filling, digital signature as encrypted string, green save button at bottom, photorealistic base with subtle ink texture on screen, muted palette, cold weight of conclusion, ten-year commitment, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt** ```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful interface, emoji, English text, handwritten signature
```

---

## 镜头16：李思远手停键盘上方·看窗外近景

| 属性 | 内容 |
|------|------|
| **镜号** | 16 |
| **类型** | 近景 |
| **情绪** | 犹豫、十年后的自己审视现在 |
| **核心主体** | 李思远的手停在键盘上方，看向窗外——雨停了，城市灯光在水迹上闪烁 |
| **角色出场** | 李思远（侧脸，手部特写） |
| **尺寸** | 1280×720 |
| **技术备注** | 手部悬停动作暗示犹豫。窗外雨后城市：灯光倒映在湿漉漉路面，形成上下对称的光斑。雨停是情绪转折点。 |

**参考Prompt**：
```
Close-up, 35yo Chinese man's hand hovering above keyboard in hesitation, looking out window at post-rain city lights reflecting on wet pavement creating vertical symmetry of light spots, rain stopping as emotional turning point, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette with warm light reflections, self-examination from ten years future, soft ink bleeding at window edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, daytime, dry road, typing action
```

---

## 镜头17：酒店房间·黑暗中笔记本屏幕光中景

| 属性 | 内容 |
|------|------|
| **镜号** | 17 |
| **类型** | 中景 |
| **情绪** | GCGC前夕的独处、问题的重量 |
| **核心主体** | 酒店房间夜景，电视开着声音调低，李思远坐床边，笔记本屏幕照亮脸 |
| **角色出场** | 李思远（面部被屏幕光照亮，电视光在背景） |
| **尺寸** | 1280×720 |
| **技术备注** | 双光源：笔记本屏幕（冷蓝/白）为主光，电视（暖/动）为背景光。电视画面虚化显示国际会议画面。房间大部分在黑暗中。 |

**参考Prompt**：
```
Medium shot, hotel room at night, TV on with low volume showing blurred international conference footage in background, 35yo Chinese man sitting on bed edge, laptop screen illuminating his face with cold blue-white light, room mostly in darkness, dual light sources: laptop primary, TV secondary, photorealistic base with Chinese ink wash aesthetic, muted palette with screen glow accents, solitude before GCGC, weight of questions, soft ink bleeding at dark edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, fully lit room, warm lighting, no TV
```

---

## 镜头18：笔记本屏幕·问题清单删减特写

| 属性 | 内容 |
|------|------|
| **镜号** | 18 |
| **类型** | 特写（屏幕文字） |
| **情绪** | 思考的挣扎、删减至本质 |
| **核心主体** | 文本文档中光标闪烁，文字不断被删除又重写，最终只剩三行 |
| **角色出场** | 无（纯界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 文档界面：极简文本编辑器，白底黑字或黑底白字。光标闪烁是视觉节拍。删除过程可后期做逐字消失效果，T2I生成最终静态帧即可。 |

**参考Prompt**：
```
Close-up, minimalist text editor screen displaying three final lines of Chinese text about shared responsibility and human traceability, cursor blinking at end of last line, clean white background with black monospace font or dark mode inverse, thinking struggle reduced to essence, photorealistic base with subtle ink texture on screen, muted palette, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful word processor, cluttered toolbar, emoji, English text
```

---

## 镜头19：李思远保存文档面部特写

| 属性 | 内容 |
|------|------|
| **镜号** | 19 |
| **类型** | 近景/面部特写 |
| **情绪** | 疲惫但坚定、明天的承诺 |
| **核心主体** | 李思远盯着屏幕，灯光勾勒疲惫但坚定的轮廓，点击保存 |
| **角色出场** | 李思远（正脸，屏幕光为主光） |
| **尺寸** | 1280×720 |
| **技术备注** | 屏幕光在脸上形成高对比：亮部（额头、鼻梁）与暗部（眼窝、脸颊）。保存动作的瞬间眼神变化。IP-Adapter。 |

**参考Prompt**：
```
Close-up portrait, 35yo Chinese man with glasses staring at screen, laptop light creating high contrast on face: bright forehead and nose bridge, shadowed eye sockets and cheeks, moment of clicking save with subtle eye determination, weary but resolute, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, tomorrow's commitment, soft ink bleeding at edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed hands, extra fingers, mutated, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, smiling, cheerful, warm lighting, even lighting
```

---

## 镜头20：监控室关灯·屏幕暗下远景

| 属性 | 内容 |
|------|------|
| **镜号** | 20 |
| **类型** | 远景 |
| **情绪** | 一天的终结、守望的轮换 |
| **核心主体** | 李思远关掉监控室最后一盏灯，三块屏幕暗了，窗外雨停 |
| **角色出场** | 李思远（剪影/远景） |
| **尺寸** | 1280×720 |
| **技术备注** | 关灯动作：手伸向开关，画面从亮到暗的渐变。屏幕暗下后的余光。窗外雨后城市灯火倒映在湿漉漉路面。 |

**参考Prompt**：
```
Wide shot, Chinese man silhouette turning off last light in monitoring room, three monitors going dark, afterglow fading, outside window post-rain Shanghai city lights reflecting on wet pavement, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette, end of day's watch, soft ink bleeding at window edges, cinematic depth of field, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, bright room, screens on, daytime
```

---

## 镜头21：手机屏幕对话特写

| 属性 | 内容 |
|------|------|
| **镜号** | 21 |
| **类型** | 特写（手机屏幕） |
| **情绪** | 简洁的传承、守门员的确认 |
| **核心主体** | 手机对话：老王问"今天那套成了？" 李思远："成了。" "你做了什么？" "看有没有人被骗。" 老王："好。" |
| **角色出场** | 无（纯手机界面） |
| **尺寸** | 1280×720 |
| **技术备注** | 聊天界面：简洁IM设计，白底气泡。老王的气泡灰色，李思远的气泡白色/淡蓝。最后的"好"字单独一行，简短有力。 |

**参考Prompt**：
```
Close-up, smartphone chat interface showing conversation between two contacts, simple IM design with white and grey message bubbles, final single character "好" in its own line, concise transmission of gatekeeper confirmation, photorealistic base with Chinese ink wash aesthetic, muted palette with screen glow, soft ink bleeding at screen edges, shallow depth of field, cinematic, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text outside bubbles, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, colorful chat app, emoji, long message, English interface
```

---

## 镜头22：走出大楼·上海天际线远景

| 属性 | 内容 |
|------|------|
| **镜号** | 22 |
| **类型** | 远景 |
| **情绪** | 个体的渺小与问题的持续、融入城市 |
| **核心主体** | 李思远走出监控室大楼，雨后夜风吹动衣领，镜头抬高——上海天际线灯火如繁星 |
| **角色出场** | 李思远（远景，与天际线融合） |
| **尺寸** | 1280×720 |
| **技术备注** | 全篇收尾。人物从前景走向中景，镜头同步抬高至天际线。衣领被微风吹动是动态细节。灯火如繁星但不过度饱和。水墨晕染在天际线顶部。 |

**参考Prompt**：
```
Wide shot, Chinese man walking out of office building at night, post-rain breeze slightly moving his collar, camera lifting to Shanghai skyline lights like scattered stars, figure merging with city, individual smallness amidst persistent questions, photorealistic base with Chinese ink wash aesthetic, muted desaturated palette with warm light points, ink bleeding at skyline top, cinematic depth of field, fade atmosphere, 16:9, 8k, masterpiece
```

**负面Prompt**：
```
cartoon, anime, 3D render, oversaturated, bright colors, deformed, ugly, duplicate, watermark, signature, text, logo, cropped, worst quality, low quality, normal quality, jpeg artifacts, error, blurry, daytime, neon colors, crowded street, clear sky
```

---

## 核心视觉符号速查

| 符号 | 出现镜头 | 技术处理要点 |
|------|---------|-------------|
| 三块屏幕布局 | 06, 13, 20 | 左买家/右卖家/中监督，普通办公室质感，非科幻 |
| 半旧笔记本 | 03, 08, 11 | 软皮磨损，红笔圈出"守门员看什么"，工作笔记字迹 |
| 审计弹窗"保存期10年" | 02, 15 | 极简系统UI，白底黑字，时间戳和数字签名 |
| 电梯金属门 | 04, 05 | 闪回偏冷蓝，金属反光，门缝阴影线 |
| 雨后湿漉漉路面 | 16, 20, 22 | 灯光倒影形成垂直对称，水墨晕染从水面边缘 |
| 摄像头窗口（老夫妻/程序员） | 09, 10 | 低分辨率、轻微噪点、圆角黑框、像素化距离感 |

---

## 光影时序总表

| 场景 | 镜头 | 主光源 | 色温 | 水墨浓度 | 关键对比 |
|------|------|--------|------|----------|----------|
| 雨夜监控室 | 01-05 | 屏幕蓝光/冷白荧光 | 冷灰 7500K | 中 | 雨水模糊vs室内清晰 |
| AI谈判 | 06-15 | 三屏复合光 | 冷蓝/青/白混合 | 低 | 数据流动态vs观察者静态 |
| 酒店房间 | 17-19 | 笔记本屏幕光 | 冷白 8000K | 高 | 屏幕照亮脸vs房间黑暗 |
| 雨停尾声 | 20-22 | 城市夜光 | 暖黄点于冷黑中 | 高 | 个体渺小vs城市繁星 |

---

## AI不拟人化视觉规范

| 元素 | 处理方式 | 禁止事项 |
|------|---------|----------|
| 墨子 | 仅数据流/卡片UI/文字日志 | 禁止出现人脸、拟人化头像、语音波形拟人 |
| 贝壳-星云Agent | 仅日志界面/摄像头窗口 | 禁止出现AI角色形象、拟人化对话气泡 |
| 谈判过程 | 结构化数据交换、并发调用可视化 | 禁止出现两个"AI角色"对话场景 |
| 程序员/老夫妻 | 仅摄像头小窗口、像素化/低分辨率 | 禁止给予真人出场镜头、正面高清面部 |

---

## 待确认事项

- [ ] 李思远定妆规格 `ASSETS/CHARACTERS/李思远/定妆规格.md` 是否已建立？需包含：35岁、微胖、戴眼镜、深色polo衫、半旧笔记本道具
- [ ] 老王定妆规格 `ASSETS/CHARACTERS/老王/定妆规格.md` 是否已建立？闪回角色，50多岁、头发花白
- [ ] 三屏UI设计是否需UI设计师出独立规范，还是T2I生成后由后期精修？
- [ ] 摄像头窗口（老夫妻/程序员）的像素化/噪点程度是否需统一标准？
- [ ] 监控室场景是否需补充 `ASSETS/BACKGROUNDS/04_棋子_监控室_背景.md`？