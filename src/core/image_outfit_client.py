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
    火山引擎图片换装客户端 (支持V1版和V2版)

    功能：基于服装图片更换到指定模特图上
    - V1版：同步接口，单件服装
    - V2版：异步接口，支持多件服装（上衣+下衣）
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

        # V1版配置
        self.V1_CONFIG = {
            "req_key": "dressing_diffusion",
            "name": "图片换装V1",
            "description": "基于服装图片更换到指定模特图上（同步接口）",
            "version": "V1",
            "supported_formats": ["JPG", "JPEG", "PNG", "JFIF"],
            "max_file_size": 5,  # MB
            "max_resolution": 4096,  # 4096*4096
            "price": 1.0,  # 元/次
            "max_garments": 1,
            "features": [
                "支持复杂模特pose",
                "支持任意品类服装图",
                "支持非服饰类输入",
                "自动生成褶皱和光影",
                "同步返回结果"
            ]
        }

        # V2版配置
        self.V2_CONFIG = {
            "req_key": "dressing_diffusionV2",
            "name": "图片换装V2",
            "description": "基于服装图片更换到指定模特图上（异步接口，支持多件服装）",
            "version": "V2",
            "supported_formats": ["JPG", "JPEG", "PNG", "JFIF"],
            "max_file_size": 5,  # MB
            "max_resolution": 4096,  # 4096*4096
            "price": 1.0,  # 元/次
            "max_garments": 2,  # 支持上衣+下衣
            "features": [
                "支持复杂模特pose",
                "支持多件服装组合（上衣+下衣）",
                "支持服装类型分类",
                "异步任务模式",
                "丰富的推理参数",
                "自动生成褶皱和光影",
                "支持保护区域配置"
            ]
        }

        # 默认使用V1版
        self.REQ_KEY = self.V1_CONFIG["req_key"]
        self.CONFIG = self.V1_CONFIG

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

    def submit_outfit_task_v2(
        self,
        garment_urls: list,
        model_url: str = None,
        garment_types: list = None,
        model_id: str = None,
        protect_mask_url: str = None,
        inference_config: Optional[Dict] = None,
        req_image_store_type: int = 1,
        binary_data_base64: list = None
    ) -> Dict[str, Any]:
        """
        提交图片换装任务 (V2版异步API)

        Args:
            garment_urls: 服装图片URL列表，最多支持2件服装
            model_url: 模特图片URL（req_image_store_type=1时必选）
            garment_types: 服装类型列表，取值：["upper", "bottom", "full"]
            model_id: 模特ID（可选）
            protect_mask_url: 模特保护区域图URL（可选）
            inference_config: 推理配置
            req_image_store_type: 图片传入方式（0:base64, 1:URL）
            binary_data_base64: base64图片数据列表（req_image_store_type=0时使用）

        Returns:
            任务提交结果，包含task_id

        Raises:
            ValueError: 参数验证失败
            Exception: 任务提交失败
        """
        # 设置V2版服务标识
        self.REQ_KEY = self.V2_CONFIG["req_key"]

        # 参数验证
        if req_image_store_type == 1 and not model_url:
            raise ValueError("URL模式时，模特图片URL不能为空")

        if not garment_urls or len(garment_urls) == 0:
            raise ValueError("服装图片URL不能为空")

        if len(garment_urls) > self.V2_CONFIG["max_garments"]:
            raise ValueError(f"V2版最多支持{self.V2_CONFIG['max_garments']}件服装")

        # 如果没有提供服装类型，默认都是full
        if not garment_types:
            garment_types = ["full"] * len(garment_urls)

        if len(garment_types) != len(garment_urls):
            raise ValueError("服装类型数量必须与服装图片数量一致")

        # 验证服装类型
        valid_types = ["upper", "bottom", "full"]
        for garment_type in garment_types:
            if garment_type not in valid_types:
                raise ValueError(f"服装类型'{garment_type}'无效，支持：{valid_types}")

        # 如果使用URL模式，验证URL格式
        if req_image_store_type == 1:
            self._validate_image_url(model_url)
            for garment_url in garment_urls:
                self._validate_image_url(garment_url)

        # 默认推理配置 - 按照V2版官方文档设置
        default_inference_config = {
            "do_sr": False,
            "seed": -1,
            "keep_head": True,
            "keep_hand": False,  # V2版默认为False
            "keep_foot": False,  # V2版默认为False
            "num_steps": 16,  # V2版默认为16
            "keep_upper": False,
            "keep_lower": False,
            "tight_mask": "loose",
            "p_bbox_iou_ratio": 0.3,
            "p_bbox_expand_ratio": 1.1,
            "max_process_side_length": 1920
        }

        # 合并推理配置
        final_inference_config = default_inference_config.copy()
        if inference_config:
            final_inference_config.update(inference_config)

        # 构建服装数据
        garment_data = []
        for i, (garment_url, garment_type) in enumerate(zip(garment_urls, garment_types)):
            data_item = {
                "type": garment_type
            }
            if req_image_store_type == 1:  # URL模式
                data_item["url"] = garment_url
            garment_data.append(data_item)

        # 构建请求数据
        data = {
            "req_key": self.REQ_KEY,
            "garment": {
                "data": garment_data
            },
            "req_image_store_type": req_image_store_type,
            "inference_config": final_inference_config
        }

        # 添加模特配置（URL模式或提供了model_id）
        if req_image_store_type == 1 or model_id:
            model_config = {}
            if req_image_store_type == 1:
                model_config["url"] = model_url
            if model_id:
                model_config["id"] = model_id
            if protect_mask_url:
                model_config["protect_mask_url"] = protect_mask_url
            data["model"] = model_config

        # 添加base64数据（base64模式）
        if req_image_store_type == 0 and binary_data_base64:
            data["binary_data_base64"] = binary_data_base64

        try:
            # V2版使用CVSubmitTask接口，异步返回task_id
            response = self._make_request("POST", "CVSubmitTask", self.REQ_KEY, data=data)

            if response.get("code") != 10000:
                error_msg = response.get("message", "未知错误")
                raise Exception(f"图片换装任务提交失败: {error_msg}")

            # 恢复V1版服务标识
            self.REQ_KEY = self.V1_CONFIG["req_key"]

            return response["data"]

        except Exception as e:
            # 恢复V1版服务标识
            self.REQ_KEY = self.V1_CONFIG["req_key"]
            raise Exception(f"图片换装任务提交失败: {str(e)}")

    def query_outfit_task_v2(
        self,
        task_id: str,
        return_url: bool = True,
        logo_info: Optional[Dict] = None,
        aigc_meta: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        查询图片换装任务状态 (V2版异步API)

        Args:
            task_id: 任务ID
            return_url: 是否返回图片链接
            logo_info: 水印信息配置
            aigc_meta: 隐式标识配置

        Returns:
            任务查询结果

        Raises:
            Exception: 查询失败
        """
        # 设置V2版服务标识
        self.REQ_KEY = self.V2_CONFIG["req_key"]

        # 默认水印配置
        default_logo_info = {
            "add_logo": False,
            "position": 0,
            "language": 0,
            "opacity": 1.0,
            "logo_text_content": "这里是明水印内容"
        }

        # 合并水印配置
        final_logo_info = default_logo_info.copy()
        if logo_info:
            final_logo_info.update(logo_info)

        # 构建req_json
        req_json = {
            "return_url": return_url,
            "logo_info": final_logo_info
        }

        # 添加隐式标识
        if aigc_meta:
            req_json["aigc_meta"] = aigc_meta

        # 构建请求数据
        data = {
            "req_key": self.REQ_KEY,
            "task_id": task_id,
            "req_json": json.dumps(req_json)
        }

        try:
            # V2版使用CVGetResult接口查询结果
            response = self._make_request("POST", "CVGetResult", self.REQ_KEY, data=data)

            # 恢复V1版服务标识
            self.REQ_KEY = self.V1_CONFIG["req_key"]

            if response.get("code") != 10000:
                error_msg = response.get("message", "未知错误")
                raise Exception(f"查询任务状态失败: {error_msg}")

            return response["data"]

        except Exception as e:
            # 恢复V1版服务标识
            self.REQ_KEY = self.V1_CONFIG["req_key"]
            raise Exception(f"查询任务状态失败: {str(e)}")

    def generate_outfit_image_v2(
        self,
        garment_urls: list,
        model_url: str = None,
        garment_types: list = None,
        return_url: bool = True,
        model_id: str = None,
        protect_mask_url: str = None,
        inference_config: Optional[Dict] = None,
        logo_info: Optional[Dict] = None,
        aigc_meta: Optional[Dict] = None,
        download: bool = True,
        filename: Optional[str] = None,
        req_image_store_type: int = 1
    ) -> Optional[str]:
        """
        一键生成换装图片 (V2版异步接口)

        Args:
            garment_urls: 服装图片URL列表，最多支持2件服装
            model_url: 模特图片URL（req_image_store_type=1时必选）
            garment_types: 服装类型列表，取值：["upper", "bottom", "full"]
            return_url: 是否返回图片链接
            model_id: 模特ID
            protect_mask_url: 模特保护区域图URL
            inference_config: 推理配置
            logo_info: 水印配置
            aigc_meta: 隐式标识配置
            download: 是否下载图片
            filename: 保存文件名
            req_image_store_type: 图片传入方式（0:base64, 1:URL）

        Returns:
            下载的文件名或图片URL

        Raises:
            Exception: 换装失败或下载失败
        """
        import time

        try:
            # 提交换装任务
            result = self.submit_outfit_task_v2(
                garment_urls=garment_urls,
                model_url=model_url,
                garment_types=garment_types,
                model_id=model_id,
                protect_mask_url=protect_mask_url,
                inference_config=inference_config,
                req_image_store_type=req_image_store_type
            )

            task_id = result.get("task_id")
            if not task_id:
                raise Exception("任务提交成功但未获取到task_id")

            print(f"✅ 换装任务已提交，任务ID: {task_id}")

            # 查询任务状态（循环等待直到完成）
            start_time = time.time()
            max_wait_time = 600  # 10分钟超时
            check_interval = 15  # 15秒检查一次

            while time.time() - start_time < max_wait_time:
                print(f"⏳ 查询任务状态... (已等待 {int(time.time() - start_time)}秒)")

                query_result = self.query_outfit_task_v2(
                    task_id=task_id,
                    return_url=return_url,
                    logo_info=logo_info,
                    aigc_meta=aigc_meta
                )

                status = query_result.get("status", "")

                if status == "done":
                    print("🎉 换装任务完成！")

                    # 获取图片URL
                    image_urls = query_result.get("image_urls", [])
                    if not image_urls:
                        raise Exception("任务完成但未获取到图片URL")

                    image_url = image_urls[0]

                    if download:
                        # 下载图片
                        if not filename:
                            timestamp = int(time.time())
                            filename = f"outfit_v2_{timestamp}.png"

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

                elif status in ["in_queue", "generating"]:
                    # 继续等待
                    time.sleep(check_interval)
                    continue

                elif status == "not_found":
                    raise Exception("任务未找到，可能原因：无此任务或任务已过期(12小时)")

                elif status == "expired":
                    raise Exception("任务已过期，请尝试重新提交任务请求")

                else:
                    # 检查是否有错误信息
                    resp_data = query_result.get("resp_data", "")
                    if resp_data:
                        try:
                            resp_data_dict = json.loads(resp_data)
                            if resp_data_dict.get("code") != 0:
                                error_msg = resp_data_dict.get("message", "未知错误")
                                raise Exception(f"换装失败: {error_msg}")
                        except json.JSONDecodeError:
                            pass

                    raise Exception(f"任务状态异常: {status}")

            else:
                raise Exception("任务处理超时，请稍后手动查询结果")

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
            print("🎉 图片换装V1版功能测试完成！")

    except Exception as e:
        print(f"❌ 图片换装V1版测试失败: {str(e)}")

    # V2版测试示例
    try:
        print("\n" + "=" * 50)
        print("测试图片换装V2版（异步接口）")
        print("=" * 50)

        # 测试参数
        MODEL_URL = "https://example.com/model.jpg"  # 替换为实际的模特图片URL
        UPPER_GARMENT_URL = "https://example.com/upper.jpg"  # 替换为实际的上衣图片URL
        BOTTOM_GARMENT_URL = "https://example.com/bottom.jpg"  # 替换为实际的下衣图片URL

        # 服装类型列表
        garment_types = ["upper", "bottom"]

        # V2版推理配置
        v2_config = {
            "num_steps": 20,  # 增加推理步数以提升质量
            "seed": 54321,  # 固定随机种子
            "keep_head": True,
            "keep_hand": False,  # V2版默认为False
            "keep_foot": False,  # V2版默认为False
            "tight_mask": "loose",
            "p_bbox_iou_ratio": 0.3,
            "p_bbox_expand_ratio": 1.1,
            "max_process_side_length": 1920
        }

        # 一键生成V2版换装图片（多件服装）
        result_v2 = client.generate_outfit_image_v2(
            garment_urls=[UPPER_GARMENT_URL, BOTTOM_GARMENT_URL],
            model_url=MODEL_URL,
            garment_types=garment_types,
            inference_config=v2_config,
            download=True,
            filename="my_outfit_v2_result.png"
        )

        if result_v2:
            print("🎉 图片换装V2版功能测试完成！")

    except Exception as e:
        print(f"❌ 图片换装V2版测试失败: {str(e)}")