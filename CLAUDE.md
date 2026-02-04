# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 语言要求

对话和思考时使用中文。

## 项目概述

这是一个 ComfyUI 自定义节点插件，用于接入 WYJH API（base URL: https://www.wyjh.top）。支持的模型类型包括：会话、问生图、图生图、视频生成、千问图像编辑、图片上传。

## 开发命令

```bash
# 安装依赖
pip install -r requirements.txt

# 使用方式：将此目录放到 ComfyUI/custom_nodes/ 下，启动 ComfyUI 即可
```

## 环境变量配置

- `WYJH_BASE_URL` - API 基础地址（默认 https://www.wyjh.top）
- `WYJH_TIMEOUT` - 请求超时秒数（默认 60）
- `WYJH_API_KEY` - API 访问密钥（Bearer 认证）
- `WYJH_IMAGE_UPLOAD_URL` - 图床上传接口

## 架构说明

### 入口与节点注册

- `__init__.py` - ComfyUI 入口，导出 `NODE_CLASS_MAPPINGS` 和 `NODE_DISPLAY_NAME_MAPPINGS`
- `nodes/__init__.py` - 节点注册表，所有节点类在此映射到显示名称

### 节点实现模式

所有节点继承 `nodes/base.py:BaseWyjhNode`，该基类：
- 设置 `CATEGORY = "WYJH"`
- 初始化 `WyjhApiClient` 实例
- 提供 `call(path, payload)` 方法封装 POST 请求

节点类需实现：
- `INPUT_TYPES()` - 类方法，定义输入参数
- `RETURN_TYPES` - 输出类型元组
- `FUNCTION` - 执行方法名
- 实际执行方法（如 `generate`、`edit`）

### API 客户端

`api/client.py:WyjhApiClient` 封装 HTTP 请求：
- 自动从 `config.py` 读取配置
- 支持 Bearer 认证
- 提供 `get()` 和 `post()` 方法

### 图像转换

`utils/image.py` 提供 PIL ↔ tensor 转换：
- `pil_to_tensor()` - PIL 图像转 numpy 数组（float32, 0-1）
- `tensor_to_pil()` - tensor/ndarray 转 PIL 图像

## 命名规范

- 类名：`PascalCase`（如 `WyjhText2Image`）
- 函数/变量：`snake_case`
- 节点键名：人类可读字符串（如 `"WYJH Text2Image"`）
