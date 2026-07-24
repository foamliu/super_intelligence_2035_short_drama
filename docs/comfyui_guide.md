# ComfyUI API 批量生成实战心得

> 记录在制作第12集《身体》短剧过程中，使用 ComfyUI REST API 批量生成的踩坑经验与最佳实践。

---

## 1. 核心思路：API JSON + Python 脚本离线批量提交

将 ComfyUI 工作流用 **Save → API Format** 导出为纯 JSON，Python 脚本 `deepcopy` 模板后注入参数（prompt、seed、尺寸、steps 等），POST 到 `http://localhost:8188/prompt`。全程无需操作 UI，可串联批量生成图片和语音：

```python
template = json.load(open("Flux.1 Dev 文生图.json"))
wf = copy.deepcopy(template)
for node_id, node in wf.items():
    if node["class_type"] == "CLIPTextEncode":
        node["inputs"]["text"] = prompt_text
    elif node["class_type"] == "KSampler":
        node["inputs"]["seed"] = random.randint(0, 2**48)

data = json.dumps({"prompt": wf}).encode()
urllib.request.urlopen("http://localhost:8188/prompt", data=data)
```

---

## 2. 导出文件的关键区别

| 导出方式 | 内容 | 适用场景 |
|---------|------|---------|
| **Save (API Format)** | 纯 JSON，无 UI 元数据 | ✅ Python 脚本直接 POST |
| Save | 含 widget_values 等 UI 信息 | 手动复用，脚本需额外清洗 |

**关键**：必须用 API Format 导出！导出路径通常在 `ComfyUI/user/default/workflows/` 或自定义目录。

---

## 3. History 返回格式（重要踩坑）

POST `/prompt` 仅返回 `prompt_id`。需轮询 `/history/{prompt_id}` 获取输出。**返回格式是嵌套字典，不是列表**：

```python
history = json.loads(resp)
outputs = history[prompt_id]["outputs"]  # {node_id: {...}}
```

每个节点的 outputs 结构：

```python
# 图片节点:
{"images": [{"filename": "ComfyUI_temp_00001_.png", "subfolder": "", "type": "temp"}]}

# 音频节点（TTS）:
{"audio": [{"filename": "xxx.flac", "subfolder": "", "type": "output"}]}
```

**正确解析方式**：
```python
for node_id, node_outputs in outputs.items():
    if isinstance(node_outputs, dict):
        items = node_outputs.get("audio",
                 node_outputs.get("images",
                 node_outputs.get("gifs", [])))
    elif isinstance(node_outputs, list):
        items = node_outputs
    else:
        items = []
    for item in items:
        filename = item["filename"]
```

---

## 4. 下载生成文件

通过 `/view` 端点下载，`type` 参数须与 history 返回一致：

```python
url = f"http://localhost:8188/view?filename={filename}&type={folder_type}&subfolder={subfolder}"
urllib.request.urlretrieve(url, dest_path)
```

---

## 5. 模型性能参考

| 引擎 | 耗时/张 | 推荐 Steps | 适用场景 |
|------|---------|-----------|---------|
| Flux.1 Dev | 3-8 分钟 | 20 | 高质量场景图 |
| Z-Image-Turbo | 30-60 秒 | 8 | 快速预览/道具 |
| Qwen3-TTS | 1-2 分钟 | — | 中文旁白语音(FLAC) |

---

## 6. 超时与断点续传策略

- 轮询间隔 5 秒，单任务超时 600 秒
- 顺序提交（一个一个等完成），避免队列拥堵导致后续任务超时
- 每个任务完成后立即下载保存到 `ASSETS/{章节}/`
- 保存 `manifest.json` 记录 prompt_id、状态、文件列表
- 超时任务可手动访问 `/history/{prompt_id}` 下载；或通过 `prompt_id` 直接恢复
- 任务间 `time.sleep(2)` 避免 API 过载

---

## 7. 快速排错清单

| 症状 | 可能原因 | 解决方案 |
|------|---------|---------|
| POST 返回 `node_errors` | 模型未加载/节点缺参数 | 检查 ComfyUI 是否已加载对应模型 |
| History 为空 | 任务未完成 | 增加超时、降低轮询间隔 |
| `AttributeError: 'str' has no 'get'` | outputs 解析格式错误 | 按第 3 节正确格式解析 |
| 超时但实际已完成 | ComfyUI 队列积压 | 手动访问 `/history/{id}` 下载 |
| 下载文件为 0 字节 | `type` 参数错误 | 对照 history 中 `type` 字段 |

---

## 8. TTS 中文旁白注意事项

- 文本不能包含中文弯引号 `""`，建议存为独立 JSON 文件加载
- `instruct` 参数控制语速和情感（如 "Moderate pace, warm and calm tone"）
- 生成格式为 FLAC，最终需转 MP3 用于剪辑