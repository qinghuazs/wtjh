# WYJH ComfyUI Custom Nodes

该工程用于在 ComfyUI 中接入 WYJH 的 API（base URL: https://www.wyjh.top），覆盖以下模型类型：

- 会话模型（Session/Chat）
- 问生图（Text-to-Image）
- 图生图（Image-to-Image）
- 视频模型（Video）
- 千问图像编辑（Qwen Image Edit）
- 图片上传（Image Upload，支持 IMAGE 或本地路径）
- Z-Image-Turbo（Text-to-Image）
- Qwen Image Max（Text-to-Image）
- 腾讯AIGC生图（创建任务 / 查询结果）
- Doubao Seedream 4.0 图生图
- Doubao Seedream 4.5 文生图 / 图文生图 / 多图融合
- Doubao Seedream 4.5 组图输出 / 单张图生组图 / 多参考图生组图
- Gemini 3 Pro Image Preview
- Gemini 2.5 Flash Image（含基础/Preview）
- 文本输入节点
- 图片URL拼接节点（多图顺序输入）

## 项目结构

```
.
├─ __init__.py
├─ config.py
├─ requirements.txt
├─ api/
│  ├─ __init__.py
│  └─ client.py
├─ nodes/
│  ├─ __init__.py
│  ├─ base.py
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ session.py
│  │  ├─ text2img.py
│  │  ├─ img2img.py
│  │  └─ video.py
│  ├─ utils/
│  │  ├─ __init__.py
│  │  ├─ upload.py
│  │  ├─ text_input.py
│  │  └─ image_url_joiner.py
│  └─ models/
│     ├─ __init__.py
│     ├─ qwen/
│     │  ├─ __init__.py
│     │  ├─ qwen_edit.py
│     │  └─ qwen_image_max.py
│     ├─ zimage/
│     │  ├─ __init__.py
│     │  └─ z_image_turbo.py
│     ├─ tencent/
│     │  ├─ __init__.py
│     │  └─ tencent_aigc_image.py
│     ├─ doubao/
│     │  ├─ __init__.py
│     │  ├─ doubao_seedream_4_0_img2img.py
│     │  ├─ doubao_seedream_4_5_txt2img.py
│     │  ├─ doubao_seedream_4_5_img2img.py
│     │  ├─ doubao_seedream_4_5_group_output.py
│     │  ├─ doubao_seedream_4_5_single_to_group.py
│     │  └─ doubao_seedream_4_5_multi_ref_group.py
│     └─ gemini/
│        ├─ __init__.py
│        ├─ gemini_3_pro_image_preview.py
│        ├─ gemini_25_flash_image.py
│        ├─ gemini_25_flash_image_basic.py
│        └─ gemini_25_flash_image_preview.py
├─ utils/
│  ├─ __init__.py
│  ├─ errors.py
│  ├─ http.py
│  ├─ image.py
│  ├─ image_io.py
│  └─ timing.py
└─ README.md
```

## 使用说明

1. 将该目录放到 `ComfyUI/custom_nodes/` 下。
2. 安装依赖：
   ```bash
   python3 -m pip install -r requirements.txt
   ```
3. 通过环境变量覆盖默认配置：

`WYJH_API_KEY`：API 访问密钥（Bearer）

也可以在 `ComfyUI/custom_nodes/wyjh/` 下创建 `.env` 文件，写入：
 
 ```env
 WYJH_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
 ```
 
4. 启动 ComfyUI 后，在节点列表中查找 `WYJH` 分类。

## 开发说明

当前仅搭建了框架与节点入口，具体 API 路径、参数和返回结果需要按接口文档补齐。

下一步建议：
- 确认各模型对应的 API 路径与入参/出参
- 实现图片/视频的编码与解码
- 增加错误处理与重试策略
