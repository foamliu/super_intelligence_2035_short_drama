# 项目经验教训记录

> 本项目在 AI 辅助制作过程中反复踩坑、修坑的完整记录。
> 维护本文件的核心目的：**下次不再犯同样的错误。**

**更新规则**：每踩一次坑，在此文件顶部追加一条，标注编号、日期、犯错的脚本/流程环节。

---

## #7 · 2026-07-28 · AI 助手混淆分镜帧目录 → 误指路径

**环节**：分镜生成后，用户问"分镜在哪"，AI 助手回答时指向了错误的目录。

**错误行为**：
- 分镜帧图片实际在 `OUTPUT/13_外骨骼/frames/`
- AI 助手错误指向 `ASSETS/SHOT_SPECS/`（那是 T2I Prompt 规格文档目录）
- 导致用户困惑，浪费时间纠正

**正确做法**：
- **`ASSETS/SHOT_SPECS/`** = T2I/I2V Prompt 模板 Markdown 文档——**不是图片**
- **`OUTPUT/{章节}/frames/`** = 实际生成的分镜帧图片
- 在回答"XXX 在哪"之前，必须先 `list_files` 确认该目录实际内容
- AI 助手不得凭文件名/路径名"推测"内容，必须亲眼看到文件列表

**约束写入**：`README.md` 已加入项目结构明确说明两个目录的区别。

---

## #6 · 2026-07-28 · 生成分镜时不引用角色定妆照 → 白做定妆

**环节**：T2I 分镜生成脚本 `generate_ep13_t2i.py`

**错误行为**：
- 角色定妆照已存入 `ASSETS/CHARACTERS/08_莎拉·赵/主定妆照.png`
- 生成分镜脚本时仅使用 Z-Image-Turbo 纯文生图
- 没有引用定妆照作为 LongCat Image Edit 的输入图
- 导致莎拉每张脸随机变化——定妆照片做了

**根因**：生成脚本没有"角色路由"逻辑——不知道哪些镜头需要引用谁的定妆照。

**正确做法**：
- 需要角色一致性的镜头 → **LongCat Image Edit**（workflow: `Image Edit (LongCat Image Edit).json`），以定妆照为 LoadImage 输入 + 场景 Prompt
- 不需要角色一致性的镜头（场景、道具、UI、群像）→ Z-Image-Turbo 纯 T2I
- 脚本必须维护 `CHARACTER_REF_MAP`（镜头名前缀 → 定妆照路径），自动判断路由

**已修复**：`scripts/generate_ep13_t2i.py` 已改造，新增 `get_character_ref()` 函数和双 workflow 构建逻辑。

**约束写入**：README §五 "角色一致性技术路线" 已明确"所有人物镜头必须引用定妆照"。

---

## #5 · 2026-07-28 · 生成脚本仅覆盖当前章节，缺乏扩展性

**环节**：`scripts/generate_ep13_t2i.py` 及同模式脚本

**问题**：
- 脚本硬编码当前章节（13_外骨骼），无法复用于其他章节
- 其他章节（14_副作用、15_南山台…）需要从头复制改写
- 每个章节的生成脚本如果都是"一次性"，维护成本会指数增长

**改进建议**（待实施）：
- 抽象通用的 `generate_chapter_t2i.py`，接受 `--chapter` 参数自动定位对应的分镜规格文件
- 角色定妆照映射独立为配置文件（`ASSETS/CHARACTERS/character_ref_map.json`），不是硬编码在脚本中
- 通用化后应支持：`python scripts/generate_chapter_t2i.py --chapter 14`

---

## #4 · 2026-07-28 · AI 助手回答未使用工具 → 违反工具调用规则

**环节**：AI 助手在对话中未使用工具而直接回复文本。

**根因**：AI 助手在不确认事实的情况下凭记忆/推理回答了问题（指向错误目录），系统要求必须先使用工具（如 `list_files`）验证路径。

**约束**：
- 回答"XXX 在哪"类型的路径问题时，**必须先 `list_files` 验证目录实际内容**
- 回答"XXX 是什么"类型的问题时，**必须先 `read_file` 确认文件实际内容**
- 不得凭文件名/路径名推测文件用途

---

## #3 · 2026-07-28 · Powerline 字体在 Windows 环境下的终端兼容性问题

**环节**：首次安装配置星云的 PowerShell 环境

**问题**：
- 使用 Powerline 特殊字符的 Oh My Posh 主题在 Windows Terminal / VS Code 集成终端中显示乱码或方块
- CaskaydiaCove Nerd Font 未安装时，prompt 显示为缺省字符

**解决方案**：
- 从 Nerd Fonts 官方 Release 下载 `CaskaydiaCove` Nerd Font 并安装
- VS Code: `"terminal.integrated.fontFamily": "CaskaydiaCove NF"`
- Windows Terminal: 对应 Profile 的 Appearance → Font face 设为 `CaskaydiaCove NF Mono`

---

## #2 · 2026-07-21 · Git 提交时 .gitignore 未覆盖生成物目录

**环节**：Git 初始化项目仓库

**问题**：
- `.gitignore` 创建后，之前 Track 的文件（如 OUTPUT/、ASSETS/*/）仍然被 Git 追踪
- 新增的生成目录（如 OUTPUT/13_外骨骼/）在 .gitignore 后仍出现在 `git status` 中

**正确做法**：
- `.gitignore` 修改后，必须先 `git rm --cached` 已追踪的文件，再检查 `git status`
- 生成物目录（OUTPUT/、ASSETS/*/图片、ASSETS/生成素材…）必须用具体通配符覆盖，不要依赖".gitignore 会自动生效"的假设

---

## #1 · 2026-07-20 · 书稿章节 renumbering 导致 BOOK/ 下文档引用失效

**环节**：书稿章节从 X 章重新编号为 Y 章

**问题**：
- `BOOK/profiles.md`、`BOOK/timeline_analysis.md`、`BOOK/glossary.md` 等多处包含对"第 X 章"的交叉引用
- 单一更改章节编号后，所有引用章节号的 .md 文件均失效
- 人工逐一手动修正费时且易遗漏

**解决方案**：
- 运行 `BOOK/fix_quotes.py` 脚本批量替换所有 .md 文件中的章节编号引用
- 脚本用映射字典 `{"第X章": "第Y章", ...}` 执行全文正则替换
- 运行后需全文检查 `grep -rn "第X章" BOOK/`，确认旧编号已清零

---

## 模板：新踩坑记录格式

```markdown
## #N · YYYY-MM-DD · 一句话概括问题

**环节**：[脚本/流程/工具名称]

**错误行为**：
- [具体做了什么错事]

**根因**：
- [为什么错了]

**正确做法 / 解决方案**：
- [应该怎么做]

**已修复**（如适用）：[修复链接/commit/文件变更]