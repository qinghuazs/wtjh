"""Tencent AIGC image task nodes."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from .base import BaseWyjhNode
from ..config import get_ssl_verify
from ..utils.image_io import download_image, pil_to_tensor
from ..utils.timing import time_block


class WyjhTencentAigcImageCreate(BaseWyjhNode):
    """Create Tencent AIGC image generation task."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": ("STRING", {"default": "GEM"}),
                "model_version": ("STRING", {"default": "3.0"}),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "file_type": ("STRING", {"default": "File"}),
                "file_id": ("STRING", {"default": ""}),
                "file_url": ("STRING", {"default": ""}),
                "file_text": ("STRING", {"default": ""}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "enhance_prompt": ("STRING", {"default": "Enabled"}),
                "storage_mode": ("STRING", {"default": "Temporary"}),
                "resolution": ("STRING", {"default": "1080P"}),
                "aspect_ratio": ("STRING", {"default": "1:1"}),
                "person_generation": ("STRING", {"default": "AllowAdult"}),
                "input_compliance_check": ("STRING", {"default": "Enabled"}),
                "output_compliance_check": ("STRING", {"default": "Enabled"}),
                "session_id": ("STRING", {"default": ""}),
                "session_context": ("STRING", {"default": ""}),
                "tasks_priority": ("INT", {"default": 0, "min": -10, "max": 10, "step": 1}),
                "ext_info": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("task_id", "request_id")
    FUNCTION = "create_task"
    CATEGORY = "WYJH/TencentAIGC"

    def create_task(
        self,
        model_name: str,
        model_version: str,
        prompt: str,
        file_type: str = "File",
        file_id: str = "",
        file_url: str = "",
        file_text: str = "",
        negative_prompt: str = "",
        enhance_prompt: str = "Enabled",
        storage_mode: str = "Temporary",
        resolution: str = "1080P",
        aspect_ratio: str = "1:1",
        person_generation: str = "AllowAdult",
        input_compliance_check: str = "Enabled",
        output_compliance_check: str = "Enabled",
        session_id: str = "",
        session_context: str = "",
        tasks_priority: int = 0,
        ext_info: str = "",
    ) -> Tuple[str, str]:
        with time_block("WYJH Tencent AIGC Create"):
            file_infos = []
            if file_type or file_id or file_url or file_text:
                file_infos.append(
                    {
                        "type": file_type,
                        "file_id": file_id,
                        "url": file_url,
                        "text": file_text,
                    }
                )

            payload: Dict[str, Any] = {
                "model_name": model_name,
                "model_version": model_version,
                "file_infos": file_infos,
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "enhance_prompt": enhance_prompt,
                "output_config": {
                    "storage_mode": storage_mode,
                    "resolution": resolution,
                    "aspect_ratio": aspect_ratio,
                    "person_generation": person_generation,
                    "input_compliance_check": input_compliance_check,
                    "output_compliance_check": output_compliance_check,
                },
                "session_id": session_id,
                "session_context": session_context,
                "tasks_priority": tasks_priority,
                "ext_info": ext_info,
            }

            response = self.call("/tencent-vod/v1/aigc-image", payload)
            data = response.get("Response", {}) if isinstance(response, dict) else {}
            task_id = data.get("TaskId", "")
            request_id = data.get("RequestId", "")
            return (task_id, request_id)


class WyjhTencentAigcImageQuery(BaseWyjhNode):
    """Query Tencent AIGC image task result."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "task_id": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "status", "file_url")
    FUNCTION = "query"
    CATEGORY = "WYJH/TencentAIGC"

    def query(self, task_id: str):
        with time_block("WYJH Tencent AIGC Query"):
            if not task_id:
                raise ValueError("task_id is required")
            response = self.get(f"/tencent-vod/v1/query/{task_id}")
            data = response.get("Response", {}) if isinstance(response, dict) else {}
            status = data.get("Status", "")
            output = data.get("Output", {}) if isinstance(data, dict) else {}
            file_infos = output.get("FileInfos", []) if isinstance(output, dict) else []
            file_url = ""
            if isinstance(file_infos, list) and file_infos:
                first = file_infos[0]
                if isinstance(first, dict):
                    file_url = first.get("FileUrl", "") or first.get("Url", "")

            if status != "FINISH" or not file_url:
                progress = data.get("Progress", "")
                raise RuntimeError(
                    f"Task not finished. status={status}, progress={progress}"
                )

            pil = download_image(file_url, verify=get_ssl_verify())
            return (pil_to_tensor(pil), status, file_url)
