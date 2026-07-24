# T2I SHOT SPECS — 36_算法法庭

> **源场景**: SCENES/36_算法法庭.md  
> **片长预估**: 11-13min  
> **核心主题**: 没有物理绑定就没有责任追溯  
> **视觉风格**: 法院门口阳光烈日，法庭内冷灰，老赵毛笔结尾暖黄；沉静克制  
> **总镜头数**: 22  
> **尺寸统一**: 1280×720, 16:9

---

## 角色出场索引

| 角色 | 出场镜号 | IP-Adapter 路径 |
|------|----------|-----------------|
| 老赵 | S01,S02,S03,S04,S05,S17,S18,S19 | `ASSETS/CHARACTERS/老赵/` (待建) |
| 李明 | S06,S07,S10 | `ASSETS/CHARACTERS/李明/` (待建) |
| 王磊 | S12,S13,S14,S15 | `ASSETS/CHARACTERS/王磊/` (待建) |
| 陈思危 | S16,S17,S18,S19,S20,S21 | `ASSETS/CHARACTERS/陈思危/` ✅ |
| 林薇 | S05,S06,S11 | `ASSETS/CHARACTERS/林薇/` (待建) |
| 老李/小王/小陈 | S21 | `ASSETS/CHARACTERS/数据权益代表/` (待建) |

---

## 分镜详表

### S01 — 法院大门外·老赵举牌
| 属性 | 内容 |
|------|------|
| **镜号** | S01 |
| **类型** | T2I |
| **情绪** | 等待/坚持 |
| **核心主体** | 北京法院大门外阳光下，60多岁老赵举牌，毛笔字"AI误诊，谁来负责？" |
| **角色出场** | 老赵 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 开场；远景→中景；阳光烈日；行人匆匆；无人停下；个人对抗系统 |
| **参考Prompt** | Beijing courthouse exterior, summer sun, 60+ Chinese man holding handwritten sign "AI误诊，谁来负责？", calligraphy brush strokes, pedestrians and lawyers passing by ignoring him, harsh bright sunlight, sense of quiet persistent waiting, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | dark, rainy, crowd gathering, dramatic lighting, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/老赵/` |

---

### S02 — 老赵的脸·等待
| 属性 | 内容 |
|------|------|
| **镜号** | S02 |
| **类型** | T2I |
| **情绪** | 安静/持续 |
| **核心主体** | 老赵的脸，被太阳晒红，表情不是愤怒是等待 |
| **角色出场** | 老赵 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 近景；晒红的皮肤；平静表情；工厂工人气质；退休老人 |
| **参考Prompt** | Lao Zhao, 60+ Chinese man, face slightly sunburned, expression not angry but quietly waiting, former factory worker's weathered face, learned calligraphy in youth, warm harsh sunlight, documentary realism, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | angry expression, young face, dramatic lighting, smiling, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/老赵/` |

---

### S03 — 牌子上的毛笔字特写
| 属性 | 内容 |
|------|------|
| **镜号** | S03 |
| **类型** | T2I |
| **情绪** | 尊严/追问 |
| **核心主体** | 毛笔字特写："AI误诊，谁来负责？" |
| **角色出场** | 老赵（手） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 特写；书法笔触；有力但不工整；个人尊严；烈日下 |
| **参考Prompt** | Close-up of handwritten sign with Chinese calligraphy "AI误诊，谁来负责？", brush stroke details, slightly uneven earnest handwriting, held by elderly hands, bright sunlight, sense of personal dignity, photorealistic, 16:9 |
| **负面Prompt** | printed text, perfect calligraphy, dark, anime |
| **角色IP-Adapter** | — |

---

### S04 — 老赵自言自语
| 属性 | 内容 |
|------|------|
| **镜号** | S04 |
| **类型** | T2I |
| **情绪** | 失去/解释 |
| **核心主体** | 老赵近景，讲述妻子故事，自言自语 |
| **角色出场** | 老赵 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 近景；口述；工厂老人；失去妻子；不是愤怒是追问 |
| **参考Prompt** | Lao Zhao close-up, speaking to invisible audience about his wife, sunburned face, quiet grief without tears, factory worker's hands gesturing slightly, bright courthouse sunlight, documentary realism, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | crying dramatically, young face, dark, smiling, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/老赵/` |

---

### S05 — 林薇经过·停下脚步
| 属性 | 内容 |
|------|------|
| **镜号** | S05 |
| **类型** | T2I |
| **情绪** | 看见/选择 |
| **核心主体** | 人群里林薇停下脚步，看老赵，然后走进法院 |
| **角色出场** | 林薇、老赵（背景） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；人群中；林薇侧影；老赵模糊背景；停顿然后离开 |
| **参考Prompt** | Lin Wei, 33yo Chinese woman, pausing in crowd outside courthouse, looking at elderly man with sign in background, then turning toward court entrance, bright sunlight, sense of witnessing and choosing, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | dark, rainy, interacting directly, smiling, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/林薇/` |

---

### S06 — 法庭内·李明案
| 属性 | 内容 |
|------|------|
| **镜号** | S06 |
| **类型** | T2I |
| **情绪** | 制度/冰冷 |
| **核心主体** | 法庭内部，李明坐轮椅，对面三个平台律师 |
| **角色出场** | 李明、林薇（旁听） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；法庭冷灰；轮椅；西装律师；制度空间；旁听席林薇 |
| **参考Prompt** | Chinese courtroom interior, young man in wheelchair (Li Ming, 29yo, right leg amputated) facing three corporate lawyers in suits, cool gray fluorescent lighting, formal institutional setting, Lin Wei in gallery background, documentary realism, photorealistic, 16:9 |
| **负面Prompt** | warm lighting, casual, smiling, dramatic, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/李明/` |

---

### S07 — 屏幕上的调度记录
| 属性 | 内容 |
|------|------|
| **镜号** | S07 |
| **类型** | T2I |
| **情绪** | 证据/冰冷计算 |
| **核心主体** | 屏幕展开算法调度记录：时间少15%，下午3:00建议休息，3:47事故 |
| **角色出场** | 无 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 屏幕特写；数据记录；时间轴；算法痕迹；冰冷 |
| **参考Prompt** | Courtroom screen showing algorithm dispatch records, timeline: delivery time 15% shorter than actual route, 3:00 PM "suggest rest" notification, 3:47 PM accident marker, data visualization, cool blue-gray interface, photorealistic, 16:9 |
| **负面Prompt** | warm colors, human faces, dramatic, anime |
| **角色IP-Adapter** | — |

---

### S08 — 法官近景
| 属性 | 内容 |
|------|------|
| **镜号** | S08 |
| **类型** | T2I |
| **情绪** | 权威/判决 |
| **核心主体** | 法官低头看着记录，"判决：平台承担百分之八十责任" |
| **角色出场** | 法官 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 近景；法官袍；低头；记录；权威但不夸张 |
| **参考Prompt** | Chinese judge in robe, looking down at documents, authoritative but restrained expression, courtroom cool gray lighting, sense of institutional justice, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | dramatic gavel, shouting, warm colors, smiling, anime |
| **角色IP-Adapter** | — |

---

### S09 — 李明低头沉默
| 属性 | 内容 |
|------|------|
| **镜号** | S09 |
| **类型** | T2I |
| **情绪** | 没有胜利/空虚 |
| **核心主体** | 李明在轮椅上低头沉默，没有胜利的表情 |
| **角色出场** | 李明 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 近景；轮椅；低头；沉默；八十七万换不回腿 |
| **参考Prompt** | Li Ming, 29yo Chinese man in wheelchair, head bowed in silence, no expression of victory, courtroom background, cool gray light, sense of hollow compensation, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | smiling, celebrating, warm colors, dramatic, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/李明/` |

---

### S10 — 林薇笔记本·"如果日志不存在呢？"
| 属性 | 内容 |
|------|------|
| **镜号** | S10 |
| **类型** | T2I |
| **情绪** | 追问/延伸 |
| **核心主体** | 林薇写下："八十七万。"另起一行："如果日志不存在呢？" |
| **角色出场** | 林薇（手/笔记本） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 特写；笔记本；手写；问题延伸；从李明案想到老赵 |
| **参考Prompt** | Close-up of notebook, handwritten Chinese: "八十七万。" then "平台的日志完整 → 责任边界清晰 → 能判。如果日志不存在呢？", woman's hand writing, courtroom gallery seat, cool gray ambient light, photorealistic, 16:9 |
| **负面Prompt** | digital text, bright colors, warm, anime |
| **角色IP-Adapter** | — |

---

### S11 — 北大法学院·王磊办公室
| 属性 | 内容 |
|------|------|
| **镜号** | S11 |
| **类型** | T2I |
| **情绪** | 学术/七年 |
| **核心主体** | 北大法学院王磊办公室，墙上贴满算法治理思维导图 |
| **角色出场** | 王磊、林薇 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；学术办公室；思维导图；论文摘要；七年研究痕迹 |
| **参考Prompt** | Peking University law professor's office, walls covered with algorithm governance mind maps and paper abstracts, Wang Lei seated at desk, scholarly atmosphere, natural window light, intellectual accumulation of seven years, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | empty walls, casual, dark, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/王磊/` |

---

### S12 — 王磊·"物理绑定"
| 属性 | 内容 |
|------|------|
| **镜号** | S12 |
| **类型** | T2I |
| **情绪** | 核心概念/力透纸背 |
| **核心主体** | 王磊站起来在白板上用力写下三个字："物理绑定" |
| **角色出场** | 王磊 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；白板；用力写字；三个字；学术力量；与陈思危白板呼应 |
| **参考Prompt** | Wang Lei, Chinese law professor, standing at whiteboard writing "物理绑定" with forceful strokes, academic office, natural light, sense of intellectual breakthrough, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | dark, casual, smiling, weak strokes, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/王磊/` |

---

### S13 — 林薇想起老赵
| 属性 | 内容 |
|------|------|
| **镜号** | S13 |
| **类型** | T2I |
| **情绪** | 连接/不公 |
| **核心主体** | 林薇表情，想起法院门外老赵举了三个月，草案讨论了三年 |
| **角色出场** | 林薇 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 近景；窗外隐约蝉鸣；表情变化；从学术到现实 |
| **参考Prompt** | Lin Wei close-up, expression shifting from academic understanding to realization of injustice, office window with summer cicadas suggested, natural light, sense of connection between two cases, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | dark, smiling, dramatic, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/林薇/` |

---

### S14 — 陈思危看屏幕·墨子架构图
| 属性 | 内容 |
|------|------|
| **镜号** | S14 |
| **类型** | T2I |
| **情绪** | 设计/底线 |
| **核心主体** | 陈思危看屏幕，墨子系统架构图，审计日志模块红色高亮 |
| **角色出场** | 陈思危 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；屏幕；架构图；红色高亮；三年前坚持的设计 |
| **参考Prompt** | Chen Siwei looking at screen showing Mozi system architecture diagram, audit log module highlighted in red, office cool gray lighting, sense of foresight and bottom line design, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | warm lighting, casual, smiling, bright colors, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/陈思危/` |

---

### S15 — 法院门外·陈思危走向老赵
| 属性 | 内容 |
|------|------|
| **镜号** | S15 |
| **类型** | T2I |
| **情绪** | 接近/两种人 |
| **核心主体** | 下午四点太阳很烈，老赵牌子举得比上午低，陈思危走到他旁边 |
| **角色出场** | 老赵、陈思危 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；烈日；老赵草帽；牌子放低；陈思危走近；热浪 |
| **参考Prompt** | Courthouse exterior, 4pm harsh summer sun, Lao Zhao with straw hat holding sign lower than morning, Chen Siwei approaching him, heat haze in air, sense of two different worlds meeting, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/老赵/`, `ASSETS/CHARACTERS/陈思危/` |

---

### S16 — 两人对话近景
| 属性 | 内容 |
|------|------|
| **镜号** | S16 |
| **类型** | I2V |
| **情绪** | 倾听/行业 |
| **核心主体** | 老赵与陈思危对话，"你们做AI的，知不知道你们的东西会出错？" |
| **角色出场** | 老赵、陈思危 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | I2V关键帧；双人中近景；烈日；老赵疲惫但不卑；陈思危坦诚 |
| **参考Prompt** | Two-shot close-up, Lao Zhao and Chen Siwei in conversation outside courthouse, harsh summer sun, elderly man's weathered face facing tech founder, honest exchange between two worlds, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | cool shade, smiling, casual, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/老赵/`, `ASSETS/CHARACTERS/陈思危/` |

---

### S17 — 老赵讲述·长镜头
| 属性 | 内容 |
|------|------|
| **镜号** | S17 |
| **类型** | I2V |
| **情绪** | 承受/讲述 |
| **核心主体** | 老赵讲述妻子故事，嘴在动，看脸、手、停顿 |
| **角色出场** | 老赵 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | I2V关键帧；长镜头感；片段声音；脸部特写；手部；停顿 |
| **参考Prompt** | Lao Zhao close-up, telling wife's story, mouth moving but we see face and hands more than hear words, pauses and swallows, sunburned skin, sense of unbearable memory borne quietly, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | crying, dramatic, young, smiling, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/老赵/` |

---

### S18 — 老赵重新举起牌子
| 属性 | 内容 |
|------|------|
| **镜号** | S18 |
| **类型** | T2I |
| **情绪** | 尊严/继续 |
| **核心主体** | 老赵："我不是要钱。我是要一个人站出来说：是我们的责任。"重新举起牌子 |
| **角色出场** | 老赵 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 近景；重新举起；牌子；阳光下；尊严；不是结束 |
| **参考Prompt** | Lao Zhao, close-up, re-raising his sign with steady hands, bright courthouse sunlight, expression of quiet dignity, sense of continuing despite everything, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | dark, defeated, crying, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/老赵/` |

---

### S19 — 老赵家·电话·鉴定报告
| 属性 | 内容 |
|------|------|
| **镜号** | S19 |
| **类型** | T2I |
| **情绪** | 系统缺陷/无法归属 |
| **核心主体** | 老赵家客厅，电话铃响，律师告知没有完整决策日志 |
| **角色出场** | 老赵 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；老赵家；电话；听；沉默；系统缺陷 |
| **参考Prompt** | Lao Zhao in modest living room, answering phone, listening to lawyer, expression slowly shifting from hope to blankness, warm afternoon light, sense of system failure, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | bright celebration, smiling, dramatic rage, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/老赵/` |

---

### S20 — 毛笔·最后两个字
| 属性 | 内容 |
|------|------|
| **镜号** | S20 |
| **类型** | T2I |
| **情绪** | 留白/尊严 |
| **核心主体** | 老赵拿起毛笔，蘸墨，在宣纸上慢慢写了两个字（不揭示内容） |
| **角色出场** | 老赵（手） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 特写；毛笔；墨；宣纸；手稳；留白；不揭示内容 |
| **参考Prompt** | Close-up of elderly man's steady hand holding brush, dipping in ink, writing slowly on rice paper, brush stroke details, sense of dignity through art, warm afternoon light, photorealistic base with Chinese ink wash aesthetic, shallow depth of field, 16:9 |
| **负面Prompt** | revealing text, digital pen, bright colors, shaky hand, anime |
| **角色IP-Adapter** | — |

---

### S21 — 数据信托谈判桌
| 属性 | 内容 |
|------|------|
| **镜号** | S21 |
| **类型** | T2I |
| **情绪** | 制度尝试/对话 |
| **核心主体** | "数据权益联盟"，老李、小王、小陈坐在对面，陈思危面对他们 |
| **角色出场** | 陈思危、老李、小王、小陈 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；谈判桌；三个普通人 vs 技术创始人；制度尝试 |
| **参考Prompt** | Meeting room, three ordinary Chinese people (retired teacher Lao Li, delivery rider Xiao Wang, community worker Xiao Chen) sitting across from Chen Siwei at negotiation table, sense of grassroots institutional experiment, cool neutral lighting, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | hostile confrontation, warm celebration, empty room, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/陈思危/` |

---

### S22 — 老赵放下毛笔·走出门
| 属性 | 内容 |
|------|------|
| **镜号** | S22 |
| **类型** | T2I |
| **情绪** | 继续/留白 |
| **核心主体** | 老赵放下毛笔，拿起外套，走出门，门在身后关上 |
| **角色出场** | 老赵 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 远景；门关上；留白；老赵继续；不写是什么字 |
| **参考Prompt** | Lao Zhao from behind, putting down brush, picking up jacket, walking out door, door closing, warm afternoon light fading, sense of unresolved continuation, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | dramatic music, bright celebration, revealing face, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/老赵/` |

---

## 角色定妆需求清单

| 角色 | 状态 | 优先级 |
|------|------|--------|
| 老赵 | 待建 | **高** — 60+工厂退休工人，书法，核心象征角色 |
| 李明 | 待建 | 中 — 29岁外卖骑手，右腿截肢，轮椅 |
| 王磊 | 待建 | 中 — 北大法学院教授，算法治理研究者 |
| 陈思危 | ✅ | 已存在 |
| 林薇 | 待建 | 中 — 旁听者+连接者 |
| 老李/小王/小陈 | 待建 | 低 — 数据权益代表，三个普通人 |

---

## 背景规格需求

| 场景 | 状态 | 说明 |
|------|------|------|
| 北京法院门外 | 待建 | 烈日，夏天，蝉鸣，个人对抗制度 |
| 法庭内部 | 待建 | 冷灰，制度空间，可与已有法庭场景共用 |
| 北大法学院办公室 | 待建 | 学术，思维导图墙，自然窗光 |
| 老赵家 | 待建 | 朴素客厅，毛笔，宣纸，午后阳光 |
| 深智科技会议室 | 待建 | 数据信托谈判，可与25集会议室共用 |

---

## 视觉一致性备忘

- **老赵书法**: 核心视觉符号，从牌子毛笔字(S01)到最后宣纸写字(S20)，书法是个人尊严的锚点
- **烈日与冷灰**: 法院门外烈日( symbolizes 个人坚持) ↔ 法庭内冷灰( symbolizes 制度空间)
- **留白**: S20不写老赵写了什么字，留给观众；S22门关上，故事继续但不揭示
- **陈思危的两次接近**: 接近老赵(S15-S18) vs 接近三个普通人(S21)，技术与社会的双向努力
- **"物理绑定"**: 王磊白板上的三个字，是全书核心概念之一，需视觉强调
- **水墨适配**: 老赵书法场景天然适配水墨；法院烈日可用淡墨渲染空气感