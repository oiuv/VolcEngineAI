"""
火山引擎单图音频驱动视频生成客户端
支持普通模式、灵动模式和大画幅灵动模式
"""

import json
import time
import hashlib
import hmac
import requests
from datetime import datetime
from typing import Dict, Optional, Tuple, Any
from urllib.parse import quote
from ..utils import retry, validate_url, validate_mode, get_mode_description, get_supported_audio_length, format_duration
from ..config import DEFAULT_TIMEOUT, MAX_RETRIES, RETRY_DELAY


class VideoAudioDrivenClient:
    """火山引擎单图音频驱动视频生成客户端"""

    def __init__(self, access_key: str, secret_key: str, region: str = "cn-north-1", service: str = "cv"):
        """
        初始化客户端

        Args:
            access_key: 火山引擎访问密钥
            secret_key: 火山引擎秘密密钥
            region: 区域，默认为cn-north-1
            service: 服务名，默认为cv
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.service = service
        self.base_url = "https://visual.volcengineapi.com"

        # 服务标识映射
        self.REQ_KEYS = {
            "normal": {
                "create_role": "realman_avatar_picture_create_role",
                "generate_video": "realman_avatar_picture_v2"
            },
            "loopy": {
                "create_role": "realman_avatar_picture_create_role_loopy",
                "generate_video": "realman_avatar_picture_loopy"
            },
            "loopyb": {
                "create_role": "realman_avatar_picture_create_role_loopyb",
                "generate_video": "realman_avatar_picture_loopyb"
            }
        }

    def _generate_signature(self, method: str, uri: str, query_params: str, headers: Dict[str, str], body: str) -> Tuple[str, str]:
        """
        生成签名

        Args:
            method: HTTP方法
            uri: 请求URI
            query_params: 查询参数
            headers: 请求头
            body: 请求体

        Returns:
            签名和签名头信息
        """
        # 计算请求时间
        now = datetime.utcnow()
        timestamp = now.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = now.strftime('%Y%m%d')

        # 规范化查询参数
        canonical_querystring = self._canonicalize_query_params(query_params)

        # 规范化请求头
        canonical_headers, signed_headers = self._canonicalize_headers(headers)

        # 创建规范请求
        canonical_request = f"{method}\n{uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{hashlib.sha256(body.encode('utf-8')).hexdigest()}"

        # 创建待签字符串
        algorithm = 'HMAC-SHA256'
        credential_scope = f"{date_stamp}/{self.region}/{self.service}/request"
        string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

        # 计算签名
        k_date = hmac.new(self.secret_key.encode('utf-8'), date_stamp.encode('utf-8'), hashlib.sha256).digest()
        k_region = hmac.new(k_date, self.region.encode('utf-8'), hashlib.sha256).digest()
        k_service = hmac.new(k_region, self.service.encode('utf-8'), hashlib.sha256).digest()
        k_signing = hmac.new(k_service, 'request'.encode('utf-8'), hashlib.sha256).digest()
        signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

        # 创建授权头
        authorization = f"{algorithm} Credential={self.access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"

        return signature, authorization

    def _canonicalize_query_params(self, query_params: str) -> str:
        """规范化查询参数"""
        if not query_params:
            return ""

        params = query_params.split('&')
        sorted_params = sorted(params)
        return '&'.join(sorted_params)

    def _canonicalize_headers(self, headers: Dict[str, str]) -> Tuple[str, str]:
        """规范化请求头"""
        # 按字母顺序排序请求头
        sorted_headers = sorted(headers.items())

        canonical_headers = []
        for key, value in sorted_headers:
            canonical_headers.append(f"{key.lower().strip()}:{value.strip()}")

        canonical_headers_str = '\n'.join(canonical_headers) + '\n'
        signed_headers = ';'.join([key.lower().strip() for key, _ in sorted_headers])

        return canonical_headers_str, signed_headers

    def _make_request(self, method: str, action: str, req_key: str, version: str = "2022-08-31", data: Optional[Dict] = None, task_id: Optional[str] = None, req_json: Optional[str] = None) -> Dict:
        """
        发送API请求

        Args:
            method: HTTP方法
            action: API动作
            version: API版本
            req_key: 服务标识
            data: 请求数据
            task_id: 任务ID
            req_json: 请求JSON配置

        Returns:
            API响应
        """
        # 构建查询参数
        query_params = f"Action={action}&Version={version}"

        # 构建请求头
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'visual.volcengineapi.com',
            'X-Content-Sha256': hashlib.sha256(json.dumps(data or {}, ensure_ascii=False).encode('utf-8')).hexdigest()
        }

        # 构建请求体
        body_data = {'req_key': req_key}
        if task_id:
            body_data['task_id'] = task_id
        if req_json:
            body_data['req_json'] = req_json
        if data:
            body_data.update(data)

        body = json.dumps(body_data, ensure_ascii=False)

        # 生成签名
        signature, authorization = self._generate_signature(method, "/", query_params, headers, body)

        # 添加认证头
        now = datetime.utcnow()
        timestamp = now.strftime('%Y%m%dT%H%M%SZ')
        headers['Authorization'] = authorization
        headers['X-Date'] = timestamp

        # 发送请求
        url = f"{self.base_url}?{query_params}"

        try:
            response = requests.post(url, headers=headers, data=body, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("API请求超时，请检查网络连接或稍后重试")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接失败，请检查网络设置")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("认证失败，请检查AccessKey和SecretKey是否正确")
            elif e.response.status_code == 403:
                raise Exception("权限不足，请检查账号是否有相应权限")
            elif e.response.status_code == 429:
                raise Exception("请求过于频繁，请稍后重试")
            elif e.response.status_code >= 500:
                raise Exception("服务器内部错误，请稍后重试")
            else:
                raise Exception(f"HTTP请求失败: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")

    @retry(max_retries=MAX_RETRIES, delay=RETRY_DELAY)
    def create_role(self, image_url: str, mode: str = "normal") -> str:
        """
        创建数字形象

        Args:
            image_url: 图片URL链接
            mode: 模式，可选值: normal(普通模式), loopy(灵动模式), loopyb(大画幅灵动模式)

        Returns:
            任务ID
        """
        # 参数验证
        if not validate_url(image_url):
            raise ValueError("图片URL格式不正确")

        if not validate_mode(mode):
            raise ValueError(f"不支持的模式: {mode}，支持的模式: normal, loopy, loopyb")

        req_key = self.REQ_KEYS[mode]["create_role"]
        print(f"开始创建数字形象，模式: {get_mode_description(mode)}")

        response = self._make_request("POST", "CVSubmitTask", req_key, data={"image_url": image_url})

        if response.get("code") != 10000:
            error_msg = response.get("message", "未知错误")
            raise Exception(f"创建形象任务提交失败: {error_msg}")

        task_id = response["data"]["task_id"]
        print(f"形象创建任务已提交，任务ID: {task_id}")
        return task_id

    def get_role_result(self, task_id: str, mode: str = "normal") -> Dict[str, Any]:
        """
        获取形象创建结果

        Args:
            task_id: 任务ID
            mode: 模式，可选值: normal(普通模式), loopy(灵动模式), loopyb(大画幅灵动模式)

        Returns:
            形象创建结果
        """
        if mode not in self.REQ_KEYS:
            raise ValueError(f"不支持的模式: {mode}")

        req_key = self.REQ_KEYS[mode]["create_role"]

        try:
            response = self._make_request("POST", "CVGetResult", req_key, task_id=task_id)

            if response.get("code") != 10000:
                raise Exception(f"获取形象创建结果失败: {response}")

            data = response["data"]
            status = data["status"]

            if status == "done":
                resp_data = json.loads(data["resp_data"])
                if resp_data.get("code") == 0:
                    resource_id = resp_data["resource_id"]
                    role_type = resp_data.get("role_type", "unknown")
                    face_position = resp_data.get("face_position", [])
                    print(f"形象创建成功！形象ID: {resource_id}, 类型: {role_type}, 人脸位置: {face_position}")
                    return {
                        "resource_id": resource_id,
                        "role_type": role_type,
                        "face_position": face_position,
                        "resp_data": resp_data
                    }
                else:
                    raise Exception(f"形象创建失败: {resp_data.get('msg', '未知错误')}")
            else:
                return {"status": status, "message": f"任务状态: {status}"}

        except Exception as e:
            raise Exception(f"获取形象创建结果失败: {str(e)}")

    @retry(max_retries=MAX_RETRIES, delay=RETRY_DELAY)
    def generate_video(self, resource_id: str, audio_url: str, mode: str = "normal", aigc_meta: Optional[Dict] = None) -> str:
        """
        生成视频

        Args:
            resource_id: 形象ID
            audio_url: 音频URL链接
            mode: 模式，可选值: normal(普通模式), loopy(灵动模式), loopyb(大画幅灵动模式)
            aigc_meta: 隐式标识配置

        Returns:
            任务ID
        """
        # 参数验证
        if not resource_id or not isinstance(resource_id, str):
            raise ValueError("形象ID不能为空")

        if not validate_url(audio_url):
            raise ValueError("音频URL格式不正确")

        if not validate_mode(mode):
            raise ValueError(f"不支持的模式: {mode}，支持的模式: normal, loopy, loopyb")

        req_key = self.REQ_KEYS[mode]["generate_video"]
        max_audio_length = get_supported_audio_length(mode)
        print(f"开始生成视频，模式: {get_mode_description(mode)}")
        print(f"注意：该模式支持的最大音频长度为 {max_audio_length} 秒")

        data = {
            "resource_id": resource_id,
            "audio_url": audio_url
        }

        response = self._make_request("POST", "CVSubmitTask", req_key, data=data)

        if response.get("code") != 10000:
            error_msg = response.get("message", "未知错误")
            raise Exception(f"视频生成任务提交失败: {error_msg}")

        task_id = response["data"]["task_id"]
        print(f"视频生成任务已提交，任务ID: {task_id}")
        return task_id

    def get_video_result(self, task_id: str, mode: str = "normal", aigc_meta: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取视频生成结果

        Args:
            task_id: 任务ID
            mode: 模式，可选值: normal(普通模式), loopy(灵动模式), loopyb(大画幅灵动模式)
            aigc_meta: 隐式标识配置

        Returns:
            视频生成结果
        """
        if mode not in self.REQ_KEYS:
            raise ValueError(f"不支持的模式: {mode}")

        req_key = self.REQ_KEYS[mode]["generate_video"]

        # 构建req_json
        req_json = None
        if aigc_meta:
            req_json = json.dumps({"aigc_meta": aigc_meta}, ensure_ascii=False)

        try:
            response = self._make_request("POST", "CVGetResult", req_key, task_id=task_id, req_json=req_json)

            if response.get("code") != 10000:
                raise Exception(f"获取视频生成结果失败: {response}")

            data = response["data"]
            status = data["status"]

            if status == "done":
                resp_data = json.loads(data["resp_data"])
                if resp_data.get("code") == 0:
                    result = {
                        "status": status,
                        "aigc_meta_tagged": data.get("aigc_meta_tagged", False)
                    }

                    # 根据返回数据结构获取视频URL
                    video_url = None

                    # 大画幅模式直接从data中获取video_url
                    if mode == "loopyb" and data.get("video_url"):
                        video_url = data.get("video_url")
                    else:
                        # 普通模式和灵动模式从resp_data的preview_url获取
                        preview_urls = resp_data.get("preview_url", [])
                        if preview_urls:
                            video_url = preview_urls[0]

                    if video_url:
                        result["video_url"] = video_url
                        print(f"视频生成成功！视频URL: {video_url}")

                    # 添加视频元数据
                    video_meta = resp_data.get("video", {})
                    if video_meta and "VideoMeta" in video_meta:
                        result["video_meta"] = video_meta["VideoMeta"]

                    return result
                else:
                    raise Exception(f"视频生成失败: {resp_data.get('msg', '未知错误')}")
            else:
                return {"status": status, "message": f"任务状态: {status}"}

        except Exception as e:
            raise Exception(f"获取视频生成结果失败: {str(e)}")

    def wait_for_completion(self, task_id: str, mode: str, operation_type: str, max_wait_time: int = 300, check_interval: int = 15) -> Dict[str, Any]:
        """
        等待任务完成

        Args:
            task_id: 任务ID
            mode: 模式
            operation_type: 操作类型 (role 或 video)
            max_wait_time: 最大等待时间（秒）
            check_interval: 检查间隔（秒）

        Returns:
            任务结果
        """
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                if operation_type == "role":
                    result = self.get_role_result(task_id, mode)
                elif operation_type == "video":
                    result = self.get_video_result(task_id, mode)
                else:
                    raise ValueError(f"不支持的操作类型: {operation_type}")

                # 检查任务是否完成
                if result.get("status") == "done":
                    return result
                elif result.get("status") in ["not_found", "expired"]:
                    raise Exception(f"任务异常: {result.get('status')}")
                elif "resource_id" in result or "video_url" in result:
                    # 如果返回结果包含resource_id或video_url，说明任务已完成
                    return result

                print(f"任务进行中... 状态: {result.get('status', 'unknown')}")
                time.sleep(check_interval)

            except Exception as e:
                if "任务异常" in str(e):
                    raise
                print(f"检查任务状态时出错: {str(e)}")
                time.sleep(check_interval)

        raise TimeoutError(f"等待任务完成超时 ({max_wait_time}秒)")

    def generate_video_from_image_audio(self, image_url: str, audio_url: str, mode: str = "normal", aigc_meta: Optional[Dict] = None, max_wait_time: int = 600) -> Dict[str, Any]:
        """
        从图片和音频生成视频（完整流程）

        Args:
            image_url: 图片URL链接
            audio_url: 音频URL链接
            mode: 模式，可选值: normal(普通模式), loopy(灵动模式), loopyb(大画幅灵动模式)
            aigc_meta: 隐式标识配置
            max_wait_time: 最大等待时间（秒）

        Returns:
            生成结果
        """
        print(f"开始生成视频，模式: {mode}")

        # 步骤1：创建形象
        print("步骤1：创建数字形象...")
        role_task_id = self.create_role(image_url, mode)
        role_result = self.wait_for_completion(role_task_id, mode, "role")
        resource_id = role_result["resource_id"]

        print(f"形象创建完成，ID: {resource_id}")

        # 保存形象信息到本地
        try:
            from src.modules.avatar_manager import avatar_manager
            avatar_manager.save_avatar(role_task_id, role_result, mode, role_result.get("resp_data"))
        except Exception as e:
            print(f"⚠️ 形象保存失败: {str(e)}")

        # 步骤2：生成视频
        print("步骤2：生成视频...")
        video_task_id = self.generate_video(resource_id, audio_url, mode, aigc_meta)
        video_result = self.wait_for_completion(video_task_id, mode, "video", max_wait_time=600)

        print("视频生成完成！")
        return {
            "resource_id": resource_id,
            "video_url": video_result.get("video_url"),
            "video_meta": video_result.get("video_meta"),
            "aigc_meta_tagged": video_result.get("aigc_meta_tagged")
        }


# 示例使用代码
if __name__ == "__main__":
    # 配置示例
    ACCESS_KEY = "your_access_key_here"
    SECRET_KEY = "your_secret_key_here"

    # 测试参数
    IMAGE_URL = "https://example.com/image.jpg"  # 替换为实际的图片URL
    AUDIO_URL = "https://example.com/audio.mp3"  # 替换为实际的音频URL

    # 初始化客户端
    client = VideoAudioDrivenClient(ACCESS_KEY, SECRET_KEY)

    try:
        # AIGC隐式标识配置（可选）
        aigc_meta = {
            "content_producer": "your_producer_id",
            "producer_id": "unique_producer_id_123",
            "content_propagator": "your_propagator_id",
            "propagate_id": "unique_propagate_id_456"
        }

        # 使用灵动模式生成视频
        result = client.generate_video_from_image_audio(
            image_url=IMAGE_URL,
            audio_url=AUDIO_URL,
            mode="loopy",
            aigc_meta=aigc_meta
        )

        print("视频生成成功！")
        print(f"视频URL: {result['video_url']}")
        print(f"形象ID: {result['resource_id']}")

    except Exception as e:
        print(f"生成视频失败: {str(e)}")