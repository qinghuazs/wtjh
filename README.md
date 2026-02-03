# WYJH ComfyUI Custom Nodes

该工程用于在 ComfyUI 中接入 WYJH 的 API（base URL: https://www.wyjh.top），覆盖以下模型类型：

- 会话模型（Session/Chat）
- 问生图（Text-to-Image）
- 图生图（Image-to-Image）
- 视频模型（Video）

## 项目结构

```
.
├─ __init__.py
├─ config.py
├─ api/
│  ├─ __init__.py
│  └─ client.py
├─ nodes/
│  ├─ __init__.py
│  ├─ base.py
│  ├─ session.py
│  ├─ text2img.py
│  ├─ img2img.py
│  └─ video.py
├─ utils/
│  ├─ __init__.py
│  ├─ errors.py
│  ├─ http.py
│  └─ image.py
└─ README.md
```

## 使用说明

1. 将该目录放到 `ComfyUI/custom_nodes/` 下。
2. 通过环境变量覆盖默认配置：
   - `WYJH_BASE_URL`：API base url
   - `WYJH_TIMEOUT`：超时时间（秒）
3. 启动 ComfyUI 后，在节点列表中查找 `WYJH` 分类。

## 开发说明

当前仅搭建了框架与节点入口，具体 API 路径、参数和返回结果需要按接口文档补齐。

下一步建议：
- 确认各模型对应的 API 路径与入参/出参
- 实现图片/视频的编码与解码
- 增加错误处理与重试策略
