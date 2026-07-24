# T2I SHOT SPECS — 22_代价

> **源场景**: SCENES/22_代价.md  
> **片长预估**: 7-9min  
> **核心主题**: 谁承担历史的成本  
> **视觉风格**: 林薇直播间暖调串三段时间线（宋代/明代/美国），三条线各有独特色调  
> **总镜头数**: 19  
> **尺寸统一**: 1280×720, 16:9

---

## 角色出场索引

| 角色 | 出场镜号 | IP-Adapter 路径 |
|------|----------|-----------------|
| 林薇 | S01,S17,S18,S19 | `ASSETS/CHARACTERS/林薇/` (待建) |
| 陈圆 | S02,S03,S04,S05,S06,S07,S08 | `ASSETS/CHARACTERS/陈圆/` ✅ |
| 沈固 | S09,S10,S11,S12 | `ASSETS/CHARACTERS/沈固/` (待建) |
| 鲍勃 | S13,S14,S15,S16 | `ASSETS/CHARACTERS/鲍勃/` ✅ |
| 多萝西 | S15,S16 | `ASSETS/CHARACTERS/多萝西/` ✅ |
| 沈梁 | S11,S12 | `ASSETS/CHARACTERS/沈梁/` (待建) |

---

## 分镜详表

### S01 — 林薇展开三件复制品
| 属性 | 内容 |
|------|------|
| **镜号** | S01 |
| **类型** | T2I |
| **情绪** | 平静/建立 |
| **核心主体** | 林薇坐在直播间，桌上展开三件复制品：地契扫描件、册子照片、生锈工牌 |
| **角色出场** | 林薇 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 开场；三件物品清晰展示；林薇手部动作；暖台灯；直播间氛围 |
| **参考Prompt** | Lin Wei, 33yo Chinese woman, scholarly elegant appearance, sitting at wooden desk in warm studio, three historical items spread before her: aged land deed, old booklet photo, rusty worker ID badge, warm desk lamp from side, bookshelf background, documentary realism, low saturation, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | bright commercial lighting, glamorous makeup, futuristic UI, oversaturated colors, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/林薇/` |

---

### S02 — 汴京街景·朱雀坊茶坊
| 属性 | 内容 |
|------|------|
| **镜号** | S02 |
| **类型** | T2I |
| **情绪** | 温暖/历史入场 |
| **核心主体** | 汴京街景，朱雀坊茶坊前，石榴树花正红，宋代建筑 |
| **角色出场** | 陈圆（远景入画） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 宋代线定调；暖黄色调；《清明上河图》风格参考；远景人群；水墨质感加重 |
| **参考Prompt** | Song Dynasty China street scene, Bianjing city, warm yellow golden tone, small tea house with pomegranate tree in bloom, ancient Chinese architecture wooden structures, ink painting aesthetic, 《清明上河图》style, distant crowds in Song costumes, atmospheric haze, photorealistic base with Chinese ink wash texture, 16:9 |
| **负面Prompt** | Ming Dynasty elements, Qing Dynasty architecture, modern buildings, neon signs, anime, cartoon |
| **角色IP-Adapter** | — |

---

### S03 — 陈圆在茶坊门口揉面
| 属性 | 内容 |
|------|------|
| **镜号** | S03 |
| **类型** | T2I |
| **情绪** | 踏实/劳作 |
| **核心主体** | 陈圆在茶坊门口揉面，汗珠晶莹，手部精细 |
| **角色出场** | 陈圆 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；宋代襦裙；汗珠细节；揉面动作；茶坊木门背景；暖光 |
| **参考Prompt** | Chen Yuan, 30yo Song Dynasty Chinese woman, gentle classical beauty, wearing Song Dynasty ruqun dress, kneading dough at tea house entrance, sweat beads on forehead glistening, hands in detail motion, wooden door frame behind, warm golden afternoon light, photorealistic base with Chinese ink wash aesthetic, historical accuracy, 16:9 |
| **负面Prompt** | Ming Qing costumes, modern makeup, anachronistic elements, bright commercial lighting, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/陈圆/` |

---

### S04 — 薄纸地契特写
| 属性 | 内容 |
|------|------|
| **镜号** | S04 |
| **类型** | T2I |
| **情绪** | 骄傲/契约 |
| **核心主体** | 薄纸地契特写："陈圆，朱雀坊民女" |
| **角色出场** | 陈圆（手） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 微距；宋代纸张质感；手写墨迹；官印模糊；手部皮肤纹理 |
| **参考Prompt** | Close-up of aged Song Dynasty land deed on thin rice paper, Chinese calligraphy "陈圆，朱雀坊民女", faded red official seal, weathered paper texture, woman's hand holding it gently, warm golden light, shallow depth of field, historical document realism, photorealistic base with ink wash texture, 16:9 |
| **负面Prompt** | modern paper, printed text, clean white background, bright colors, digital document |
| **角色IP-Adapter** | — |

---

### S05 — 陈圆独自走进衙门
| 属性 | 内容 |
|------|------|
| **镜号** | S05 |
| **类型** | I2V |
| **情绪** | 独立/尊严 |
| **核心主体** | 陈圆独自走进衙门办地契，不需要男人挂名 |
| **角色出场** | 陈圆 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | I2V关键帧；衙门建筑；陈圆背影/中景；宋代官服人群；暖调 |
| **参考Prompt** | Chen Yuan, Song Dynasty woman in ruqun dress, walking alone into ancient Chinese government yamen office, wooden architecture with stone lions, other people in Song costumes around, her posture confident and independent, warm golden historical tone, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | Ming Qing architecture, modern clothing, anachronistic elements, cool colors, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/陈圆/` |

---

### S06 — 金兵入城·茶坊牌匾砸落
| 属性 | 内容 |
|------|------|
| **镜号** | S06 |
| **类型** | I2V |
| **情绪** | 破碎/历史断裂 |
| **核心主体** | 金兵入城，烟火，人群奔逃，茶坊牌匾砸落 |
| **角色出场** | 陈圆（远景） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | I2V关键帧；动作场面但保持水墨克制；烟雾不夸张；牌匾砸落瞬间；色调转冷 |
| **参考Prompt** | Song Dynasty city under attack, Jin soldiers entering gates, smoke rising in distance, crowds fleeing in panic, wooden tea house signboard falling, historical chaos captured with restraint, warm tones shifting to cold gray, dust in air, photorealistic base with Chinese ink wash aesthetic, cinematic but not Hollywood, 16:9 |
| **负面Prompt** | excessive fire, explosions, blood, Hollywood action style, bright colors, anime |
| **角色IP-Adapter** | — |

---

### S07 — 陈圆在茶坊·远房堂兄
| 属性 | 内容 |
|------|------|
| **镜号** | S07 |
| **类型** | T2I |
| **情绪** | 接受但不对/隐忍 |
| **核心主体** | 陈圆在茶坊，远房堂兄坐着什么也不做，她每月分他一成 |
| **角色出场** | 陈圆、远房堂兄 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；堂兄懒散姿态 vs 陈圆劳作；茶坊内部；暖调但压抑 |
| **参考Prompt** | Song Dynasty tea house interior, Chen Yuan working while distant male relative sits idle doing nothing, wooden tables and benches, warm but oppressive atmosphere, traditional Chinese interior, photorealistic base with Chinese ink wash aesthetic, subtle tension in composition, 16:9 |
| **负面Prompt** | modern furniture, bright cheerful lighting, smiling faces, anachronistic elements, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/陈圆/` |

---

### S08 — 陈圆年老的手收地契
| 属性 | 内容 |
|------|------|
| **镜号** | S08 |
| **类型** | T2I |
| **情绪** | 沉寂/历史封存 |
| **核心主体** | 陈圆年老的手把地契收进箱底 |
| **角色出场** | 陈圆（老年，手部） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 特写；老年手部皱纹；木箱纹理；地契折痕；暖调但黯淡；结束宋代线 |
| **参考Prompt** | Close-up of elderly Chinese woman's wrinkled hands, folding aged land deed, placing it into wooden box, weathered skin texture, warm but dim golden light, sense of history sealed away, photorealistic base with Chinese ink wash aesthetic, shallow depth of field, 16:9 |
| **负面Prompt** | young hands, bright lighting, modern box, colorful scene, anime |
| **角色IP-Adapter** | — |

---

### S09 — 沈固坐在空了的织坊
| 属性 | 内容 |
|------|------|
| **镜号** | S09 |
| **类型** | T2I |
| **情绪** | 空洞/遗落 |
| **核心主体** | 沈固坐在空了的织坊，铜器银两被洗劫，空架子 |
| **角色出场** | 沈固 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 明代线定调；灰青色调；空织坊架子；灰尘；窗光；与宋代暖黄形成对比 |
| **参考Prompt** | Ming Dynasty empty textile workshop, wooden shelves stripped bare, 50yo Chinese man in rough gray robe sitting alone in center, dust particles in dim light through window, gray-blue Qinghui tone, desolate atmosphere, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | Song Dynasty elements, bright colors, cheerful scene, modern objects, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/沈固/` |

---

### S10 — 散落在地上的旧书碎片
| 属性 | 内容 |
|------|------|
| **镜号** | S10 |
| **类型** | T2I |
| **情绪** | 残破/知识消逝 |
| **核心主体** | 散落在地上的旧书碎片 |
| **角色出场** | 无 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 特写；书页碎片；墨迹；灰尘；灰青色调；织坊地面 |
| **参考Prompt** | Close-up of scattered old book fragments on dusty wooden floor, Ming Dynasty printed pages torn, ink characters partially visible, dust settled on paper, gray-blue tone, sense of lost knowledge, photorealistic base with Chinese ink wash aesthetic, shallow depth of field, 16:9 |
| **负面Prompt** | clean paper, bright lighting, modern book, colorful scene, digital text |
| **角色IP-Adapter** | — |

---

### S11 — 沈梁把旧书交给官员
| 属性 | 内容 |
|------|------|
| **镜号** | S11 |
| **类型** | T2I |
| **情绪** | 冷漠/制度碾压 |
| **核心主体** | 沈梁（孙子）在皂角树下把旧书交给官员 |
| **角色出场** | 沈梁、官员 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；皂角树；明代官服；交接动作；灰青色调；官员冷漠表情 |
| **参考Prompt** | Ming Dynasty scene under soapberry tree, young man Shen Liang handing old books to official in Ming government robe, official expression cold and indifferent, traditional Chinese garden setting, gray-blue Qinghui tone, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | modern clothing, bright cheerful colors, smiling faces, anachronistic elements, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/沈梁/` |

---

### S12 — 沈梁站在皂角树下
| 属性 | 内容 |
|------|------|
| **镜号** | S12 |
| **类型** | I2V |
| **情绪** | 悲伤/风吹 |
| **核心主体** | 沈梁站在皂角树下，风吹树叶 |
| **角色出场** | 沈梁 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | I2V关键帧；风吹树叶动态；沈梁背影/侧影；灰青色调；结束明代线 |
| **参考Prompt** | Shen Liang, young Chinese man, standing under soapberry tree, wind blowing leaves, back view or side profile, Ming Dynasty scholar clothing, gray-blue tone, melancholic atmosphere, leaves in motion, photorealistic base with Chinese ink wash aesthetic, cinematic, 16:9 |
| **负面Prompt** | bright colors, smiling, modern clothing, cherry blossoms (wrong tree), anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/沈梁/` |

---

### S13 — 鲍勃在福特工厂流水线
| 属性 | 内容 |
|------|------|
| **镜号** | S13 |
| **类型** | T2I |
| **情绪** | 踏实/工业时代 |
| **核心主体** | 鲍勃在福特工厂流水线，工装挂在第二个钩子 |
| **角色出场** | 鲍勃 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 美国线定调；40年代底特律工厂；暖褪色调；工业质感；工装细节 |
| **参考Prompt** | Bob, 60+ American white man, working on Ford assembly line, 1940s Detroit factory interior, work uniform hanging on second hook, industrial machinery background, warm faded film grain tone, documentary realism, photorealistic base with subtle ink wash texture, 16:9 |
| **负面Prompt** | modern factory, bright colors, clean environment, futuristic, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/鲍勃/` |

---

### S14 — 银白色工牌特写
| 属性 | 内容 |
|------|------|
| **镜号** | S14 |
| **类型** | T2I |
| **情绪** | 岁月/磨损 |
| **核心主体** | 银白色工牌，边角磨圆 |
| **角色出场** | 鲍勃（手） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 特写；工牌磨损细节；银白色氧化；挂绳旧化；暖褪色调 |
| **参考Prompt** | Close-up of silver-white employee ID badge, edges worn round and smooth, metal slightly oxidized, old fabric lanyard, weathered texture, warm faded film grain tone, shallow depth of field, documentary realism, photorealistic, 16:9 |
| **负面Prompt** | new clean badge, bright colors, modern design, digital display, anime |
| **角色IP-Adapter** | — |

---

### S15 — 黑暗客厅·鲍勃和多萝西并肩坐着
| 属性 | 内容 |
|------|------|
| **镜号** | S15 |
| **类型** | T2I |
| **情绪** | 悲凉/暮色 |
| **核心主体** | 黑暗客厅，鲍勃和多萝西并肩坐着，暖褪色调 |
| **角色出场** | 鲍勃、多萝西 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；40年代底特律房子；暗调；窗光；两人姿态；历史感 |
| **参考Prompt** | Elderly American couple, Bob and Dorothy, sitting side by side on worn sofa in dark living room, 1940s Detroit house interior, warm faded film grain, melancholic afternoon light through window, both looking forward with quiet sadness, documentary realism, photorealistic base with subtle ink wash texture, 16:9 |
| **负面Prompt** | bright room, modern furniture, smiling, vibrant colors, clean environment, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/鲍勃/`, `ASSETS/CHARACTERS/多萝西/` |

---

### S16 — 多萝西把工牌放进纸箱
| 属性 | 内容 |
|------|------|
| **镜号** | S16 |
| **类型** | T2I |
| **情绪** | 沉默/封存 |
| **核心主体** | 多萝西把工牌放进储藏室纸箱，合上盖子 |
| **角色出场** | 多萝西（手） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 特写；手部动作；纸箱；储藏室昏暗；结束美国线；与S08陈圆收地契呼应 |
| **参考Prompt** | Close-up of elderly woman's hands placing worn worker ID badge into cardboard box in dim storage room, closing lid slowly, warm faded film grain tone, dust in air, sense of ending and storage, documentary realism, photorealistic, 16:9 |
| **负面Prompt** | bright lighting, modern room, smiling, colorful, anime |
| **角色IP-Adapter** | — |

---

### S17 — 三件史料并排·林薇抚摸
| 属性 | 内容 |
|------|------|
| **镜号** | S17 |
| **类型** | T2I |
| **情绪** | 沉思/串联 |
| **核心主体** | 三件史料并排，林薇的手缓缓抚摸 |
| **角色出场** | 林薇（手/部分身体） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；三件物品并置；林薇手部动作；暖台灯；与S01呼应 |
| **参考Prompt** | Three historical items laid side by side on wooden desk: aged Chinese land deed, old booklet fragments, rusty American worker badge, woman's hand gently touching them, warm desk lamp light, sense of connection across time, documentary realism, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | bright commercial lighting, futuristic, oversaturated, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/林薇/` |

---

### S18 — 林薇抬头看向镜头
| 属性 | 内容 |
|------|------|
| **镜号** | S18 |
| **类型** | I2V |
| **情绪** | 凝视/当代追问 |
| **核心主体** | 林薇抬头，看向镜头（观众） |
| **角色出场** | 林薇 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | I2V关键帧；核心情感镜头；浅景深；直视观众；打破第四墙 |
| **参考Prompt** | Lin Wei, 33yo Chinese woman, medium close-up, looking directly into camera, warm studio light, bookshelf background, contemplative expression, low saturation, cinematic, photorealistic base with Chinese ink wash aesthetic, direct gaze at viewer, 16:9 |
| **负面Prompt** | looking away, bright commercial lighting, smiling, dramatic makeup, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/林薇/` |

---

### S19 — 直播间灯光渐暗
| 属性 | 内容 |
|------|------|
| **镜号** | S19 |
| **类型** | T2I |
| **情绪** | 余韵/沉思 |
| **核心主体** | 直播间灯光渐暗，只剩台灯照亮桌面的三件史料 |
| **角色出场** | 无 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 收尾镜；暗调；台灯聚焦；三件物品在光中；环境沉入黑暗 |
| **参考Prompt** | Dim studio room, only desk lamp illuminating three historical items on wooden table, rest of room in shadow, warm focused light, quiet contemplative atmosphere, sense of history's weight, photorealistic base with Chinese ink wash aesthetic, low saturation, cinematic, 16:9 |
| **负面Prompt** | bright room, multiple light sources, colorful, futuristic, anime |
| **角色IP-Adapter** | — |

---

## 角色定妆需求清单

| 角色 | 状态 | 优先级 |
|------|------|--------|
| 林薇 | 待建 | **高** — 多集核心讲述者，需完整定妆 |
| 沈固 | 待建 | 中 — 明代线核心，50岁织造后裔 |
| 沈梁 | 待建 | 低 — 仅S11/S12出场，沈固孙子 |
| 陈圆 | ✅ | 已存在，需确认宋代襦裙造型适配 |
| 鲍勃 | ✅ | 已存在，需确认40年代工装造型 |
| 多萝西 | ✅ | 已存在，需确认老年造型适配 |

---

## 背景规格需求

| 场景 | 状态 | 说明 |
|------|------|------|
| 林薇直播间 | 待建 | 核心重复场景，木质书桌+台灯+书架，可与22/24共用 |
| 汴京朱雀坊 | 待建 | 宋代线，可与19_汴京的茶香共用 |
| 明代织坊 | 待建 | 明代线，灰青色调，空架子+灰尘 |
| 40年代底特律工厂 | 待建 | 美国线，可与21_美国梦的味道共用 |
| 40年代底特律民居 | 待建 | 美国线，黑暗客厅，暖褪色调 |

---

## 视觉一致性备忘

- **三线色调区分**:
  - 宋代线：暖黄金调，汴京繁华与凋零
  - 明代线：灰青调，空寂与制度冷漠
  - 美国线：暖褪色调，胶片颗粒感，工业时代余晖
- **直播间**: 始终暖台灯，林薇作为穿越三线的叙述锚点
- **封存动作呼应**: S08陈圆收地契 ↔ S16多萝西收工牌，跨越时空的女性封存历史
- **水墨适配**: 宋代线可加重水墨比例；明代线偏灰青水墨；美国线保持写实基底+轻微褪色质感