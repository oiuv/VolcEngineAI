#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
火山引擎图片换装客户端
支持基于服装图片更换到指定模特图上生成换装效果
实现V1版API: dressing_diffusion
"""

import json
from typing import Dict, Any, Optional

from .base_volcengine_client import BaseVolcengineClient


class ImageOutfitClient(BaseVolcengineClient):
    """
    火山引擎图片换装客户端 (V1版)

    功能：基于服装图片更换到指定模特图上
    - 输入：模特图 + 服装图
    - 输出：模特穿着指定服装的图片
    - 支持各种姿势、画幅的模特图
    - 支持平铺图、挂拍图、上身图等服装图类型
    """

    def __init__(self, access_key: str, secret_key: str):
        """
        初始化图片换装客户端

        Args:
            access_key: 火山引擎访问密钥
            secret_key: 火山引擎秘密密钥
        """
        super().__init__(access_key, secret_key)

        # 服务标识
        self.REQ_KEY = "dressing_diffusion"

        # 配置信息
        self.CONFIG = {
            "name": "图片换装",
            "description": "基于服装图片更换到指定模特图上",
            "version": "V1",
            "supported_formats": ["JPG", "JPEG", "PNG", "JFIF"],
            "max_file_size": 5,  # MB
            "max_resolution": 4096,  # 4096*4096
            "price": 1.0,  # 元/次
            "features": [
                "支持复杂模特pose",
                "支持任意品类服装图",
                "支持非服饰类输入",
                "自动生成褶皱和光影"
            ]
        }

    def submit_outfit_task(
        self,
        model_url: str,
        garment_url: str,
        return_url: bool = True,
        model_id: str = "1",
        garment_id: str = "1",
        inference_config: Optional[Dict] = None,
        logo_info: Optional[Dict] = None,
        aigc_meta: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        提交图片换装任务 (V1版同步API)

        Args:
            model_url: 模特图片URL（需公网可访问）
            garment_url: 服装图片URL（需公网可访问）
            return_url: 是否返回图片链接
            model_id: 模特ID，建议值："1"
            garment_id: 服装ID，建议值："1"
            inference_config: 推理配置
            logo_info: 水印信息配置
            aigc_meta: 隐式标识配置

        Returns:
            换装结果，包含图片URL

        Raises:
            ValueError: 参数验证失败
            Exception: 换装失败
        """
        # 参数验证
        self._validate_image_url(model_url)
        self._validate_image_url(garment_url)

        # 默认推理配置 - 按照官方文档设置
        default_inference_config = {
            "do_sr": False,
            "seed": -1,
            "keep_head": True,
            "keep_hand": True,
            "keep_foot": True,
            "num_steps": 50,
            "keep_upper": False,
            "keep_lower": False,
            "tight_mask": "loose"
        }

        # 合并推理配置
        final_inference_config = default_inference_config.copy()
        if inference_config:
            final_inference_config.update(inference_config)

        # 默认水印配置
        default_logo_info = {
            "add_logo": False,
            "position": 0,
            "language": 0,
            "logo_text_content": "这里是明水印内容"
        }

        # 合并水印配置
        final_logo_info = default_logo_info.copy()
        if logo_info:
            final_logo_info.update(logo_info)

        # 构建请求数据
        data = {
            "req_key": self.REQ_KEY,
            "model": {
                "id": model_id,
                "url": model_url
            },
            "garment": {
                "id": garment_id,
                "data": [
                    {
                        "url": garment_url
                    }
                ]
            },
            "return_url": return_url,
            "logo_info": final_logo_info,
            "inference_config": final_inference_config
        }

        # 添加隐式标识
        if aigc_meta:
            data["aigc_meta"] = aigc_meta

        try:
            # V1版使用CVProcess接口，同步返回结果
            response = self._make_request("POST", "CVProcess", self.REQ_KEY, data=data)

            if response.get("code") != 10000:
                error_msg = response.get("message", "未知错误")
                raise Exception(f"图片换装失败: {error_msg}")

            # 直接返回完整的原始API响应
            return response["data"]

        except Exception as e:
            raise Exception(f"图片换装失败: {str(e)}")

    def generate_outfit_image(
        self,
        model_url: str,
        garment_url: str,
        return_url: bool = True,
        model_id: str = "1",
        garment_id: str = "1",
        inference_config: Optional[Dict] = None,
        logo_info: Optional[Dict] = None,
        aigc_meta: Optional[Dict] = None,
        download: bool = True,
        filename: Optional[str] = None
    ) -> Optional[str]:
        """
        一键生成换装图片

        Args:
            model_url: 模特图片URL
            garment_url: 服装图片URL
            return_url: 是否返回图片链接
            model_id: 模特ID
            garment_id: 服装ID
            inference_config: 推理配置
            logo_info: 水印配置
            aigc_meta: 隐式标识配置
            download: 是否下载图片
            filename: 保存文件名

        Returns:
            下载的文件名或图片URL

        Raises:
            Exception: 换装失败或下载失败
        """
        try:
            # 提交换装任务
            result = self.submit_outfit_task(
                model_url=model_url,
                garment_url=garment_url,
                return_url=return_url,
                model_id=model_id,
                garment_id=garment_id,
                inference_config=inference_config,
                logo_info=logo_info,
                aigc_meta=aigc_meta
            )

            # 获取图片URL
            image_urls = result.get("image_urls", [])
            if not image_urls:
                raise Exception("换装成功但未获取到图片URL")

            image_url = image_urls[0]

            if download:
                # 下载图片
                if not filename:
                    import time
                    timestamp = int(time.time())
                    filename = f"outfit_{timestamp}.png"

                try:
                    # 使用现有的download_image函数
                    from ..utils import download_image
                    downloaded_file = download_image(image_url, filename)
                    print(f"✅ 换装图片已保存到: {downloaded_file}")
                    return downloaded_file
                except Exception as e:
                    raise Exception(f"下载图片失败: {str(e)}")
            else:
                print(f"✅ 换装图片URL: {image_url}")
                return image_url

        except Exception as e:
            raise Exception(f"生成换装图片失败: {str(e)}")


# 示例使用代码
if __name__ == "__main__":
    # 配置示例
    ACCESS_KEY = "your_access_key_here"
    SECRET_KEY = "your_secret_key_here"

    # 测试参数
    MODEL_URL = "https://example.com/model.jpg"  # 替换为实际的模特图片URL
    GARMENT_URL = "https://example.com/garment.jpg"  # 替换为实际的服装图片URL

    # 初始化客户端
    client = ImageOutfitClient(ACCESS_KEY, SECRET_KEY)

    try:
        # AIGC隐式标识配置（可选）
        aigc_meta = {
            "content_producer": "your_producer_id",
            "producer_id": "unique_producer_id_123",
            "content_propagator": "your_propagator_id",
            "propagate_id": "unique_propagate_id_456"
        }

        # 自定义推理配置（可选）
        custom_config = {
            "num_steps": 40,  # 减少推理步数以加快速度
            "seed": 12345,  # 固定随机种子以获得可重现的结果
            "keep_head": True,
            "keep_hand": True,
            "keep_foot": False
        }

        # 一键生成换装图片
        result = client.generate_outfit_image(
            model_url=MODEL_URL,
            garment_url=GARMENT_URL,
            inference_config=custom_config,
            aigc_meta=aigc_meta,
            download=True,
            filename="my_outfit_result.png"
        )

        if result:
            print("🎉 图片换装功能测试完成！")

    except Exception as e:
        print(f"❌ 图片换装失败: {str(e)}")