#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
火山引擎VolcEngine通用基础客户端
提供所有VolcEngine服务的通用功能：签名、请求、错误处理等
"""

import json
import hmac
import hashlib
import requests
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from ..utils import validate_url


class BaseVolcengineClient:
    """
    火山引擎VolcEngine通用基础客户端

    提供所有VolcEngine服务的通用功能：
    - HMAC-SHA256签名生成
    - HTTP请求处理
    - 错误处理和重试机制
    - 参数验证
    """

    def __init__(self, access_key: str, secret_key: str):
        """
        初始化基础客户端

        Args:
            access_key: 火山引擎访问密钥
            secret_key: 火山引擎秘密密钥
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = "https://visual.volcengineapi.com"
        self.region = "cn-north-1"
        self.service = "cv"

    def _make_request(self, method: str, action: str, req_key: str, version: str = "2022-08-31", data: Optional[Dict] = None, task_id: Optional[str] = None, req_json: Optional[str] = None) -> Dict:
        """
        发送API请求

        Args:
            method: HTTP方法
            action: API动作
            req_key: 服务标识
            version: API版本
            data: 请求数据
            task_id: 任务ID
            req_json: 请求JSON配置

        Returns:
            API响应
        """
        # 构建查询参数
        query_params = f"Action={action}&Version={version}"

        # 构建请求体
        body_data = {'req_key': req_key}
        if task_id:
            body_data['task_id'] = task_id
        if req_json:
            body_data['req_json'] = req_json
        if data:
            body_data.update(data)

        # 构建请求头（X-Content-Sha256基于完整的请求体）
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'visual.volcengineapi.com',
            'X-Content-Sha256': hashlib.sha256(json.dumps(body_data, ensure_ascii=False).encode('utf-8')).hexdigest()
        }

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
            response = requests.post(url, headers=headers, data=body, timeout=30)
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

    def _validate_url(self, url: str) -> bool:
        """
        验证URL格式

        Args:
            url: 要验证的URL

        Returns:
            True if URL格式正确, False otherwise
        """
        return validate_url(url)

    def _validate_image_url(self, url: str) -> None:
        """
        验证图片URL并抛出异常

        Args:
            url: 图片URL

        Raises:
            ValueError: URL格式不正确
        """
        if not self._validate_url(url):
            raise ValueError("图片URL格式不正确")

    def _validate_video_url(self, url: str) -> None:
        """
        验证视频URL并抛出异常

        Args:
            url: 视频URL

        Raises:
            ValueError: URL格式不正确
        """
        if not self._validate_url(url):
            raise ValueError("视频URL格式不正确")

    def _validate_audio_url(self, url: str) -> None:
        """
        验证音频URL并抛出异常

        Args:
            url: 音频URL

        Raises:
            ValueError: URL格式不正确
        """
        if not self._validate_url(url):
            raise ValueError("音频URL格式不正确")