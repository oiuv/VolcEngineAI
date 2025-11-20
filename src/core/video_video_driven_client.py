#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
火山引擎单图视频驱动客户端
实现单图+视频的动作模仿功能
通过图片和驱动视频生成模仿视频动作的视频
"""

import json
import time
from typing import Dict, Any, Optional

from .base_volcengine_client import BaseVolcengineClient


class VideoVideoDrivenClient(BaseVolcengineClient):
    """
    火山引擎单图视频驱动客户端

    功能：输入图片+视频，生成以图片场景和人物模仿视频动作的视频
    支持人脸表情和肢体动作驱动，输出960x540或896x672分辨率的视频
    """

    def __init__(self, access_key: str, secret_key: str):
        """
        初始化单图视频驱动客户端

        Args:
            access_key: 火山引擎访问密钥
            secret_key: 火山引擎秘密密钥
        """
        super().__init__(access_key, secret_key)

        # 服务标识
        self.REQ_KEY = "realman_avatar_imitator_v2v_gen_video"

        # 配置信息
        self.CONFIG = {
            "name": "单图视频驱动",
            "description": "通过图片和驱动视频生成模仿视频动作的视频",
            "max_video_duration": 30,  # 最大30秒
            "supported_video_formats": ["mp4", "mov", "webm"],
            "supported_image_formats": ["jpeg", "jpg", "png"],
            "min_image_resolution": 512,
            "max_image_resolution": 4096,
            "min_video_resolution": 540,
            "max_video_resolution": 2048,
            "output_resolutions": ["960x540", "896x672"],
            "price": 0.3,  # 元/秒
            "features": ["表情驱动", "肢体动作驱动", "全身驱动", "半身驱动", "肖像驱动"]
        }

    def submit_driven_task(self, image_url: str, video_url: str, aigc_meta: Optional[Dict] = None) -> str:
        """
        提交单图视频驱动任务

        Args:
            image_url: 图片URL链接（需公网可访问）
            video_url: 驱动视频URL链接（需公网可访问）
            aigc_meta: 隐式标识配置

        Returns:
            任务ID

        Raises:
            ValueError: 参数验证失败
            Exception: 任务提交失败
        """
        # 参数验证
        self._validate_image_url(image_url)
        self._validate_video_url(video_url)

        # 构建请求数据
        data = {
            "image_url": image_url,
            "driving_video_info": {
                "store_type": 0,  # 固定值0
                "video_url": video_url
            }
        }

        # 构建req_json（隐式标识）
        req_json = None
        if aigc_meta:
            req_json = json.dumps({"aigc_meta": aigc_meta}, ensure_ascii=False)

        try:
            # 提交任务
            response = self._make_request("POST", "CVSubmitTask", self.REQ_KEY, data=data, req_json=req_json)

            if response.get("code") != 10000:
                error_msg = response.get("message", "未知错误")
                raise Exception(f"单图视频驱动任务提交失败: {error_msg}")

            task_id = response["data"]["task_id"]
            return task_id

        except Exception as e:
            raise Exception(f"提交单图视频驱动任务失败: {str(e)}")

    def get_driven_result(self, task_id: str, aigc_meta: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取单图视频驱动任务结果

        Args:
            task_id: 任务ID
            aigc_meta: 隐式标识配置

        Returns:
            任务结果

        Raises:
            Exception: 查询结果失败
        """
        # 构建req_json（隐式标识）
        req_json = None
        if aigc_meta:
            req_json = json.dumps({"aigc_meta": aigc_meta}, ensure_ascii=False)

        try:
            # 查询结果
            response = self._make_request("POST", "CVGetResult", self.REQ_KEY, task_id=task_id, req_json=req_json)

            if response.get("code") != 10000:
                error_msg = response.get("message", "未知错误")
                raise Exception(f"获取单图视频驱动结果失败: {error_msg}")

            # 直接返回完整的原始API响应
            return response["data"]

        except Exception as e:
            raise Exception(f"获取单图视频驱动结果失败: {str(e)}")

    def wait_for_completion(self, task_id: str, max_wait_time: int = 600, check_interval: int = 15) -> Dict[str, Any]:
        """
        等待任务完成

        Args:
            task_id: 任务ID
            max_wait_time: 最大等待时间（秒）
            check_interval: 检查间隔（秒）

        Returns:
            任务结果

        Raises:
            Exception: 任务失败或超时
        """
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                result = self.get_driven_result(task_id)

                if result.get("status") == "done":
                    return result
                elif result.get("status") in ["not_found", "expired"]:
                    raise Exception(f"任务异常: {result.get('status')}")
                elif result.get("video_url"):
                    # 如果有video_url说明任务已完成
                    return result

                print(f"任务进行中... 状态: {result.get('status', 'unknown')}")
                time.sleep(check_interval)

            except Exception as e:
                if "任务异常" in str(e):
                    raise
                print(f"检查任务状态时出错: {str(e)}")
                time.sleep(check_interval)

        raise Exception(f"等待超时 ({max_wait_time}秒)，任务可能仍在处理")


# 示例使用代码
if __name__ == "__main__":
    # 配置示例
    ACCESS_KEY = "your_access_key_here"
    SECRET_KEY = "your_secret_key_here"

    # 测试参数
    IMAGE_URL = "https://example.com/image.jpg"  # 替换为实际的图片URL
    VIDEO_URL = "https://example.com/video.mp4"  # 替换为实际的视频URL

    # 初始化客户端
    client = VideoVideoDrivenClient(ACCESS_KEY, SECRET_KEY)

    try:
        # AIGC隐式标识配置（可选）
        aigc_meta = {
            "content_producer": "your_producer_id",
            "producer_id": "unique_producer_id_123",
            "content_propagator": "your_propagator_id",
            "propagate_id": "unique_propagate_id_456"
        }

        # 提交单图视频驱动任务
        task_id = client.submit_driven_task(
            image_url=IMAGE_URL,
            video_url=VIDEO_URL,
            aigc_meta=aigc_meta
        )

        # 等待任务完成
        result = client.wait_for_completion(task_id)

        if result.get("video_url"):
            print("🎉 单图视频驱动视频生成成功！")
            print(f"📹 视频URL: {result['video_url']}")
            print(f"🏷️ 隐式标识: {'已添加' if result.get('aigc_meta_tagged') else '未添加'}")
        else:
            print("❌ 视频生成失败")

    except Exception as e:
        print(f"单图视频驱动失败: {str(e)}")