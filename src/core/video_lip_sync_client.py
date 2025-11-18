"""
火山引擎视频改口型客户端
输入单人口播视频+音频，修改视频中人物口型以匹配音频
支持Lite模式和Basic模式
"""

import json
import time
from typing import Dict, Any

from .base_volcengine_client import BaseVolcengineClient
from ..utils import retry
from ..config import DEFAULT_TIMEOUT, MAX_RETRIES, RETRY_DELAY


class VideoLipSyncClient(BaseVolcengineClient):
    """火山引擎视频改口型客户端"""

    def __init__(self, access_key: str, secret_key: str):
        """
        初始化客户端

        Args:
            access_key: 火山引擎访问密钥
            secret_key: 火山引擎秘密密钥
        """
        super().__init__(access_key, secret_key)

        # 服务标识映射
        self.REQ_KEYS = {
            "lite": "realman_change_lips",
            "basic": "realman_change_lips_basic_chimera"
        }

        # 模式配置
        self.MODE_CONFIG = {
            "lite": {
                "name": "Lite模式",
                "description": "支持单人正面视频",
                "max_audio_length": 240,  # 秒
                "min_audio_length": 1,
                "supports_align_audio": True,
                "supports_templ_start": True
            },
            "basic": {
                "name": "Basic模式",
                "description": "支持单人复杂场景",
                "max_audio_length": 150,  # 秒
                "min_audio_length": 1,
                "supports_scene_detection": True,
                "supports_separate_vocal": True
            }
        }

    
    @retry(max_retries=MAX_RETRIES, delay=RETRY_DELAY)
    def submit_lip_sync_task(self, video_url: str, audio_url: str, mode: str = "lite", **kwargs) -> str:
        """
        提交视频改口型任务

        Args:
            video_url: 视频素材URL
            audio_url: 纯人声音频URL
            mode: 模式，可选值: lite(Lite模式), basic(Basic模式)
            **kwargs: 其他可选参数

        Returns:
            任务ID
        """
        # 参数验证
        self._validate_video_url(video_url)
        self._validate_audio_url(audio_url)

        if mode not in self.REQ_KEYS:
            raise ValueError(f"不支持的模式: {mode}，支持的模式: lite, basic")

        req_key = self.REQ_KEYS[mode]
        config = self.MODE_CONFIG[mode]

        print(f"开始提交视频改口型任务，模式: {config['name']} - {config['description']}")

        # 构建请求数据
        data = {
            "url": video_url,
            "pure_audio_url": audio_url
        }

        # 添加可选参数
        if "separate_vocal" in kwargs and mode == "basic":
            data["separate_vocal"] = kwargs["separate_vocal"]
            print(f"人声分离: {'开启' if kwargs['separate_vocal'] else '关闭'}")

        if "open_scenedet" in kwargs and mode == "basic":
            data["open_scenedet"] = kwargs["open_scenedet"]
            print(f"场景切分与说话人识别: {'开启' if kwargs['open_scenedet'] else '关闭'}")

        if "align_audio" in kwargs and mode == "lite":
            data["align_audio"] = kwargs["align_audio"]
            print(f"视频循环: {'开启' if kwargs['align_audio'] else '关闭'}")

        if "align_audio_reverse" in kwargs and mode == "lite":
            data["align_audio_reverse"] = kwargs["align_audio_reverse"]
            if kwargs["align_audio_reverse"]:
                data["align_audio"] = True  # 倒放循环需要同时开启正循环
            print(f"倒放循环: {'开启' if kwargs['align_audio_reverse'] else '关闭'}")

        if "templ_start_seconds" in kwargs and mode == "lite":
            data["templ_start_seconds"] = kwargs["templ_start_seconds"]
            print(f"模板视频开始时间: {kwargs['templ_start_seconds']}秒")

        response = self._make_request("POST", "CVSubmitTask", req_key, data=data)

        if response.get("code") != 10000:
            error_msg = response.get("message", "未知错误")
            raise Exception(f"视频改口型任务提交失败: {error_msg}")

        task_id = response["data"]["task_id"]
        print(f"视频改口型任务已提交，任务ID: {task_id}")
        print(f"注意：该模式支持音频长度 {config['min_audio_length']}-{config['max_audio_length']} 秒")
        return task_id

    def get_lip_sync_result(self, task_id: str, mode: str = "lite", aigc_meta: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取视频改口型结果

        Args:
            task_id: 任务ID
            mode: 模式
            aigc_meta: 隐式标识配置

        Returns:
            视频改口型结果
        """
        if mode not in self.REQ_KEYS:
            raise ValueError(f"不支持的模式: {mode}")

        req_key = self.REQ_KEYS[mode]

        # 构建req_json
        req_json = None
        if aigc_meta:
            req_json = json.dumps({"aigc_meta": aigc_meta}, ensure_ascii=False)

        try:
            response = self._make_request("POST", "CVGetResult", req_key, task_id=task_id, req_json=req_json)

            if response.get("code") != 10000:
                raise Exception(f"获取视频改口型结果失败: {response}")

            data = response["data"]
            status = data["status"]

            if status == "done":
                resp_data = json.loads(data["resp_data"])
                if resp_data.get("code") == 0:
                    result = {
                        "status": status,
                        "task_id": task_id,
                        "aigc_meta_tagged": data.get("aigc_meta_tagged", False)
                    }

                    # 获取视频URL
                    video_url = resp_data.get("url")
                    if video_url:
                        result["video_url"] = video_url

                    # 添加视频元数据
                    vid_info = resp_data.get("vid_info", {})
                    if vid_info and "VideoMeta" in vid_info:
                        result["video_meta"] = vid_info["VideoMeta"]

                    return result
                else:
                    raise Exception(f"视频改口型失败: {resp_data.get('msg', '未知错误')}")
            else:
                return {"status": status, "message": f"任务状态: {status}"}

        except Exception as e:
            raise Exception(f"获取视频改口型结果失败: {str(e)}")

    def wait_for_completion(self, task_id: str, mode: str, max_wait_time: int = 600, check_interval: int = 15) -> Dict[str, Any]:
        """
        等待任务完成

        Args:
            task_id: 任务ID
            mode: 模式
            max_wait_time: 最大等待时间（秒）
            check_interval: 检查间隔（秒）

        Returns:
            任务结果
        """
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                result = self.get_lip_sync_result(task_id, mode)

                # 检查API响应状态
                if result.get("code") == 10000:  # API成功
                    data = result.get("data", {})
                    status = data.get("status")

                    if status == "done":
                        return result
                    elif status in ["not_found", "expired"]:
                        raise Exception(f"任务异常: {status}")
                    elif "video_url" in result:
                        # 如果返回结果包含video_url，说明任务已完成
                        return result

                # 优先使用API返回的中文message，如果没有则使用status
                message = result.get("message", f"任务状态: {result.get('status', 'unknown')}")
                print(f"任务进行中... {message}")
                time.sleep(check_interval)

            except Exception as e:
                if "任务异常" in str(e):
                    raise
                print(f"检查任务状态时出错: {str(e)}")
                time.sleep(check_interval)

        raise TimeoutError(f"等待任务完成超时 ({max_wait_time}秒)")

    def change_lip_sync(self, video_url: str, audio_url: str, mode: str = "lite", aigc_meta: Optional[Dict] = None, max_wait_time: int = 600, **kwargs) -> Dict[str, Any]:
        """
        视频改口型（完整流程）

        Args:
            video_url: 视频素材URL
            audio_url: 纯人声音频URL
            mode: 模式，可选值: lite(Lite模式), basic(Basic模式)
            aigc_meta: 隐式标识配置
            max_wait_time: 最大等待时间（秒）
            **kwargs: 其他可选参数

        Returns:
            生成结果
        """
        print(f"开始视频改口型，模式: {mode}")

        # 步骤1：提交任务
        task_id = self.submit_lip_sync_task(video_url, audio_url, mode, **kwargs)

        # 步骤2：等待完成
        result = self.wait_for_completion(task_id, mode, max_wait_time=max_wait_time)

        if result.get("status") == "done":
            print("🎉 视频改口型完成！")
            return {
                "video_url": result.get("video_url"),
                "video_meta": result.get("video_meta"),
                "aigc_meta_tagged": result.get("aigc_meta_tagged"),
                "task_id": task_id
            }
        else:
            raise Exception(f"视频改口型失败: {result}")


# 示例使用代码
if __name__ == "__main__":
    # 配置示例
    ACCESS_KEY = "your_access_key_here"
    SECRET_KEY = "your_secret_key_here"

    # 测试参数
    VIDEO_URL = "https://example.com/video.mp4"  # 替换为实际的视频URL
    AUDIO_URL = "https://example.com/audio.mp3"  # 替换为实际的音频URL

    # 初始化客户端
    client = VideoLipSyncClient(ACCESS_KEY, SECRET_KEY)

    try:
        # AIGC隐式标识配置（可选）
        aigc_meta = {
            "content_producer": "your_producer_id",
            "producer_id": "unique_producer_id_123",
            "content_propagator": "your_propagator_id",
            "propagate_id": "unique_propagate_id_456"
        }

        # 使用Lite模式进行视频改口型
        result = client.change_lip_sync(
            video_url=VIDEO_URL,
            audio_url=AUDIO_URL,
            mode="lite",
            aigc_meta=aigc_meta,
            align_audio=True,  # 开启视频循环
            separate_vocal=False  # 关闭人声分离
        )

        print("视频改口型成功！")
        print(f"视频URL: {result['video_url']}")

    except Exception as e:
        print(f"视频改口型失败: {str(e)}")