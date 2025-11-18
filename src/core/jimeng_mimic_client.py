#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
即梦AI动作模仿客户端
实现图片+视频的动作模仿功能
"""

import json
import time
from typing import Dict, Any, Optional

from .base_volcengine_client import BaseVolcengineClient


class VideoJimengMimicClient(BaseVolcengineClient):
    """
    即梦AI动作模仿客户端

    功能：输入图片+模板视频，生成动作模仿视频
    支持真人、动漫、宠物的动作和表情模仿
    """

    def __init__(self, access_key: str, secret_key: str):
        """
        初始化即梦AI动作模仿客户端

        Args:
            access_key: 火山引擎访问密钥
            secret_key: 火山引擎秘密密钥
        """
        super().__init__(access_key, secret_key)

    def submit_mimic_task(self, image_url: str, video_url: str, aigc_meta: Optional[Dict] = None) -> str:
        """
        提交动作模仿任务

        Args:
            image_url: 图片URL链接（需公网可访问）
            video_url: 视频URL链接（需公网可访问）
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
            "video_url": video_url
        }

        # 构建req_json（隐式标识）
        req_json = None
        if aigc_meta:
            req_json = json.dumps({"aigc_meta": aigc_meta}, ensure_ascii=False)

        try:
            # 使用同步转异步提交任务接口
            response = self._make_request("POST", "CVSync2AsyncSubmitTask", "jimeng_dream_actor_m1_gen_video_cv", data=data, req_json=req_json)

            if response.get("code") != 10000:
                error_msg = response.get("message", "未知错误")
                raise Exception(f"动作模仿任务提交失败: {error_msg}")

            task_id = response["data"]["task_id"]
            return task_id

        except Exception as e:
            raise Exception(f"提交动作模仿任务失败: {str(e)}")

    def get_mimic_result(self, task_id: str, aigc_meta: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取动作模仿任务结果

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
            # 使用同步转异步查询结果接口
            response = self._make_request("POST", "CVSync2AsyncGetResult", "jimeng_dream_actor_m1_gen_video_cv", task_id=task_id, req_json=req_json)

            if response.get("code") != 10000:
                error_msg = response.get("message", "未知错误")
                raise Exception(f"获取动作模仿结果失败: {error_msg}")

            # 直接返回完整的原始API响应
            return response["data"]

        except Exception as e:
            raise Exception(f"获取动作模仿结果失败: {str(e)}")

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
                result = self.get_mimic_result(task_id)

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
    client = VideoJimengMimicClient(ACCESS_KEY, SECRET_KEY)

    try:
        # AIGC隐式标识配置（可选）
        aigc_meta = {
            "content_producer": "your_producer_id",
            "producer_id": "unique_producer_id_123",
            "content_propagator": "your_propagator_id",
            "propagate_id": "unique_propagate_id_456"
        }

        # 提交动作模仿任务
        task_id = client.submit_mimic_task(
            image_url=IMAGE_URL,
            video_url=VIDEO_URL,
            aigc_meta=aigc_meta
        )

        # 等待任务完成
        result = client.wait_for_completion(task_id)

        if result.get("video_url"):
            print("🎉 动作模仿视频生成成功！")
            print(f"📹 视频URL: {result['video_url']}")
            print(f"🏷️ 隐式标识: {'已添加' if result.get('aigc_meta_tagged') else '未添加'}")
        else:
            print("❌ 视频生成失败")

    except Exception as e:
        print(f"动作模仿失败: {str(e)}")