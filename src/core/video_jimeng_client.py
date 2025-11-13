"""
火山引擎即梦AI数字人生成客户端
支持OmniHuman 1.0和1.5两个版本
1.0版：主体识别 + 视频生成（480P，1元/秒，建议音频<15秒）
1.5版：主体识别 + 主体检测 + 视频生成（1080P，1.2元/秒，音频<35秒，支持提示词和多主体）
"""

import json
import time
import hashlib
import hmac
import requests
from datetime import datetime
from typing import Dict, Optional, Tuple, Any, List

from ..utils import retry, validate_url
from ..config import DEFAULT_TIMEOUT, MAX_RETRIES, RETRY_DELAY


class VideoJimengClient:
    """火山引擎即梦AI数字人生成客户端"""

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
            "1.0": {
                "detect": "jimeng_realman_avatar_picture_create_role_omni",
                "generate": "jimeng_realman_avatar_picture_omni_v2"
            },
            "1.5": {
                "detect": "jimeng_realman_avatar_picture_create_role_omni_v15",
                "detect_object": "jimeng_realman_avatar_object_detection",
                "generate": "jimeng_realman_avatar_picture_omni_v15"
            }
        }

        # 版本配置
        self.VERSION_CONFIG = {
            "1.0": {
                "name": "OmniHuman 1.0",
                "description": "数字人快速模式",
                "resolution": "480P",
                "max_audio_length": 15,  # 建议值
                "price": 1.0,  # 元/秒
                "features": ["主体识别", "视频生成"]
            },
            "1.5": {
                "name": "OmniHuman 1.5",
                "description": "数字人增强模式",
                "resolution": "1080P",
                "max_audio_length": 35,  # 严格限制
                "price": 1.2,  # 元/秒
                "features": ["主体识别", "主体检测", "视频生成", "提示词控制", "多主体指定", "情感表演"]
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
            # 直接返回API的原始响应
            try:
                error_json = e.response.json()
                raise Exception(f"{error_json}")
            except:
                raise Exception(f"{e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")

    @retry(max_retries=MAX_RETRIES, delay=RETRY_DELAY)
    def detect_avatar(self, image_url: str, version: str = "1.0") -> Dict[str, Any]:
        """
        数字人形象识别（检测图片是否包含人、类人、拟人等主体）

        Args:
            image_url: 图片URL链接
            version: 版本号，可选值: 1.0, 1.5

        Returns:
            识别结果
        """
        # 参数验证
        if not validate_url(image_url):
            raise ValueError("图片URL格式不正确")

        if version not in self.REQ_KEYS:
            raise ValueError(f"不支持的版本: {version}，支持的版本: 1.0, 1.5")

        config = self.VERSION_CONFIG[version]
        req_key = self.REQ_KEYS[version]["detect"]

        print(f"开始数字人形象识别，版本: {config['name']} - {config['description']}")

        response = self._make_request("POST", "CVSubmitTask", req_key, data={"image_url": image_url})

        if response.get("code") != 10000:
            error_msg = response.get("message", "未知错误")
            raise Exception(f"数字人形象识别任务提交失败: {error_msg}")

        task_id = response["data"]["task_id"]
        print(f"数字人形象识别任务已提交，任务ID: {task_id}")

        # 等待识别完成
        result = self.wait_for_completion(task_id, "detect", version)
        return result

    @retry(max_retries=MAX_RETRIES, delay=RETRY_DELAY)
    def detect_object(self, image_url: str) -> Dict[str, Any]:
        """
        对象检测（1.5版专用，检测图片中的所有主体，返回mask图）

        Args:
            image_url: 图片URL链接

        Returns:
            对象检测结果，包含mask图URL
        """
        # 参数验证
        if not validate_url(image_url):
            raise ValueError("图片URL格式不正确")

        req_key = self.REQ_KEYS["1.5"]["detect_object"]
        version = "1.5"
        config = self.VERSION_CONFIG[version]

        print(f"开始对象检测，版本: {config['name']} - 检测多主体信息和mask图")

        # 主体检测使用CVProcess接口，不是异步任务
        response = self._make_request("POST", "CVProcess", req_key, data={"image_url": image_url})

        if response.get("code") != 10000:
            error_msg = response.get("message", "未知错误")
            raise Exception(f"对象检测失败: {error_msg}")

        # 解析响应数据
        resp_data = response["data"].get("resp_data")
        if resp_data:
            try:
                resp_data_dict = json.loads(resp_data) if isinstance(resp_data, str) else resp_data
                status = resp_data_dict.get("status", 0)  # 0:不包含主体, 1:包含主体

                if status == 1:
                    object_detection_result = resp_data_dict.get("object_detection_result", {})
                    mask_urls = object_detection_result.get("mask", {}).get("url", [])
                    print(f"✅ 检测到 {len(mask_urls)} 个对象")
                    return {
                        "status": "done",
                        "contains_object": status,
                        "mask_urls": mask_urls,
                        "resp_data": resp_data_dict
                    }
                else:
                    print("❌ 未检测到对象")
                    return {
                        "status": "done",
                        "contains_object": status,
                        "mask_urls": [],
                        "resp_data": resp_data_dict
                    }
            except json.JSONDecodeError:
                print(f"解析检测结果失败: {resp_data}")
                return {"status": "error", "message": "解析检测结果失败"}
        else:
            return {"status": "error", "message": "未获取到检测数据"}

    @retry(max_retries=MAX_RETRIES, delay=RETRY_DELAY)
    def generate_video(self, image_url: str, audio_url: str, version: str = "1.5", prompt: Optional[str] = None, mask_url: Optional[List[str]] = None, seed: Optional[int] = None, pe_fast_mode: bool = False, aigc_meta: Optional[Dict] = None, auto_detect: bool = True) -> str:
        """
        生成数字人视频

        Args:
            image_url: 图片URL链接
            audio_url: 音频URL链接
            version: 版本号，可选值: 1.0, 1.5
            prompt: 提示词（仅1.5版支持，支持中文、英语、日语、韩语、墨西哥语、印尼语）
            mask_url: mask图URL列表（仅1.5版，用于指定主体）
            seed: 随机种子（仅1.5版，默认-1随机）
            pe_fast_mode: 是否启用快速模式（仅1.5版）
            aigc_meta: 隐式标识配置
            auto_detect: 是否自动进行主体检测（1.5版时建议开启）

        Returns:
            任务ID
        """
        # 参数验证
        if not validate_url(image_url):
            raise ValueError("图片URL格式不正确")

        if not validate_url(audio_url):
            raise ValueError("音频URL格式不正确")

        if version not in self.REQ_KEYS:
            raise ValueError(f"不支持的版本: {version}，支持的版本: 1.0, 1.5")

        config = self.VERSION_CONFIG[version]
        req_key = self.REQ_KEYS[version]["generate"]

        print(f"开始生成数字人视频，版本: {config['name']}")
        print(f"输出分辨率: {config['resolution']}")
        print(f"收费标准: {config['price']}元/秒")
        print(f"音频长度限制: {config['max_audio_length']}秒")

        # 1.5版建议先进行主体检测
        if version == "1.5" and auto_detect:
            print("🔍 建议先进行主体检测以确保图片符合要求...")
            try:
                detect_result = self.detect_avatar(image_url, version)
                if detect_result.get("contains_subject") == 0:
                    raise Exception("图片中未检测到人、类人、拟人等主体，请更换图片")
                print("✅ 主体检测通过，开始生成视频...")

                # 如果没有提供mask_url但检测到多个对象，提示用户
                if not mask_url and detect_result.get("mask_urls") and len(detect_result["mask_urls"]) > 1:
                    print(f"💡 检测到 {len(detect_result['mask_urls'])} 个对象，如需指定特定对象说话，请使用对象检测获取mask_url")
            except Exception as e:
                print(f"⚠️ 主体检测失败，但仍继续生成: {str(e)}")

        # 构建请求数据
        data = {
            "image_url": image_url,
            "audio_url": audio_url
        }

        # 1.5版特有参数
        if version == "1.5":
            if prompt:
                # 支持的语言：中文、英语、日语、韩语、墨西哥语、印尼语
                data["prompt"] = prompt
                print(f"提示词: {prompt}")

            if mask_url:
                data["mask_url"] = mask_url
                print(f"指定主体mask数量: {len(mask_url)}")

            if seed is not None:
                data["seed"] = seed
                print(f"随机种子: {seed}")

            if pe_fast_mode:
                data["pe_fast_mode"] = True
                print("启用快速模式")

        # 构建req_json（隐式标识）
        req_json = None
        if aigc_meta:
            req_json = json.dumps({"aigc_meta": aigc_meta}, ensure_ascii=False)

        response = self._make_request("POST", "CVSubmitTask", req_key, data=data, req_json=req_json)

        if response.get("code") != 10000:
            error_msg = response.get("message", "未知错误")
            raise Exception(f"视频生成任务提交失败: {error_msg}")

        task_id = response["data"]["task_id"]
        print(f"数字人视频任务已提交，任务ID: {task_id}")
        return task_id

    def get_result(self, task_id: str, operation_type: str = "generate", version: str = "1.5", aigc_meta: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取任务结果

        Args:
            task_id: 任务ID
            operation_type: 操作类型 (detect, detect_subjects, generate)
            version: 版本号
            aigc_meta: 隐式标识配置

        Returns:
            任务结果
        """
        if version not in self.REQ_KEYS:
            raise ValueError(f"不支持的版本: {version}")

        # 根据操作类型选择req_key
        if operation_type == "detect":
            req_key = self.REQ_KEYS[version]["detect"]
        elif operation_type == "detect_object":
            req_key = self.REQ_KEYS[version]["detect_object"]
        elif operation_type == "generate":
            req_key = self.REQ_KEYS[version]["generate"]
        else:
            raise ValueError(f"不支持的操作类型: {operation_type}")

        # 构建req_json（隐式标识）
        req_json = None
        if aigc_meta:
            req_json = json.dumps({"aigc_meta": aigc_meta}, ensure_ascii=False)

        try:
            response = self._make_request("POST", "CVGetResult", req_key, task_id=task_id, req_json=req_json)

            if response.get("code") != 10000:
                raise Exception(f"获取结果失败: {response}")

            data = response["data"]
            status = data["status"]

            if status == "done":
                result = {
                    "status": status,
                    "aigc_meta_tagged": data.get("aigc_meta_tagged", False)
                }

                # 根据操作类型处理结果
                if operation_type == "generate":
                    # 视频生成结果
                    video_url = data.get("video_url")
                    if video_url:
                        result["video_url"] = video_url
                        print(f"视频生成成功！视频URL: {video_url}")
                elif operation_type in ["detect", "detect_object"]:
                    # 主体识别/检测结果
                    resp_data = data.get("resp_data")
                    if resp_data:
                        try:
                            resp_data_dict = json.loads(resp_data) if isinstance(resp_data, str) else resp_data
                            if operation_type == "detect":
                                result["contains_subject"] = resp_data_dict.get("status", 0)  # 0:不包含, 1:包含
                                print(f"主体识别结果: {'包含主体' if result['contains_subject'] == 1 else '不包含主体'}")
                            elif operation_type == "detect_object":
                                result["contains_object"] = resp_data_dict.get("status", 0)  # 0:不包含, 1:包含
                                print(f"对象检测结果: {'包含对象' if result['contains_object'] == 1 else '不包含对象'}")
                        except json.JSONDecodeError:
                            print(f"解析检测结果失败: {resp_data}")

                return result
            else:
                return {"status": status, "message": f"任务状态: {status}"}

        except Exception as e:
            raise Exception(f"获取结果失败: {str(e)}")

    def wait_for_completion(self, task_id: str, operation_type: str, version: str, max_wait_time: int = 300, check_interval: int = 15) -> Dict[str, Any]:
        """
        等待任务完成

        Args:
            task_id: 任务ID
            operation_type: 操作类型
            version: 版本号
            max_wait_time: 最大等待时间（秒）
            check_interval: 检查间隔（秒）

        Returns:
            任务结果
        """
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                result = self.get_result(task_id, operation_type, version)

                if result.get("status") == "done":
                    return result
                elif result.get("status") in ["not_found", "expired"]:
                    raise Exception(f"任务异常: {result.get('status')}")
                elif result.get("status") == "processing":
                    # 1.5版特有状态：前置处理中
                    print("任务前置处理中，请稍候...")
                elif result.get("video_url") or result.get("contains_subject") is not None or result.get("contains_object") is not None:
                    # 如果返回结果包含有效数据，说明任务已完成
                    return result

                print(f"任务进行中... 状态: {result.get('status', 'unknown')}")
                time.sleep(check_interval)

            except Exception as e:
                if "任务异常" in str(e):
                    raise
                print(f"检查任务状态时出错: {str(e)}")
                time.sleep(check_interval)

        raise TimeoutError(f"等待任务完成超时 ({max_wait_time}秒)")

    def generate_video_from_image_audio(self, image_url: str, audio_url: str, version: str = "1.5", prompt: Optional[str] = None, mask_url: Optional[List[str]] = None, seed: Optional[int] = None, pe_fast_mode: bool = False, aigc_meta: Optional[Dict] = None, max_wait_time: int = 600) -> Dict[str, Any]:
        """
        从图片和音频生成数字人视频（完整流程）

        Args:
            image_url: 图片URL链接
            audio_url: 音频URL链接
            version: 版本号
            prompt: 提示词（仅1.5版支持）
            mask_url: mask图URL列表（仅1.5版）
            seed: 随机种子（仅1.5版）
            pe_fast_mode: 快速模式（仅1.5版）
            aigc_meta: 隐式标识配置
            max_wait_time: 最大等待时间（秒）

        Returns:
            生成结果
        """
        config = self.VERSION_CONFIG[version]
        print(f"开始生成数字人视频（{config['name']}）")

        # 步骤：生成视频（内部自动包含检测）
        task_id = self.generate_video(image_url, audio_url, version, prompt, mask_url, seed, pe_fast_mode, aigc_meta)

        # 等待完成
        result = self.wait_for_completion(task_id, "generate", version, max_wait_time=max_wait_time)

        if result.get("status") == "done":
            print("🎉 数字人视频生成完成！")
            return {
                "video_url": result.get("video_url"),
                "aigc_meta_tagged": result.get("aigc_meta_tagged"),
                "task_id": task_id,
                "version": version
            }
        else:
            raise Exception(f"视频生成失败: {result}")


# 示例使用代码
if __name__ == "__main__":
    # 配置示例
    ACCESS_KEY = "your_access_key_here"
    SECRET_KEY = "your_secret_key_here"

    # 测试参数
    IMAGE_URL = "https://example.com/image.jpg"  # 替换为实际的图片URL
    AUDIO_URL = "https://example.com/audio.mp3"  # 替换为实际的音频URL

    # 初始化客户端
    client = VideoJimengClient(ACCESS_KEY, SECRET_KEY)

    try:
        # AIGC隐式标识配置（可选）
        aigc_meta = {
            "content_producer": "your_producer_id",
            "producer_id": "unique_producer_id_123",
            "content_propagator": "your_propagator_id",
            "propagate_id": "unique_propagate_id_456"
        }

        # 使用1.5版生成视频（推荐）
        result = client.generate_video_from_image_audio(
            image_url=IMAGE_URL,
            audio_url=AUDIO_URL,
            version="1.5",
            prompt="情感丰富的表演，电影感运镜，自然流畅",
            seed=12345,  # 固定随机种子
            pe_fast_mode=False,  # 不使用快速模式
            aigc_meta=aigc_meta
        )

        print("数字人视频生成成功！")
        print(f"视频URL: {result['video_url']}")
        print(f"使用版本: {result['version']}")

    except Exception as e:
        print(f"生成视频失败: {str(e)}")