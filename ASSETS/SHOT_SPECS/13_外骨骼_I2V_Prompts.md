# 第13集《外骨骼》— I2V/T2V 视频生成 Prompt 规格

> **🎯 首选模型**：`workflows/video_minimax_h3_i2v.json`（Minimax H3 Image to Video，质量最高）
> **备选 Workflow**：`workflows/Wan 2.2 图生视频.json`（国产）和 `workflows/Image to Video (LTX-2.3).json`（最后备选）
> **输入图像来源**：`ASSETS/SHOT_SPECS/13_外骨骼_T2I_Prompts.md` 生成的静态图
> **输出分辨率**：Minimax H3: 最高 1280×720 @ 24fps | Wan 2.2: 640×640 @ 16fps | LTX-2.3: 1280×720 @ 25fps（仅备选）
> **视频时长**：每个镜头 5-10 秒
> **⚠️ 模型策略**：**任何情况下优先使用 Minimax H3（I2V/R2V）**。Wan 2.2 作为国产备选，LTX-2.3 仅作最后的备选方案。

---

## Workflow 使用策略（Minimax H3 优先）

| Workflow | 适用场景 | 优势 | 限制 |
|----------|---------|------|------|
| **Minimax H3 I2V** | 人物表演、微表情、对话镜头（**首选**） | 画面质量最高，角色一致性最好 | 需 Int8 量化 UNet |
| **Minimax H3 R2V** | 需要多张参考图保持角色一致性 | 支持 ref_image_0 + ref_image_1 | 需 ref2va UNet |
| **Wan 2.2 I2V** | 国产备选——人物表演 | 动作自然度不错 | 640×640，需后期放大 |
| **LTX-2.3 I2V** | 仅作最后备选——屏幕内容/UI动画 | 1280×720 | 质量不如 Minimax H3/Wan |

---

## 🎵 音频生成策略（三层混合）

H3 是视频+音频联合生成模型，一次推理同时输出画面和环境音。推荐分层：

| 层次 | 工具 | 策略 |
|:----:|------|------|
| 🎬 环境音/氛围 | **Minimax H3 内建音频 VAE** | prompt 中描述环境音，H3 天然音画同步 |
| 🎙️ 角色配音 | **Qwen3-TTS** | `seed` 锁定音色，跨集一致 |
| 🎵 配乐 BGM | **ACE-Step 1.5** | 结构化 `[Verse][Chorus]` 控制情绪弧线 |

> 后期混音：H3 环境音轨 + TTS 配音轨 + ACE 配乐轨 → 剪辑软件三层合成

---

## 各镜头 Workflow 推荐

| 镜头 | 推荐 Workflow | 原因 |
|------|--------------|------|
| 镜头01·莎拉解释外骨骼 | **Minimax H3 I2V** | 人物表演+双屏内容，全片核心 |
| 镜头02·外骨骼UI慢推 | LTX-2.3 I2V | 屏幕内容动态 |
| 镜头03·师兄"合法吗" | **Minimax H3 I2V** | 人物对话表演 |
| 镜头04·2017实验室闪回 | LTX-2.3 I2V | 氛围镜头 |
| 镜头05·地铁车厢群像 | LTX-2.3 I2V | 群像微动作 |
| 镜头06·莎拉地铁观察 | **Minimax H3 I2V** | 人物微表演 |
| 镜头07·虚拟观众脸 | LTX-2.3 I2V | AI渲染脸，全片视觉心脏 |
| 镜头08·渲染vs真实 | LTX-2.3 I2V | 上下双联 |
| 镜头09·笔记本慢推 | LTX-2.3 I2V | 微距物体 |
| 镜头10·微信十秒沉默 | LTX-2.3 I2V | 手机屏幕动画 |
| 镜头11·吧台散场0.52 | **Minimax H3 I2V** | 人物情感表演，全片情感落点 |
| 镜头12·双标注UI概念 | LTX-2.3 T2V | UI概念动画 |

---

## 制作优先级

| 优先级 | 镜头 | Workflow | 时长 |
|--------|------|----------|------|
| **P0** | 镜头01·莎拉解释外骨骼 | Minimax H3 I2V | 10s |
| **P0** | 镜头07·虚拟观众脸在笑 | LTX-2.3 I2V | 6s |
| **P0** | 镜头08·渲染vs真实 | LTX-2.3 I2V | 8s |
| **P0** | 镜头11·吧台收林薇0.52 | Minimax H3 I2V | 10s |
| P1 | 镜头06·莎拉地铁观察 | Minimax H3 I2V | 8s |
| P1 | 镜头03·师兄"合法吗" | Minimax H3 I2V | 7s |
| P1 | 镜头10·微信十秒沉默 | LTX-2.3 I2V | 10s |
| P2 | 镜头02·外骨骼UI慢推 | LTX-2.3 I2V | 8s |
| P2 | 镜头04·2017实验室闪回 | LTX-2.3 I2V | 8s |
| P2 | 镜头05·地铁车厢群像 | LTX-2.3 I2V | 8s |
| P3 | 镜头12·双标注UI概念 | LTX-2.3 T2V | 8s |
| P3 | 镜头09·笔记本慢推 | LTX-2.3 I2V | 7s |

---

## 文件命名规范

```
13_{内容}_{简短描述}.mp4

表演: 13_sarah_desk_explaining_exoskeleton.mp4
      13_sarah_subway_observing.mp4
      13_sarah_bar_052_aftermath.mp4
      13_shixiong_coffee_heshi_ma.mp4

核心: 13_virtual_face_082_laughing.mp4
      13_render_vs_real_fade.mp4

场景: 13_office_exoskeleton_ui_push.mp4
      13_lab_2017_night_coffee_steam.mp4
      13_subway_rush_hour_commute.mp4

道具: 13_notebook_untransferable_push.mp4
      13_wechat_typing_hao.mp4

UI:   13_ui_double_annotation_xiaozhou.mp4
```

> **详见**：完整的 Prompt 文本请参考关联文件或已生成的 `OUTPUT/13_外骨骼/logs/*_params.json`。