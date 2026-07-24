# T2I SHOT SPECS — 11_极速ASI

> **源场景**: SCENES/11_极速ASI.md  
> **片长预估**: 8-10min  
> **核心主题**: 被速度甩下的人  
> **视觉风格**: 上海出租屋暖调，低饱和，真实质感  
> **总镜头数**: 16  
> **尺寸统一**: 1280×720, 16:9

---

## 角色出场索引

| 角色 | 出场镜号 | IP-Adapter 路径 |
|------|----------|-----------------|
| 周沫 | S02,S03,S04,S05,S07,S08,S09,S11,S12,S13,S14,S15,S16 | `ASSETS/CHARACTERS/周沫/` (待建) |
| 技术总监 | S06 | `ASSETS/CHARACTERS/技术总监/` (待建) |
| 弹幕字形 | S14 | CG合成 |

---

## 分镜详表

### S01 — 上海夜景·冬·窗外万家灯火
| 属性 | 内容 |
|------|------|
| **镜号** | S01 |
| **类型** | T2I |
| **情绪** | 建立/疏离 |
| **核心主体** | 上海冬夜城市远景，万家灯火，冷蓝灰天空 |
| **角色出场** | 无 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 开场定调镜；冷蓝灰与室内暖黄形成对比；远景不聚焦具体建筑，取城市肌理 |
| **参考Prompt** | Shanghai winter night cityscape, panoramic view from apartment window, thousands of warm yellow window lights against cold blue-gray sky, distant skyscrapers blurred, atmospheric haze, cinematic wide shot, low saturation, photorealistic with subtle ink wash texture, muted tones, 16:9 |
| **负面Prompt** | oversaturated, neon cyberpunk, cartoon, anime, futuristic vehicles, flying cars |
| **角色IP-Adapter** | — |

---

### S02 — 周沫坐在直播间白墙前
| 属性 | 内容 |
|------|------|
| **镜号** | S02 |
| **类型** | T2I |
| **情绪** | 日常/坚持 |
| **核心主体** | 周沫坐在小型直播间，白墙贴满手写A4纸公式，小台灯暖光 |
| **角色出场** | 周沫 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；A4纸上的公式需清晰可辨："注意力机制""残差连接"等；台灯为唯一主光源；上海老破小真实质感 |
| **参考Prompt** | Zhou Mo, 30yo Chinese woman, delicate natural beauty with slight fatigue under eyes, casual home clothes loose sweater, sitting in small livestream corner, white wall covered with handwritten A4 papers with machine learning formulas, small desk lamp warm yellow light, tiny messy Shanghai apartment, realistic everyday lighting, low saturation, documentary style, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | glamorous makeup, professional studio, clean minimalist, bright commercial lighting, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/周沫/` |

---

### S03 — A4纸上的字特写
| 属性 | 内容 |
|------|------|
| **镜号** | S03 |
| **类型** | T2I |
| **情绪** | 专注/知识 |
| **核心主体** | A4纸特写，手写中文字："注意力机制""残差连接" |
| **角色出场** | 周沫（手/写字痕迹） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 微距感特写；手写字体需自然不工整；纸张略有卷边和胶带痕迹；暖黄台灯侧光 |
| **参考Prompt** | Close-up of handwritten A4 paper on wall, Chinese characters "注意力机制" and "残差连接", natural messy handwriting, paper slightly curled with transparent tape marks, warm desk lamp side light, shallow depth of field, realistic paper texture, low saturation, documentary photography style, 16:9 |
| **负面Prompt** | printed font, perfect calligraphy, digital text, clean white paper, studio lighting |
| **角色IP-Adapter** | — |

---

### S04 — 在线人数：23人跳动
| 属性 | 内容 |
|------|------|
| **镜号** | S04 |
| **类型** | T2I |
| **情绪** | 坚持/微小 |
| **核心主体** | 手机屏幕/电脑屏幕显示直播间在线人数"23"，缓慢跳动 |
| **角色出场** | 周沫（手部入镜） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 屏幕反光映出周沫侧脸；数字UI简洁；暖环境光；手自然握持手机 |
| **参考Prompt** | Smartphone screen showing livestream viewer count "23" in simple UI, screen reflection showing partial side profile of Chinese woman, warm ambient light from desk lamp, hand holding phone naturally, shallow depth of field, realistic screen glow, low saturation, documentary style, photorealistic, 16:9 |
| **负面Prompt** | bright neon UI, futuristic hologram, oversaturated screen, cartoon interface |
| **角色IP-Adapter** | — |

---

### S05 — 闪回：周沫站在总监办公室门口
| 属性 | 内容 |
|------|------|
| **镜号** | S05 |
| **类型** | T2I |
| **情绪** | 茫然/刺痛 |
| **核心主体** | 周沫站在总监办公室门口，手里捏着工卡，走廊荧光灯冷白 |
| **角色出场** | 周沫 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 闪回标记；办公室走廊冷白荧光灯 vs 出租屋暖黄形成温度对比；工卡捏紧的手部细节 |
| **参考Prompt** | Zhou Mo, 30yo Chinese woman, standing in office corridor outside director's office, holding employee ID card tightly in hand, cold white fluorescent ceiling light, modern tech company hallway, glass walls, her expression blank and lost, documentary style, cool color temperature, photorealistic base with subtle ink wash texture, 16:9 |
| **负面Prompt** | warm lighting, home environment, smiling, vibrant colors, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/周沫/` |

---

### S06 — 总监说出实情
| 属性 | 内容 |
|------|------|
| **镜号** | S06 |
| **类型** | I2V |
| **情绪** | 刺痛/无奈 |
| **核心主体** | 技术总监对周沫说话，办公室走廊，双人中近景 |
| **角色出场** | 技术总监、周沫（背影/侧影） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | I2V关键帧；总监表情疲惫而非冷酷；双人中近景；荧光灯冷调；赵建军式制度冷灰可参考 |
| **参考Prompt** | Chinese office corridor, 45yo tech director in casual shirt T-shirt, tired expression not cruel, speaking to younger woman, fluorescent office lighting, two-shot medium close-up, naturalistic style, cool gray tones, documentary realism, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | villain expression, dramatic lighting, warm tones, cinematic blockbuster style, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/技术总监/` |

---

### S07 — 工牌正面·门禁灯闪红灭掉
| 属性 | 内容 |
|------|------|
| **镜号** | S07 |
| **类型** | T2I |
| **情绪** | 终了/静默 |
| **核心主体** | 工牌正面周沫照片，门禁读卡器红灯闪烁后熄灭 |
| **角色出场** | 周沫（照片） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 特写；照片上的周沫比此刻年轻；红灯闪烁的微妙动态感用静态暗示；塑料工牌磨损痕迹 |
| **参考Prompt** | Employee ID card close-up, photo of young Chinese woman on card, access control reader with red LED light, card slightly worn with scratches, cold office lighting, shallow depth of field, the red light suggesting deactivation, documentary realism, muted colors, photorealistic, 16:9 |
| **负面Prompt** | bright vibrant colors, cartoon ID card, perfect clean card, futuristic hologram |
| **角色IP-Adapter** | — |

---

### S08 — 周沫走出办公楼
| 属性 | 内容 |
|------|------|
| **镜号** | S08 |
| **类型** | I2V |
| **情绪** | 空白/ summer刺眼 |
| **核心主体** | 周沫走出办公楼，上海夏天阳光刺眼，背影中景 |
| **角色出场** | 周沫 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | I2V关键帧；强逆光；背影；办公楼玻璃幕墙反射；夏天热浪空气感 |
| **参考Prompt** | Zhou Mo, 30yo Chinese woman, walking out of modern office building, summer Shanghai, harsh bright sunlight, back view medium shot, glass curtain wall reflections, heat haze in air, overexposed sky, documentary realism, low saturation, photorealistic base with subtle ink wash texture, 16:9 |
| **负面Prompt** | winter, night, front view smiling, cool colors, dramatic sunset, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/周沫/` |

---

### S09 — 周沫在家改简历→投递→无回应
| 属性 | 内容 |
|------|------|
| **镜号** | S09 |
| **类型** | T2I |
| **情绪** | 焦虑/循环 |
| **核心主体** | 周沫坐在电脑前，屏幕显示招聘网站，房间昏暗，外卖盒 |
| **角色出场** | 周沫 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；屏幕光映脸；桌上泡面/外卖盒；简历投递状态"已读未回"；出租屋真实凌乱 |
| **参考Prompt** | Zhou Mo, 30yo Chinese woman, sitting at small desk in dim apartment, computer screen showing job application website, screen light reflecting on her tired face, instant noodle cups and takeout boxes on desk, messy Shanghai rental room, late night atmosphere, documentary realism, low saturation, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | bright clean room, professional home office, smiling, vibrant colors, organized desk |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/周沫/` |

---

### S10 — 送外卖收入与房租账单并排
| 属性 | 内容 |
|------|------|
| **镜号** | S10 |
| **类型** | T2I |
| **情绪** | 压迫/生存 |
| **核心主体** | 手机屏幕：外卖收入数字与房租账单并排显示 |
| **角色出场** | 无 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 特写；两个APP界面并置；数字对比刺眼；屏幕反光隐约映出天花板 |
| **参考Prompt** | Smartphone screen split view, left side showing food delivery app income figures, right side showing rent bill, stark numerical contrast, screen glow in dark room, ceiling reflected faintly on screen, documentary realism, muted colors, photorealistic, 16:9 |
| **负面Prompt** | bright cheerful UI, oversaturated colors, futuristic hologram, cartoon graphics |
| **角色IP-Adapter** | — |

---

### S11 — 周沫拆包裹·小型机器人模型
| 属性 | 内容 |
|------|------|
| **镜号** | S11 |
| **类型** | T2I |
| **情绪** | 微小希望/起点 |
| **核心主体** | 周沫拆开闲鱼包裹，小型机器人模型露出，出租屋日常光 |
| **角色出场** | 周沫 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；拆包裹的日常动作；机器人模型作为直播道具；自然窗光；期待感 |
| **参考Prompt** | Zhou Mo, 30yo Chinese woman, opening cardboard package on small table, small robot model revealed inside, natural window light in Shanghai apartment, casual home clothes, expression of faint curiosity and hope, everyday realism, low saturation, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | professional studio, bright commercial lighting, exaggerated excitement, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/周沫/` |

---

### S12 — 第一次开播
| 属性 | 内容 |
|------|------|
| **镜号** | S12 |
| **类型** | T2I |
| **情绪** | 紧张/起点 |
| **核心主体** | 周沫第一次开播，背景白墙，在线人数显示"3" |
| **角色出场** | 周沫 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 中景；与S02同场景但更早/更简陋；手机支架；紧张的手部姿态；屏幕显示"3人" |
| **参考Prompt** | Zhou Mo, 30yo Chinese woman, sitting in front of plain white wall, first livestream setup with phone on cheap tripod, screen showing viewer count "3", nervous hand gesture, small desk lamp, minimal setup, Shanghai apartment, documentary realism, low saturation, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | professional studio, ring light, confident smile, vibrant colors, multiple cameras |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/周沫/` |

---

### S13 — 周沫深夜备课
| 属性 | 内容 |
|------|------|
| **镜号** | S13 |
| **类型** | T2I |
| **情绪** | 孤独/坚持 |
| **核心主体** | 周沫深夜一个人备课，翻旧书，书脊透明胶粘着 |
| **角色出场** | 周沫 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 近景；书脊透明胶细节；台灯暖光；深夜安静感；旧教材/笔记 |
| **参考Prompt** | Zhou Mo, 30yo Chinese woman, close-up at desk late night, flipping through old textbook with transparent tape on spine, warm desk lamp light on her focused face, worn pages, quiet solitude, Shanghai apartment midnight atmosphere, documentary realism, low saturation, photorealistic base with Chinese ink wash aesthetic, 16:9 |
| **负面Prompt** | bright room, daytime, multiple people, digital tablet, clean new book, smiling |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/周沫/` |

---

### S14 — 弹幕滚动
| 属性 | 内容 |
|------|------|
| **镜号** | S14 |
| **类型** | T2I |
| **情绪** | 温暖/连接 |
| **核心主体** | 屏幕上的弹幕："你讲的不一样""我听懂了" |
| **角色出场** | 无（CG弹幕字形） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 屏幕特写；弹幕字形自然；暖环境光；与S04同场景但情绪反转 |
| **参考Prompt** | Livestream screen close-up, Chinese bullet comments scrolling "你讲的不一样" "我听懂了", warm ambient light from desk lamp, simple clean UI, screen glow in dark room, sense of quiet connection, documentary realism, muted colors, photorealistic, 16:9 |
| **负面Prompt** | neon bright colors, exaggerated animation, cyberpunk UI, overwhelming spam |
| **角色IP-Adapter** | — |

---

### S15 — 周沫微笑眼眶微湿
| 属性 | 内容 |
|------|------|
| **镜号** | S15 |
| **类型** | I2V |
| **情绪** | 坚定/感动 |
| **核心主体** | 周沫近景，微笑，眼眶微湿但不落泪，暖台灯照面 |
| **角色出场** | 周沫 |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | I2V关键帧；核心情感镜头；浅景深；白墙A4纸背景；情绪高点 |
| **参考Prompt** | Zhou Mo, 30yo Chinese woman, close-up portrait, soft smile, eyes glistening but not crying, warm desk lamp light on face, white wall with handwritten papers behind, shallow depth of field, cinematic, low saturation, photorealistic base with Chinese ink wash aesthetic, emotional restraint, dignity, 16:9 |
| **负面Prompt** | tears streaming down, dramatic crying, bright commercial lighting, exaggerated emotion, anime |
| **角色IP-Adapter** | `ASSETS/CHARACTERS/周沫/` |

---

### S16 — 直播间光→窗外上海夜景
| 属性 | 内容 |
|------|------|
| **镜号** | S16 |
| **类型** | T2I |
| **情绪** | 希望/辽阔 |
| **核心主体** | 直播间的光拉远至窗外上海夜景，万家灯火 |
| **角色出场** | 周沫（远景剪影） |
| **尺寸** | 1280×720, 16:9 |
| **技术备注** | 收尾镜；与S01呼应；从室内暖光过渡至城市夜景；拉远镜头；希望感 |
| **参考Prompt** | Shanghai night cityscape, camera pulling back from warm lit window of small apartment to wide city view, silhouette of woman inside, thousands of warm window lights against dark blue sky, distant skyscrapers, atmospheric haze, cinematic wide shot, sense of quiet hope and vastness, low saturation, photorealistic base with subtle ink wash texture, 16:9 |
| **负面Prompt** | oversaturated, neon cyberpunk, futuristic vehicles, dramatic sunset, anime |
| **角色IP-Adapter** | — |

---

## 角色定妆需求清单

| 角色 | 状态 | 优先级 |
|------|------|--------|
| 周沫 | 待建 | **高** — 本集核心角色，需完整定妆规格+IP-Adapter |
| 技术总监 | 待建 | 中 — 仅S06出场，需基础定妆 |

---

## 背景规格需求

| 场景 | 状态 | 说明 |
|------|------|------|
| 上海出租屋直播间 | 待建 | 核心重复场景，白墙+A4纸+小台灯，需统一规格 |
| 写字楼办公室走廊 | 待建 | S05/S06/S07/S08使用，冷白荧光灯 |
| 上海夜景远景 | 待建 | S01/S16使用，可与01_晨钟上海夜景共用 |

---

## 视觉一致性备忘

- **色调**: 出租屋暖黄(2700K) vs 办公室冷白(5000K)，形成温度叙事
- **周沫造型**: 居家便装，素颜略有疲惫，不化妆，不戴首饰
- **A4纸公式**: 手写体，需统一风格，可重复使用同一批 asset
- **时间标记**: 闪回(S05-S08)与现在(S01-S04,S11-S16)通过色温区分