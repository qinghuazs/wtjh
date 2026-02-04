"""Node registration for ComfyUI."""

from .session import WyjhSessionChat
from .text2img import WyjhText2Image
from .img2img import WyjhImage2Image
from .video import WyjhVideoGenerate
from .qwen_edit import WyjhQwenImageEdit
from .upload import WyjhImageUpload


NODE_CLASS_MAPPINGS = {
    "WYJH Session Chat": WyjhSessionChat,
    "WYJH Text2Image": WyjhText2Image,
    "WYJH Image2Image": WyjhImage2Image,
    "WYJH Video": WyjhVideoGenerate,
    "WYJH Qwen Image Edit": WyjhQwenImageEdit,
    "WYJH Image Upload": WyjhImageUpload,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WYJH Session Chat": "WYJH · 会话",
    "WYJH Text2Image": "WYJH · 问生图",
    "WYJH Image2Image": "WYJH · 图生图",
    "WYJH Video": "WYJH · 视频",
    "WYJH Qwen Image Edit": "WYJH · 千问图像编辑",
    "WYJH Image Upload": "WYJH · 图片上传",
}
