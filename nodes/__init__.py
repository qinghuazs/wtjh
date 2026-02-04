"""Node registration for ComfyUI."""

from .session import WyjhSessionChat
from .text2img import WyjhText2Image
from .img2img import WyjhImage2Image
from .video import WyjhVideoGenerate
from .qwen_edit import WyjhQwenImageEdit
from .upload import WyjhImageUpload, WyjhLocalImageUpload
from .z_image_turbo import WyjhZImageTurbo
from .qwen_image_max import WyjhQwenImageMax
from .tencent_aigc_image import WyjhTencentAigcImageCreate, WyjhTencentAigcImageQuery
from .doubao_seedream_4_0_img2img import WyjhDoubaoSeedream40Img2Img
from .doubao_seedream_4_5_txt2img import WyjhDoubaoSeedream45Txt2Img
from .doubao_seedream_4_5_img2img import (
    WyjhDoubaoSeedream45Img2Img,
    WyjhDoubaoSeedream45MultiFusion,
)
from .gemini_3_pro_image_preview import WyjhGemini3ProImagePreview
from .gemini_25_flash_image import WyjhGemini25FlashImage
from .gemini_25_flash_image_basic import WyjhGemini25FlashImageBasic
from .gemini_25_flash_image_preview import WyjhGemini25FlashImagePreview
from .text_input import WyjhTextInput


NODE_CLASS_MAPPINGS = {
    "WYJH Session Chat": WyjhSessionChat,
    "WYJH Text2Image": WyjhText2Image,
    "WYJH Image2Image": WyjhImage2Image,
    "WYJH Video": WyjhVideoGenerate,
    "WYJH Qwen Image Edit": WyjhQwenImageEdit,
    "WYJH Image Upload": WyjhImageUpload,
    "WYJH Local Image Upload": WyjhLocalImageUpload,
    "WYJH Z-Image-Turbo": WyjhZImageTurbo,
    "WYJH Qwen Image Max": WyjhQwenImageMax,
    "WYJH Tencent AIGC Create": WyjhTencentAigcImageCreate,
    "WYJH Tencent AIGC Query": WyjhTencentAigcImageQuery,
    "WYJH Doubao Seedream 4.0 Img2Img": WyjhDoubaoSeedream40Img2Img,
    "WYJH Doubao Seedream 4.5 Txt2Img": WyjhDoubaoSeedream45Txt2Img,
    "WYJH Doubao Seedream 4.5 Img2Img": WyjhDoubaoSeedream45Img2Img,
    "WYJH Doubao Seedream 4.5 Multi Fusion": WyjhDoubaoSeedream45MultiFusion,
    "WYJH Gemini 3 Pro Image Preview": WyjhGemini3ProImagePreview,
    "WYJH Gemini 2.5 Flash Image": WyjhGemini25FlashImage,
    "WYJH Gemini 2.5 Flash Image Basic": WyjhGemini25FlashImageBasic,
    "WYJH Gemini 2.5 Flash Image Preview": WyjhGemini25FlashImagePreview,
    "WYJH Text Input": WyjhTextInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WYJH Session Chat": "WYJH · 会话",
    "WYJH Text2Image": "WYJH · 问生图",
    "WYJH Image2Image": "WYJH · 图生图",
    "WYJH Video": "WYJH · 视频",
    "WYJH Qwen Image Edit": "WYJH · 千问图像编辑",
    "WYJH Image Upload": "WYJH · 图片上传",
    "WYJH Local Image Upload": "WYJH · 本地图片上传",
    "WYJH Z-Image-Turbo": "WYJH · Z-Image-Turbo",
    "WYJH Qwen Image Max": "WYJH · Qwen Image Max",
    "WYJH Tencent AIGC Create": "WYJH · 腾讯AIGC生图(创建)",
    "WYJH Tencent AIGC Query": "WYJH · 腾讯AIGC生图(查询)",
    "WYJH Doubao Seedream 4.0 Img2Img": "WYJH · Doubao Seedream 4.0 图生图",
    "WYJH Doubao Seedream 4.5 Txt2Img": "WYJH · Doubao Seedream 4.5 文生图",
    "WYJH Doubao Seedream 4.5 Img2Img": "WYJH · Doubao Seedream 4.5 图文生图",
    "WYJH Doubao Seedream 4.5 Multi Fusion": "WYJH · Doubao Seedream 4.5 多图融合",
    "WYJH Gemini 3 Pro Image Preview": "WYJH · Gemini 3 Pro Image Preview",
    "WYJH Gemini 2.5 Flash Image": "WYJH · Gemini 2.5 Flash Image",
    "WYJH Gemini 2.5 Flash Image Basic": "WYJH · Gemini 2.5 Flash Image（基础）",
    "WYJH Gemini 2.5 Flash Image Preview": "WYJH · Gemini 2.5 Flash Image Preview",
    "WYJH Text Input": "WYJH · 文本输入",
}
