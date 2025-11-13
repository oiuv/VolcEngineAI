"""
火山引擎创意特效视频生成客户端
基于字节先进的多模态生成类大模型，支持一键生成趣味创意特效视频
支持V1和V2两个版本的接口
"""

import json
import time
import hashlib
import hmac
import requests
from datetime import datetime
from typing import Dict, Optional, Tuple, Any

from ..utils import retry, validate_url
from ..config import DEFAULT_TIMEOUT


class VideoEffectClient:
    """火山引擎创意特效视频生成客户端"""

    def __init__(self, access_key: str, secret_key: str):
        """
        初始化客户端

        Args:
            access_key: 火山引擎访问密钥
            secret_key: 火山引擎秘密密钥
        """
        self.access_key = access_key
        self.secret_key = secret_key

        # V1版本模板（req_key: i2v_bytedance_effects_v1）
        self.V1_TEMPLATES = {
            "becoming_doll": "变身玩偶_480p版",
            "becoming_doll_720p": "变身玩偶_720p版",
            "all_things_ridability_pig": "召唤坐骑 - 猪_480p版",
            "all_things_ridability_pig_720p": "召唤坐骑 - 猪_720p版",
            "all_things_ridability_tiger": "召唤坐骑 - 老虎_480p版",
            "all_things_ridability_tiger_720p": "召唤坐骑 - 老虎_720p版",
            "all_things_ridability_loong": "召唤坐骑 - 龙_480p版",
            "all_things_ridability_loong_720p": "召唤坐骑 - 龙_720p版",
            "all_things_bloom_with_flowers": "万物生花_480p版",
            "all_things_bloom_with_flowers_720p": "万物生花_720p版",
            "double_embrace_single_person": "爱的拥抱（单图）_480p版",
            "double_embrace_single_person_720p": "爱的拥抱（单图）_720p版",
            "double_embrace": "爱的拥抱（双图）_480p版",
            "double_embrace_720p": "爱的拥抱（双图）_720p版",
            "beauty_surround": "AI美女环绕_480p版",
            "beauty_surround_720p": "AI美女环绕_720p版",
            "handsome_man_surround": "AI帅哥环绕_480p版",
            "handsome_man_surround_720p": "AI帅哥环绕_720p版",
            "ai_baby": "天赐宝宝_480p版",
            "ai_baby_720p": "天赐宝宝_720p版"
        }

        # V2版本模板（req_key: i2v_template_cv_v2）
        self.V2_TEMPLATES = {
            "multi_style_stacking_dolls": "emoji小人变身_480p",
            "fluffy_dream_doll_s2e": "梦幻娃娃变身1_480p",
            "fluffy_dream_doll_s2e_720p": "梦幻娃娃变身1_720p",
            "fluffy_dream_doll": "梦幻娃娃变身2_480p",
            "fluffy_dream_doll_720p": "梦幻娃娃变身2_720p",
            "my_world": "我的世界风_480p",
            "my_world_720p": "我的世界风_720p",
            "crystal_ball": "装进水晶球_480p",
            "crystal_ball_720p": "装进水晶球_720p",
            "lying_on_fluffy_belly": "猫星人的守护_480p",
            "lying_on_fluffy_belly_720p": "猫星人的守护_720p",
            "angel_figure": "天使手办变身_480p",
            "angel_figure_720p": "天使手办变身_720p",
            "felt_keychain": "毛毡钥匙扣变身_480p",
            "felt_keychain_720p": "毛毡钥匙扣变身_720p",
            "acrylic_charm": "亚克力挂饰变身_480p",
            "acrylic_charm_720p": "亚克力挂饰变身_720p",
            "polaroid": "拍立得风_480p",
            "polaroid_720p": "拍立得风_720p",
            "blister_pack_action_figure": "潮玩手办变身_480p",
            "blister_pack_action_figure_720p": "潮玩手办变身_720p",
            "french_kiss_dual_version": "法式热吻_双图",
            "french_kiss_dual_version_720p": "法式热吻_双图_720p",
            "french_kiss_solo_version": "法式热吻_单图",
            "french_kiss_solo_version_720p": "法式热吻_单图_720p",
            "costume_bikini": "变装比基尼",
            "costume_bikini_720p": "变装比基尼_720p",
            "hot_dance": "热舞",
            "hot_dance_720p": "热舞_720p",
            "transform_into_mermaid": "变身美人鱼",
            "transform_into_mermaid_720p": "变身美人鱼_720p"
        }

        # 合并所有模板用于查找
        self.ALL_TEMPLATES = {**self.V1_TEMPLATES, **self.V2_TEMPLATES}

        # V1版本双图模板
        self.V1_DUAL_TEMPLATES = ["double_embrace", "double_embrace_720p"]

        # V2版本双图模板
        self.V2_DUAL_TEMPLATES = ["french_kiss_dual_version", "french_kiss_dual_version_720p"]

    def _detect_template_version(self, template_id: str) -> str:
        """
        自动检测模板版本

        Args:
            template_id: 模板ID

        Returns:
            版本号 ('v1' 或 'v2')
        """
        if template_id in self.V1_TEMPLATES:
            return "v1"
        elif template_id in self.V2_TEMPLATES:
            return "v2"
        else:
            raise ValueError(f"不支持的模板ID: {template_id}")

    def _get_req_key(self, template_id: str) -> str:
        """
        根据模板ID获取对应的req_key

        Args:
            template_id: 模板ID

        Returns:
            对应的req_key
        """
        version = self._detect_template_version(template_id)
        if version == "v1":
            return "i2v_bytedance_effects_v1"
        else:  # v2
            return "i2v_template_cv_v2"

    def _is_dual_template(self, template_id: str) -> bool:
        """
        检查是否为双图模板

        Args:
            template_id: 模板ID

        Returns:
            是否为双图模板
        """
        version = self._detect_template_version(template_id)
        if version == "v1":
            return template_id in self.V1_DUAL_TEMPLATES
        else:  # v2
            return template_id in self.V2_DUAL_TEMPLATES

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
        credential_scope = f"{date_stamp}/cn-north-1/cv/request"
        string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

        # 计算签名
        k_date = hmac.new(self.secret_key.encode('utf-8'), date_stamp.encode('utf-8'), hashlib.sha256).digest()
        k_region = hmac.new(k_date, 'cn-north-1'.encode('utf-8'), hashlib.sha256).digest()
        k_service = hmac.new(k_region, 'cv'.encode('utf-8'), hashlib.sha256).digest()
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

    def _make_request(self, method: str, action: str, req_key: str, version: str = "2022-08-31", data: Optional[Dict] = None, task_id: Optional[str] = None) -> Dict:
        """
        发送API请求

        Args:
            method: HTTP方法
            action: API动作
            req_key: 服务标识
            version: API版本
            data: 请求数据
            task_id: 任务ID

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
        url = f"https://visual.volcengineapi.com?{query_params}"

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

    @retry(max_retries=3, delay=2)
    def submit_task(self, image_url: str, template_id: str, final_stitch_switch: bool = True) -> str:
        """
        提交特效视频生成任务

        Args:
            image_url: 图片URL链接，双图模板使用'|'分隔
            template_id: 特效模板ID
            final_stitch_switch: 分屏设置（仅V2版本支持）

        Returns:
            任务ID
        """
        # 参数验证
        if not image_url:
            raise ValueError("图片URL不能为空")

        if not template_id:
            raise ValueError("模板ID不能为空")

        # 自动检测模板版本
        version = self._detect_template_version(template_id)
        req_key = self._get_req_key(template_id)
        is_dual_template = self._is_dual_template(template_id)

        print(f"使用{version.upper()}版本接口: {self.ALL_TEMPLATES[template_id]}")

        # 验证双图模板的图片URL
        if is_dual_template:
            if "|" not in image_url:
                raise ValueError(f"模板 '{template_id}' 需要两张图片链接，请用'|'分隔，例如：'https://person1.jpg|https://person2.png'")

            urls = image_url.split("|")
            if len(urls) != 2:
                raise ValueError(f"模板 '{template_id}' 需要恰好两张图片链接")

            # 验证两个URL
            for url in urls:
                if not validate_url(url.strip()):
                    raise ValueError(f"图片URL格式不正确: {url}")
        else:
            # 单图模板验证
            if "|" in image_url:
                raise ValueError(f"模板 '{template_id}' 只支持单张图片，不能包含'|'分隔符")

            if not validate_url(image_url):
                raise ValueError("图片URL格式不正确")

        # 构建请求数据
        data = {
            "image_input": image_url,
            "template_id": template_id
        }

        # V2版本支持final_stitch_switch参数
        if version == "v2":
            # 注意：emoji小人变身_480p不支持分屏功能
            if template_id == "multi_style_stacking_dolls":
                print("⚠️ 注意：emoji小人变身_480p模板不支持开启分屏")
                data["final_stitch_switch"] = True
            else:
                data["final_stitch_switch"] = final_stitch_switch
        else:
            # V1版本不支持final_stitch_switch参数
            if template_id.startswith("multi_style_stacking_dolls"):
                print("⚠️ V1版本不支持分屏设置参数")

        try:
            response = self._make_request(
                "POST",
                "CVSync2AsyncSubmitTask",
                req_key,
                data=data
            )

            if response.get("code") != 10000:
                error_msg = response.get("message", "未知错误")
                raise Exception(f"任务提交失败: {error_msg}")

            task_id = response["data"]["task_id"]
            print(f"特效视频任务已提交，任务ID: {task_id}")
            if is_dual_template:
                print(f"💕 使用双图模式，已传入2张图片")
            return task_id

        except Exception as e:
            raise Exception(f"提交任务失败: {str(e)}")

    def get_task_req_key(self, task_id: str) -> str:
        """
        根据任务ID获取对应的req_key
        这里需要先尝试V2，再尝试V1

        Args:
            task_id: 任务ID

        Returns:
            对应的req_key
        """
        v2_error = None
        v1_error = None

        # 先尝试V2版本
        try:
            response = self._make_request(
                "POST",
                "CVSync2AsyncGetResult",
                "i2v_template_cv_v2",
                task_id=task_id
            )
            return f"i2v_template_cv_v2|{response}"
        except Exception as e:
            v2_error = e

        # 再尝试V1版本
        try:
            response = self._make_request(
                "POST",
                "CVSync2AsyncGetResult",
                "i2v_bytedance_effects_v1",
                task_id=task_id
            )
            return f"i2v_bytedance_effects_v1|{response}"
        except Exception as e:
            v1_error = e

        # 直接抛出原始异常
        raise Exception(f"V2: {v2_error} | V1: {v1_error}")

    @retry(max_retries=3, delay=2)
    def get_result(self, task_id: str, req_key: str = None) -> Dict[str, Any]:
        """
        获取任务结果

        Args:
            task_id: 任务ID
            req_key: 服务标识（可选，如果不提供会自动检测）

        Returns:
            任务结果
        """
        try:
            # 如果没有提供req_key，尝试自动检测
            if not req_key:
                req_key_result = self.get_task_req_key(task_id)
                if "|" in req_key_result:
                    req_key, response = req_key_result.split("|", 1)
                    # 尝试解析JSON，如果失败则返回原始响应
                    try:
                        return json.loads(response)
                    except:
                        # 如果JSON解析失败，说明这可能不是完整的JSON响应
                        # 或者响应格式有问题，直接用检测到的req_key重新查询
                        req_key = req_key
                else:
                    req_key = req_key_result

            response = self._make_request(
                "POST",
                "CVSync2AsyncGetResult",
                req_key,
                task_id=task_id
            )

            # API返回的是JSON格式，直接返回字典对象
            return response

        except Exception as e:
            raise Exception(f"获取结果失败: {str(e)}")

    def wait_for_completion(self, task_id: str, max_wait_time: int = 600, check_interval: int = 15, req_key: str = None) -> Dict[str, Any]:
        """
        等待任务完成

        Args:
            task_id: 任务ID
            max_wait_time: 最大等待时间（秒）
            check_interval: 检查间隔（秒）

        Returns:
            任务结果
        """
        start_time = time.time()
        req_key = None  # 缓存检测到的req_key

        while time.time() - start_time < max_wait_time:
            try:
                result = self.get_result(task_id, req_key)

                # 直接显示API完整响应
                print(f"API响应: {result}")

                # 检查是否完成
                if result.get("code") == 10000:  # 成功
                    data = result.get("data", {})
                    status = data.get("status")

                    if status == "done":
                        return result
                    elif status in ["not_found", "expired"]:
                        raise Exception(f"任务异常: {status}")
                    else:
                        # 任务还在处理中，继续等待
                        if not req_key:
                            # 自动检测req_key
                            req_key = self.get_task_req_key(task_id)
                            # 版本检测返回格式为"req_key|response"，需要提取req_key
                            if "|" in req_key:
                                req_key = req_key.split("|")[0]
                else:
                    # API返回错误，直接抛出异常
                    raise Exception(f"API错误: {result}")

                time.sleep(check_interval)

            except Exception as e:
                if "任务异常" in str(e):
                    raise
                print(f"检查任务状态时出错: {str(e)}")
                time.sleep(check_interval)

        raise TimeoutError(f"等待任务完成超时 ({max_wait_time}秒)")

    def generate_video_from_image(self, image_url: str, template_id: str, final_stitch_switch: bool = True, max_wait_time: int = 600) -> Dict[str, Any]:
        """
        从图片生成特效视频（完整流程）

        Args:
            image_url: 图片URL链接
            template_id: 特效模板ID
            final_stitch_switch: 分屏设置
            max_wait_time: 最大等待时间（秒）

        Returns:
            生成结果
        """
        print(f"开始生成特效视频（模板: {template_id}）")

        # 步骤1：提交任务
        task_id = self.submit_task(image_url, template_id, final_stitch_switch)

        # 步骤2：等待完成，直接使用对应的req_key避免版本检测
        if template_id in self.V2_TEMPLATES:
            req_key = "i2v_template_cv_v2"
        else:
            req_key = "i2v_bytedance_effects_v1"
        result = self.wait_for_completion(task_id, max_wait_time, 15, req_key)

        if result.get("code") == 10000:
            data = result.get("data", {})
            if data.get("status") == "done":
                print("🎉 特效视频生成成功！")
                # resp_data是JSON字符串，需要解析
                import json
                resp_data_str = data.get("resp_data", "{}")
                try:
                    resp_data = json.loads(resp_data_str)
                except:
                    resp_data = {"raw": resp_data_str}
                video_url = resp_data.get("video_url")
                print(f"📹 视频URL: {video_url}")
                return {
                    "video_url": video_url,
                    "task_id": task_id,
                    "resp_data": resp_data
                }
            else:
                raise Exception(f"视频生成未完成: {result}")
        else:
            raise Exception(f"视频生成失败: {result}")