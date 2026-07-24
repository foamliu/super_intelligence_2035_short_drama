# ComfyUI 蓝图工具适配分析 —— 《超级智能2035》短剧制作

> 编写日期：2026-07-23 | 对照来源：ComfyUI 官方 built-in blueprints 列表 (2026-06 ~ 2026-07)

---

## 一、已有 Workflow 盘点

当前 `workflows/` 目录下已部署 14 个 workflow：

| 类别 | 已有 Workflow | 对应功能 |
|------|-------------|---------|
| 文生图 | `Z-Image-Turbo 文生图.json`、`Flux.1 Dev 文生图.json` | 角色/场景概念图生成 |
| 图编辑 | `Image Edit (LongCat Image Edit).json` | 图像局部修改 |
| 姿态→图像 | `Pose to Image (Z-Image-Turbo).json` | 角色姿态控制生成 |
| 图像→姿态 | `Image to Pose Map (SDPose Multi-Person).json` | 多人姿态提取 |
| 图像分割 | `Image Segmentation (SAM3).json` | 前景/背景分离 |
| 图像→3D | `Image to Model (Hunyuan3d 2.1).json` (×2) | 3D资产生成 |
| 文生视频 | `Text to Video (LTX-2.3).json` | 文本→视频 |
| 图生视频 | `Image to Video (LTX-2.3).json`、`Wan 2.2 图生视频.json` | 图像→视频 |
| 语音合成 | `Qwen3-TTS 语音合成.json` | TTS旁白/对白 |
| 语音识别 | `Qwen3-ASR 语音识别.json` | ASR转写 |
| 音频生成 | `ACE-Step 1.5 文生音频.json` | 配乐/环境音生成 |

---

## 二、蓝图列表对照：缺失但强烈建议引入的工具

以下按 **短剧管线实际需要** 与蓝图列表逐一对照，标注优先级。

### 🔴 P0 — 立即引入（直接阻塞当前制作流程）

| 蓝图名称 | 对应功能 | 在你的管线中的用途 | 理由 |
|---------|---------|------------------|------|
| **Remove Background (BiRefNet)** | AI抠图/去背景 | 角色定妆图去背景 → 与场景合成；分屏画面中角色图层分离 | 当前没有抠图工具。分屏合成、角色+场景合成均需此步骤。这是**最高优先级缺失工具**。 |
| **Image Upscale (Z-Image-Turbo)** | 图像超分辨率放大 | 所有AI生成图的最终输出放大（从生成分辨率→制作分辨率） | AI生图默认分辨率通常不足以直接用于后期。必须放大。 |
| **Merge Videos** | 视频拼接合并 | 将多个分镜片段合并为完整一集 | 当前无视频拼接工具，合成需外部完成。 |
| **Color Balance** + **Color Curves** | 色彩平衡 + 曲线调色 | 统一各分镜色彩风格、确保"半写实半水墨"视觉规范落地 | 跨分镜色彩一致性是短剧视觉质量的底线。 |

### 🟡 P1 — 本迭代引入（显著提升效率）

| 蓝图名称 | 对应功能 | 在你的管线中的用途 | 理由 |
|---------|---------|------------------|------|
| **Image to Layers (Qwen-Image-Layered)** | 图像自动分层（前景/中景/背景） | 场景图分层 → 便于分屏构图中独立控制各层 | SAM3 只能做分割，此工具做结构化分层，更适合分屏合成。 |
| **ControlNet (Z-Image-Turbo)** | 受控文生图（基于参考图结构） | 角色一致性生成——用定妆图作为 ControlNet 输入，确保跨集角色外观稳定 | 角色跨集一致性是最大痛点，ControlNet 是最高效的解决路径。 |
| **Canny to Image (Z-Image-Turbo)** | 线稿→图像生成 | 用分镜线稿/草图精确控制画面构图 | 适合需要严格控制构图的镜头（如多人对峙、分屏布局）。 |
| **Depth to Image (Z-Image-Turbo)** | 深度图→图像生成 | 基于深度信息生成场景，控制空间关系 | 适合复杂空间场景（如第16集三江分屏、第28集教堂/婚礼） |
| **First-Last-Frame to Video (LTX-2.3)** | 首尾帧控制视频生成 | 提供首帧+尾帧，生成中间过渡动画 | 精确控制镜头起止帧 → 大幅提升分镜转视频的可控性 |
| **Video Upscale (GAN x4)** | 视频超分辨率放大 | AI生成视频的最终输出放大 | 视频超分是制作收尾的必备步骤 |
| **Frame Interpolation** | 帧插值（补帧） | 提升视频流畅度、创建慢动作效果 | AI视频常帧率不足，补帧可大幅提升观感 |
| **Prompt Enhance** | 提示词自动优化 | 提升文生图/文生视频提示词质量 | 减少人工反复调试提示词的时间 |

### 🟢 P2 — 后续迭代引入（锦上添花）

| 蓝图名称 | 对应功能 | 潜在用途 |
|---------|---------|---------|
| **Film Grain** | 胶片颗粒效果 | 为特定段落（如第15集南山台、第27集景山的历史段落）增加质感 |
| **Chromatic Aberration** | 色差/色散效果 | AR界面、屏幕显示、故障效果（墨子界面、数据污染段落） |
| **Glow** | 发光效果 | 屏幕光、数据流、墨子"觉醒"时刻的视觉强调 |
| **Image Inpainting (Flux.1 Fill Dev)** | 图像局部修补 | 修复生成图中的瑕疵区域 |
| **Video Inpainting (Wan2.1 VACE)** | 视频局部修补 | 修复生成视频中的闪烁/畸变 |
| **Video Depth Estimation (Depth Anything 3)** | 视频深度估计 | 为视频添加景深效果、空间合成 |
| **Image Depth Estimation (Depth Anything 3)** | 图像深度估计 | 替代/补充 MoGe，获取更精确深度信息 |
| **Image Captioning (gemini)** | 图像自动描述 | 批量生成已有参考图的描述 → 建立视觉资产元数据库 |
| **Get Any Video Frame** | 提取视频任意帧 | 从参考视频中提取关键帧作为生成素材 |
| **Video Stitch** | 视频拼接（带转场） | 比 Merge Videos 更高级，支持转场效果 |
| **Select Per-Line Text by Index** | 按行索引提取文本 | 批量处理分镜脚本文本 → 自动化提取提示词 |
| **Image Face Detection (Mediapipe)** | 人脸检测 | 角色定妆图质量检查——确保面部可见、无畸变 |
| **Geometry Estimation (MoGe)** | 单图几何估计 | 场景空间的3D理解 → 辅助构图 |
| **Image to Gaussian Splat (TripoSplat)** | 图像→高斯泼溅 | 高精度场景重建 → 自由视角渲染 |
| **Image to Model (Hunyuan3d 2.1)** | 已有 | 3D资产已覆盖 |

---

## 三、按短剧制作阶段映射

```
[前期资产] ──→ [分镜生成] ──→ [动画生成] ──→ [合成后期] ──→ [成品输出]

前期资产:
  ✅ Z-Image-Turbo 文生图 (已有)
  ✅ Flux.1 Dev 文生图 (已有)
  🆕 ControlNet (Z-Image-Turbo) ← P1 引入，角色一致性
  🆕 Image Upscale (Z-Image-Turbo) ← P0 引入

分镜生成:
  ✅ Pose to Image (已有)
  ✅ Image to Pose Map (已有)
  🆕 Canny to Image ← P1 引入，精确构图
  🆕 Depth to Image ← P1 引入，空间控制
  🆕 Remove Background (BiRefNet) ← P0 引入，角色/场景合成

动画生成:
  ✅ Text to Video (LTX-2.3) (已有)
  ✅ Image to Video (LTX-2.3) (已有)
  ✅ Wan 2.2 图生视频 (已有)
  🆕 First-Last-Frame to Video ← P1 引入，可控视频
  🆕 Frame Interpolation ← P1 引入，补帧
  🆕 Prompt Enhance ← P1 引入，提示词优化

合成后期:
  ✅ Image Edit (LongCat) (已有)
  ✅ Image Segmentation (SAM3) (已有)
  🆕 Image to Layers (Qwen-Image-Layered) ← P1 引入，分屏合成
  🆕 Color Balance + Color Curves ← P0 引入，色彩统一
  🆕 Merge Videos ← P0 引入，分镜合并
  🆕 Video Upscale (GAN x4) ← P1 引入

成品输出:
  🆕 Video Stitch ← P2
  🆕 Film Grain ← P2
  🆕 Chromatic Aberration ← P2
```

---

## 四、与分屏实现指南的对照

`docs/split_screen_implementation_guide.md` 中推荐的三种技术路径，在新引入蓝图后的更新：

| 分屏技术 | 原有依赖 | 新蓝图增强 |
|---------|---------|-----------|
| **后期合成（Premiere/AE）** | 单镜头分别渲染+手动合成 | `Remove Background` 自动抠图 → `Image to Layers` 自动分层 → 合成效率 3× 提升 |
| **ComfyUI 构图** | 一次性生成完整分屏画面 | `ControlNet` + `Canny to Image` 精确控制分屏位置 → 无需后期拆分 |
| **混合方案** | 主要元素AI生成 + 次要元素后期叠加 | `Remove Background` + `Image Upscale` 自动化预处理 → 降低人工操作量 |

---

## 五、如何在 ComfyUI 中使用这些蓝图

**这些蓝图已内置于 ComfyUI 桌面应用，无需手动下载 JSON 文件。**

操作步骤：
1. 打开 ComfyUI 桌面版
2. 点击左侧边栏 **Blueprint**（蓝图）标签
3. 在搜索框中输入蓝图名称（如 `Remove Background`）
4. 点击搜索结果中的蓝图卡片 → 自动在画布中创建完整 workflow
5. 连接输入/输出节点即可使用

无需从 GitHub 手动下载任何 JSON 文件。

---

## 六、建议的引入顺序

```
Week 1 (P0):
  ├── Remove Background (BiRefNet)      ← 角色定妆 → 场景合成
  ├── Image Upscale (Z-Image-Turbo)     ← 所有资产超分
  ├── Merge Videos                      ← 首集合成验证
  └── Color Balance + Color Curves      ← 色彩统一框架

Week 2 (P1):
  ├── ControlNet (Z-Image-Turbo)        ← 角色一致性
  ├── Canny to Image + Depth to Image   ← 精确构图
  ├── First-Last-Frame to Video         ← 可控动画
  ├── Image to Layers (Qwen)            ← 分屏分层
  ├── Frame Interpolation               ← 视频流畅度
  ├── Video Upscale (GAN x4)            ← 视频成品超分
  └── Prompt Enhance                    ← 提示词效率

Week 3+ (P2):
  按需引入 Film Grain、Chromatic Aberration、Video Inpainting 等
```

---

## 六、总结

对照 ComfyUI 官方蓝图列表，你的 `workflows/` 目录目前覆盖了**基础生成能力**（文生图、图生视频、语音合成），但缺少**生产管线中游和下游**的关键工具——尤其是**抠图去背景、图像超分、色彩统一、视频合并**这四个直接阻塞当前流程的工具。

**建议立即引入的 P0 工具（4个）：** Remove Background、Image Upscale、Merge Videos、Color Balance + Color Curves

**本周内引入的 P1 工具（8个）：** ControlNet、Canny to Image、Depth to Image、First-Last-Frame to Video、Image to Layers、Frame Interpolation、Video Upscale、Prompt Enhance

引入后，你的 ComfyUI 管线将覆盖从「概念图生成」到「成品视频输出」的完整链路。