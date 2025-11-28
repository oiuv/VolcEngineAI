"""
火山引擎AI统一入口
支持多种AI功能：单图音频驱动、图像生成、文本模型等
"""

import os
import sys
import time
import argparse
import requests
from typing import Dict, Any, Optional, List

from src.config import ACCESS_KEY, SECRET_KEY
from src.modules.avatar_manager import avatar_manager


class VolcEngineAI:
    """火山引擎AI统一客户端"""

    def __init__(self, access_key: str = None, secret_key: str = None):
        """初始化客户端"""
        self.access_key = access_key or ACCESS_KEY
        self.secret_key = secret_key or SECRET_KEY

        # 动态导入模块
        self._avatar_client = None
        self._lip_sync_client = None
        self._init_clients()

    def _init_clients(self):
        """初始化各个功能模块的客户端"""
        # 延迟导入，避免循环依赖
        try:
            from src.core.video_audio_driven_client import VideoAudioDrivenClient
            self._avatar_client = VideoAudioDrivenClient(self.access_key, self.secret_key)
        except ImportError:
            self._avatar_client = None

        try:
            from src.core.video_lip_sync_client import VideoLipSyncClient
            self._lip_sync_client = VideoLipSyncClient(self.access_key, self.secret_key)
        except ImportError:
            self._lip_sync_client = None

        try:
            from src.core.jimeng_omni_client import VideoJimengClient
            self._jimeng_client = VideoJimengClient(self.access_key, self.secret_key)
        except ImportError:
            self._jimeng_client = None

        try:
            from src.core.jimeng_mimic_client import VideoJimengMimicClient
            self._jimeng_mimic_client = VideoJimengMimicClient(self.access_key, self.secret_key)
        except ImportError:
            self._jimeng_mimic_client = None

        try:
            from src.core.video_effect_client import VideoEffectClient
            self._effect_client = VideoEffectClient(self.access_key, self.secret_key)
        except ImportError:
            self._effect_client = None

        try:
            from src.core.video_video_driven_client import VideoVideoDrivenClient
            self._video_driven_client = VideoVideoDrivenClient(self.access_key, self.secret_key)
        except ImportError:
            self._video_driven_client = None

        try:
            from src.core.image_outfit_client import ImageOutfitClient
            self._image_outfit_client = ImageOutfitClient(self.access_key, self.secret_key)
        except ImportError:
            self._image_outfit_client = None

    # 单图音频驱动功能
    def create_avatar(self, image_url: str, mode: str = "normal") -> str:
        """创建数字形象"""
        if not self._avatar_client:
            raise Exception("单图音频驱动模块未正确加载")
        return self._avatar_client.create_role(image_url, mode)

    def get_avatar_result(self, task_id: str, mode: str = "normal"):
        """获取形象创建结果"""
        if not self._avatar_client:
            raise Exception("单图音频驱动模块未正确加载")
        return self._avatar_client.get_role_result(task_id, mode)

    def generate_avatar_video(self, resource_id: str, audio_url: str, mode: str = "normal", aigc_meta: Optional[Dict] = None) -> str:
        """生成角色视频"""
        if not self._avatar_client:
            raise Exception("单图音频驱动模块未正确加载")
        return self._avatar_client.generate_video(resource_id, audio_url, mode, aigc_meta)

    def get_video_result(self, task_id: str, mode: str = "normal", aigc_meta: Optional[Dict] = None):
        """获取视频生成结果"""
        if not self._avatar_client:
            raise Exception("单图音频驱动模块未正确加载")
        return self._avatar_client.get_video_result(task_id, mode, aigc_meta)

    def generate_avatar_video_from_image_audio(self, image_url: str, audio_url: str, mode: str = "normal", aigc_meta: Optional[Dict] = None, max_wait_time: int = 600):
        """从图片和音频生成完整视频"""
        if not self._avatar_client:
            raise Exception("单图音频驱动模块未正确加载")
        return self._avatar_client.generate_video_from_image_audio(image_url, audio_url, mode, aigc_meta, max_wait_time)

    # 预留其他AI功能接口
    def image_generation(self, prompt: str, **kwargs):
        """图像生成（文生图）- 待实现"""
        raise NotImplementedError("图像生成功能待实现")

    def image_to_image(self, image_url: str, prompt: str, **kwargs):
        """图像生成（图生图）- 待实现"""
        raise NotImplementedError("图生图功能待实现")

    def image_effects(self, image_url: str, effect_type: str, **kwargs):
        """图像特效 - 待实现"""
        raise NotImplementedError("图像特效功能待实现")

    def image_style_transfer(self, image_url: str, style: str, **kwargs):
        """图像风格化 - 待实现"""
        raise NotImplementedError("图像风格化功能待实现")

    def image_outfit_change(self, image_url: str, outfit_type: str, **kwargs):
        """图片换装 - 待实现"""
        raise NotImplementedError("图片换装功能待实现")

    def image_cartoon(self, image_url: str, **kwargs):
        """智能绘图（漫画版）- 待实现"""
        raise NotImplementedError("漫画版功能待实现")

    def image_recognition(self, image_url: str, **kwargs):
        """图像识别与理解 - 待实现"""
        raise NotImplementedError("图像识别功能待实现")

    def image_processing(self, image_url: str, operation: str, **kwargs):
        """智能图像处理 - 待实现"""
        raise NotImplementedError("图像处理功能待实现")

    def text_generation(self, prompt: str, **kwargs):
        """文本生成 - 待实现"""
        raise NotImplementedError("文本生成功能待实现")

    def music_generation(self, prompt: str, **kwargs):
        """音乐生成 - 待实现"""
        raise NotImplementedError("音乐生成功能待实现")

    def video_generation(self, prompt: str, **kwargs):
        """视频生成 - 待实现"""
        raise NotImplementedError("视频生成功能待实现")

    def generate_effect_video(self, image_url: str, template_id: str, **kwargs):
        """生成创意特效视频"""
        if not self._effect_client:
            raise Exception("特效视频模块未正确加载")
        return self._effect_client.generate_video_from_image(image_url, template_id, **kwargs)

    def get_effect_video_result(self, task_id: str):
        """获取特效视频生成结果"""
        if not self._effect_client:
            raise Exception("特效视频模块未正确加载")
        return self._effect_client.get_result(task_id)

    # 视频改口型功能
    def submit_lip_sync_task(self, video_url: str, audio_url: str, mode: str = "lite", **kwargs) -> str:
        """提交视频改口型任务"""
        if not self._lip_sync_client:
            raise Exception("视频改口型模块未正确加载")
        return self._lip_sync_client.submit_lip_sync_task(video_url, audio_url, mode, **kwargs)

    def get_lip_sync_result(self, task_id: str, mode: str = "lite", aigc_meta: Optional[Dict] = None):
        """获取视频改口型结果"""
        if not self._lip_sync_client:
            raise Exception("视频改口型模块未正确加载")
        return self._lip_sync_client.get_lip_sync_result(task_id, mode, aigc_meta)

    def change_lip_sync(self, video_url: str, audio_url: str, mode: str = "lite", aigc_meta: Optional[Dict] = None, max_wait_time: int = 600, **kwargs):
        """视频改口型（完整流程）"""
        if not self._lip_sync_client:
            raise Exception("视频改口型模块未正确加载")
        return self._lip_sync_client.change_lip_sync(video_url, audio_url, mode, aigc_meta, max_wait_time, **kwargs)

    # 即梦AI数字人功能
    def jm_detect_avatar(self, image_url: str, version: str = "1.5"):
        """数字人形象识别"""
        if not self._jimeng_client:
            raise Exception("即梦AI模块未正确加载")
        return self._jimeng_client.detect_avatar(image_url, version)

    def jm_detect_object(self, image_url: str):
        """对象检测（1.5版专用）"""
        if not self._jimeng_client:
            raise Exception("即梦AI模块未正确加载")
        return self._jimeng_client.detect_object(image_url)

    def jm_create_video(self, image_url: str, audio_url: str, version: str = "1.5", prompt: Optional[str] = None, mask_url: Optional[List[str]] = None, seed: Optional[int] = None, pe_fast_mode: bool = False):
        """生成数字人视频（只提交任务，返回task_id）"""
        if not self._jimeng_client:
            raise Exception("即梦AI模块未正确加载")
        return self._jimeng_client.generate_video(image_url, audio_url, version, prompt, mask_url, seed, pe_fast_mode)

    def jm_query_result(self, task_id: str, operation_type: str = "generate", version: str = "1.5"):
        """查询即梦AI任务结果"""
        if not self._jimeng_client:
            raise Exception("即梦AI模块未正确加载")
        return self._jimeng_client.get_result(task_id, operation_type, version)

    def jm_mimic_submit_task(self, image_url: str, video_url: str) -> str:
        """提交动作模仿任务"""
        if not self._jimeng_mimic_client:
            raise Exception("即梦AI动作模仿模块未正确加载")
        return self._jimeng_mimic_client.submit_mimic_task(image_url, video_url)

    def jm_mimic_get_result(self, task_id: str) -> Dict[str, Any]:
        """获取动作模仿任务结果"""
        if not self._jimeng_mimic_client:
            raise Exception("即梦AI动作模仿模块未正确加载")
        return self._jimeng_mimic_client.get_mimic_result(task_id)

    # 单图视频驱动功能
    def submit_video_driven_task(self, image_url: str, video_url: str, aigc_meta: Optional[Dict] = None) -> str:
        """提交单图视频驱动任务"""
        if not self._video_driven_client:
            raise Exception("单图视频驱动模块未正确加载")
        return self._video_driven_client.submit_driven_task(image_url, video_url, aigc_meta)

    def get_video_driven_result(self, task_id: str, aigc_meta: Optional[Dict] = None) -> Dict[str, Any]:
        """获取单图视频驱动任务结果"""
        if not self._video_driven_client:
            raise Exception("单图视频驱动模块未正确加载")
        return self._video_driven_client.get_driven_result(task_id, aigc_meta)

    # 图片换装功能
    def submit_outfit_task(self, model_url: str, garment_url: str, return_url: bool = True,
                          model_id: str = "1", garment_id: str = "1",
                          inference_config: Optional[Dict] = None,
                          logo_info: Optional[Dict] = None,
                          aigc_meta: Optional[Dict] = None) -> Dict[str, Any]:
        """提交图片换装任务"""
        if not self._image_outfit_client:
            raise Exception("图片换装模块未正确加载")
        return self._image_outfit_client.submit_outfit_task(
            model_url=model_url,
            garment_url=garment_url,
            return_url=return_url,
            model_id=model_id,
            garment_id=garment_id,
            inference_config=inference_config,
            logo_info=logo_info,
            aigc_meta=aigc_meta
        )

    def generate_outfit_image(self, model_url: str, garment_url: str, return_url: bool = True,
                              model_id: str = "1", garment_id: str = "1",
                              inference_config: Optional[Dict] = None,
                              logo_info: Optional[Dict] = None,
                              aigc_meta: Optional[Dict] = None,
                              download: bool = True, filename: Optional[str] = None) -> Optional[str]:
        """一键生成换装图片"""
        if not self._image_outfit_client:
            raise Exception("图片换装模块未正确加载")
        return self._image_outfit_client.generate_outfit_image(
            model_url=model_url,
            garment_url=garment_url,
            return_url=return_url,
            model_id=model_id,
            garment_id=garment_id,
            inference_config=inference_config,
            logo_info=logo_info,
            aigc_meta=aigc_meta,
            download=download,
            filename=filename
        )

    def submit_outfit_task_v2(self, garment_urls: list, model_url: str = None,
                             garment_types: list = None, model_id: str = None,
                             protect_mask_url: str = None, inference_config: Optional[Dict] = None,
                             req_image_store_type: int = 1, binary_data_base64: list = None) -> Dict[str, Any]:
        """提交图片换装任务 (V2版)"""
        if not self._image_outfit_client:
            raise Exception("图片换装模块未正确加载")
        return self._image_outfit_client.submit_outfit_task_v2(
            garment_urls=garment_urls,
            model_url=model_url,
            garment_types=garment_types,
            model_id=model_id,
            protect_mask_url=protect_mask_url,
            inference_config=inference_config,
            req_image_store_type=req_image_store_type,
            binary_data_base64=binary_data_base64
        )

    def query_outfit_task_v2(self, task_id: str, return_url: bool = True,
                            logo_info: Optional[Dict] = None,
                            aigc_meta: Optional[Dict] = None) -> Dict[str, Any]:
        """查询图片换装任务状态 (V2版)"""
        if not self._image_outfit_client:
            raise Exception("图片换装模块未正确加载")
        return self._image_outfit_client.query_outfit_task_v2(
            task_id=task_id,
            return_url=return_url,
            logo_info=logo_info,
            aigc_meta=aigc_meta
        )

    def generate_outfit_image_v2(self, garment_urls: list, model_url: str = None,
                                garment_types: list = None, return_url: bool = True,
                                model_id: str = None, protect_mask_url: str = None,
                                inference_config: Optional[Dict] = None,
                                logo_info: Optional[Dict] = None,
                                aigc_meta: Optional[Dict] = None,
                                download: bool = True, filename: Optional[str] = None,
                                req_image_store_type: int = 1) -> Optional[str]:
        """一键生成换装图片 (V2版)"""
        if not self._image_outfit_client:
            raise Exception("图片换装模块未正确加载")
        return self._image_outfit_client.generate_outfit_image_v2(
            garment_urls=garment_urls,
            model_url=model_url,
            garment_types=garment_types,
            return_url=return_url,
            model_id=model_id,
            protect_mask_url=protect_mask_url,
            inference_config=inference_config,
            logo_info=logo_info,
            aigc_meta=aigc_meta,
            download=download,
            filename=filename,
            req_image_store_type=req_image_store_type
        )


def create_avatar(args):
    """创建形象（自动查询并等待完成）"""
    ai = VolcEngineAI()
    try:
        print(f"🎨 开始创建数字形象（{args.mode}模式）")
        print(f"📷 图片URL: {args.image_url}")

        task_id = ai.create_avatar(args.image_url, args.mode)
        print(f"✅ 形象创建任务已提交")
        print(f"🆔 任务ID: {task_id}")
        print("⏳ 正在等待处理完成...")

        # 自动查询并等待完成（调用现有的query_avatar逻辑）
        # 创建一个临时的args对象来传递给query_avatar
        class QueryArgs:
            def __init__(self):
                self.task_id = task_id
                self.mode = args.mode

        query_avatar(QueryArgs())

    except Exception as e:
        print(f"❌ 创建失败: {str(e)}")


def query_avatar(args):
    """查询形象状态"""
    ai = VolcEngineAI()
    try:
        print(f"🔍 查询任务ID: {args.task_id} ({args.mode}模式)")

        # 循环查询直到任务完成
        import time
        start_time = time.time()
        max_wait_time = 600  # 最大等待10分钟
        check_interval = 15  # 每15秒查询一次

        while time.time() - start_time < max_wait_time:
            try:
                result = ai.get_avatar_result(args.task_id, args.mode)

                # 显示当前状态
                if isinstance(result, dict):
                    status = result.get("status", "unknown")
                    if status == "done":
                        print(f"📋 API响应: {result}")

                        # 保存形象信息
                        if "resource_id" in result:
                            avatar_manager.save_avatar(args.task_id, result, args.mode, result.get("resp_data"))
                            print("\n🎉 数字形象创建完成！")
                            print("=" * 50)
                            print(f"🆔 形象ID: {result['resource_id']}")
                            print(f"🎭 形象类型: {result.get('role_type', 'unknown')}")
                            if result.get('face_position'):
                                print(f"📍 人脸位置: {result['face_position']}")
                            print("=" * 50)
                        return

                    elif status in ["not_found", "expired"]:
                        print(f"❌ 任务异常: {status}")
                        return

                    elif "resource_id" in result:
                        # 如果有resource_id说明任务已完成
                        print(f"📋 API响应: {result}")
                        avatar_manager.save_avatar(args.task_id, result, args.mode, result.get("resp_data"))
                        print("\n🎉 数字形象创建完成！")
                        print("=" * 50)
                        print(f"🆔 形象ID: {result['resource_id']}")
                        print("=" * 50)
                        return

                    else:
                        # 优先使用API返回的中文message，如果没有则使用status
                        message = result.get("message", f"任务状态: {status}")
                        print(f"⏳ 任务进行中... {message}")
                        print(f"📋 API响应: {result}")

                else:
                    print(f"⏳ 任务进行中... 状态: {result}")

                time.sleep(check_interval)

            except Exception as e:
                print(f"⚠️ 查询出错: {str(e)}，{check_interval}秒后重试...")
                time.sleep(check_interval)

        print(f"⏰ 等待超时 ({max_wait_time}秒)，任务可能仍在处理")
        print(f"💡 提示: 可手动继续查询: python volcengine_ai.py va query-avatar {args.task_id} --mode {args.mode}")

    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")


def generate_video(args):
    """生成视频"""
    ai = VolcEngineAI()
    try:
        task_id = ai.generate_avatar_video(args.resource_id, args.audio_url, args.mode)
        print(f"✅ 视频生成任务已提交")
        print(f"🆔 任务ID: {task_id}")
        return task_id
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")
        return None


def query_video(args):
    """查询视频状态（循环等待直到完成）"""
    import time
    ai = VolcEngineAI()
    start_time = time.time()
    max_wait_time = 600  # 10分钟
    check_interval = 15  # 15秒检查一次

    try:
        print(f"🔍 开始查询任务ID: {args.task_id} ({args.mode}模式)")
        print(f"⏰ 最大等待时间: {max_wait_time}秒，每{check_interval}秒检查一次")

        while time.time() - start_time < max_wait_time:
            try:
                result = ai.get_video_result(args.task_id, args.mode)
                print(f"📋 API响应: {result}")

                # 检查任务状态
                if isinstance(result, dict):
                    status = result.get("status", "unknown")
                    if status == "done":
                        print(f"✅ 任务完成！")

                        # 下载视频
                        if result.get("video_url"):
                            video_url = result["video_url"]
                            filename = args.filename or f"video_{args.task_id}.mp4"
                            download_video(video_url, filename)
                            print("\n🎉 视频生成完成！")
                            print("=" * 50)
                            print(f"🆔 任务ID: {args.task_id}")
                            print(f"📹 视频URL: {video_url}")
                            print("=" * 50)
                        return

                    elif status in ["not_found", "expired"]:
                        print(f"❌ 任务异常: {status}")
                        return

                    elif result.get("video_url"):
                        # 如果有video_url说明任务已完成
                        print(f"✅ 任务完成！")
                        video_url = result["video_url"]
                        filename = args.filename or f"video_{args.task_id}.mp4"
                        download_video(video_url, filename)
                        print("\n🎉 视频生成完成！")
                        print("=" * 50)
                        print(f"🆔 任务ID: {args.task_id}")
                        print("=" * 50)
                        return

                    else:
                        # 优先使用API返回的中文message，如果没有则使用status
                        message = result.get("message", f"任务状态: {status}")
                        print(f"⏳ 任务进行中... {message}")

                else:
                    print(f"⏳ 任务进行中... 状态: {result}")

                time.sleep(check_interval)

            except Exception as e:
                print(f"⚠️ 查询出错: {str(e)}，{check_interval}秒后重试...")
                time.sleep(check_interval)

        print(f"⏰ 等待超时 ({max_wait_time}秒)，任务可能仍在处理")
        print(f"💡 提示: 可手动继续查询: python volcengine_ai.py va query-video {args.task_id} --mode {args.mode}")

    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")


def download_video(url: str, filename: str):
    """下载视频到本地"""
    try:
        print(f"📥 开始下载视频到: {filename}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r📥 下载进度: {percent:.1f}%", end='', flush=True)

        print(f"\n✅ 视频下载完成: {filename}")
        print(f"📁 文件大小: {downloaded / (1024*1024):.1f} MB")

    except Exception as e:
        print(f"\n❌ 下载失败: {str(e)}")


def list_avatars(args):
    """列出保存的形象"""
    if args.mode:
        avatar_manager.list_avatars(args.mode)
    else:
        avatar_manager.list_avatars()


def use_latest_avatar(args):
    """使用最新的形象生成视频"""
    latest_avatar = avatar_manager.get_latest_avatar(args.mode)

    if not latest_avatar:
        print(f"❌ 未找到{args.mode + '模式' if args.mode else ''}的形象")
        print("💡 请先创建形象")
        return

    print(f"🎭 使用最新{latest_avatar.get('mode')}模式形象: {latest_avatar['resource_id']}")

    ai = VolcEngineAI()
    try:
        task_id = ai.generate_avatar_video(
            latest_avatar['resource_id'],
            args.audio_url,
            latest_avatar.get('mode', 'normal')
        )
        print(f"✅ 视频生成任务已提交")
        print(f"🆔 任务ID: {task_id}")
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")


def submit_effect_video_task(args):
    """提交特效视频生成任务"""
    ai = VolcEngineAI()
    try:
        print(f"🎨 开始提交特效视频生成任务...")
        print(f"📷 图片URL: {args.image_url}")
        print(f"🎭 模板ID: {args.template_id}")

        # 检查是否为双图模板并给出提示
        v1_dual_templates = ["double_embrace", "double_embrace_720p"]
        v2_dual_templates = ["french_kiss_dual_version", "french_kiss_dual_version_720p"]
        all_dual_templates = v1_dual_templates + v2_dual_templates

        if args.template_id in all_dual_templates:
            if "|" not in args.image_url:
                version = "V1" if args.template_id in v1_dual_templates else "V2"
                print(f"💕 提示: {version}版本模板 '{args.template_id}' 需要两张图片")
                print(f"   请使用以下格式: --image-url '图片1.jpg|图片2.jpg'")

        # 提交任务
        task_id = ai._effect_client.submit_task(
            image_url=args.image_url,
            template_id=args.template_id,
            final_stitch_switch=args.final_stitch_switch
        )

        print(f"✅ 特效视频任务已提交")
        print(f"🆔 任务ID: {task_id}")
        print("💡 可以使用以下命令查询状态:")
        print(f"   python volcengine_ai.py ve query {task_id}")
        return task_id
    except Exception as e:
        print(f"❌ 任务提交失败: {str(e)}")
        if "两张图片链接" in str(e):
            print("💡 双图模板使用示例:")
            print("   V1版本: python volcengine_ai.py ve create 'https://person1.jpg|https://person2.jpg' double_embrace")
            print("   V2版本: python volcengine_ai.py ve create 'https://person1.jpg|https://person2.jpg' french_kiss_dual_version")
        return None


def generate_effect_video(args):
    """生成创意特效视频（模块化组合：提交任务+查询结果）"""
    # 步骤1：提交任务
    task_id = submit_effect_video_task(args)
    if not task_id:
        return

    # 步骤2：查询结果（使用现有的query_effect_video函数）
    print("⏳ 等待特效视频生成完成...")

    # 创建一个临时的args对象来传递给query_effect_video
    class QueryArgs:
        def __init__(self):
            self.task_id = task_id
            self.download = True  # 总是下载
            self.filename = None

    query_effect_video(QueryArgs())


def query_effect_video(args):
    """查询特效视频状态（循环等待直到完成）"""
    import time
    ai = VolcEngineAI()
    start_time = time.time()
    max_wait_time = 600  # 10分钟
    check_interval = 15  # 15秒检查一次

    try:
        print(f"🔍 开始查询特效视频任务ID: {args.task_id}")
        print(f"⏰ 最大等待时间: {max_wait_time}秒，每{check_interval}秒检查一次")

        while time.time() - start_time < max_wait_time:
            try:
                result = ai.get_effect_video_result(args.task_id)
                print(f"📋 API响应: {result}")

                # 检查任务状态
                if isinstance(result, dict) and result.get("code") == 10000:
                    data = result.get("data", {})
                    status = data.get("status")

                    if status == "done":
                        print(f"✅ 任务完成！")

                        # 解析resp_data获取视频URL
                        resp_data_str = data.get("resp_data", "{}")
                        try:
                            import json
                            resp_data = json.loads(resp_data_str)
                            video_url = resp_data.get("video_url")
                            if video_url:
                                filename = args.filename or f"effect_video_{args.task_id}.mp4"
                                download_video(video_url, filename)
                                print("\n🎉 特效视频生成完成！")
                                print("=" * 50)
                                print(f"🆔 任务ID: {args.task_id}")
                                print(f"📹 视频URL: {video_url}")
                                print("=" * 50)
                            return
                        except:
                            print("\n🎉 特效视频生成完成！")
                            print("=" * 50)
                            print(f"🆔 任务ID: {args.task_id}")
                            print("=" * 50)
                            return

                    elif status in ["not_found", "expired"]:
                        print(f"❌ 任务异常: {status}")
                        return

                    else:
                        # 优先使用API返回的中文message，如果没有则使用status
                        message = data.get("message", f"任务状态: {status}")
                        print(f"⏳ 任务进行中... {message}")

                else:
                    print(f"⏳ 任务进行中... 状态: {result}")

                time.sleep(check_interval)

            except Exception as e:
                print(f"⚠️ 查询出错: {str(e)}，{check_interval}秒后重试...")
                time.sleep(check_interval)

        print(f"⏰ 等待超时 ({max_wait_time}秒)，任务可能仍在处理")
        print(f"💡 提示: 可手动继续查询: python volcengine_ai.py ve query {args.task_id}")

    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")

def submit_lip_sync_task(args):
    """提交视频改口型任务"""
    ai = VolcEngineAI()
    try:
        # 构建可选参数
        kwargs = {}
        if args.separate_vocal:
            kwargs['separate_vocal'] = True
        if args.open_scenedet:
            kwargs['open_scenedet'] = True
        # align_audio在lite模式下默认为True
        if args.mode == 'lite':
            kwargs['align_audio'] = getattr(args, 'align_audio', True) or True
        if args.align_audio_reverse:
            kwargs['align_audio_reverse'] = True
            # 倒放循环需要同时开启正循环
            kwargs['align_audio'] = True
        if hasattr(args, 'templ_start_seconds') and args.templ_start_seconds is not None:
            kwargs['templ_start_seconds'] = args.templ_start_seconds

        task_id = ai.submit_lip_sync_task(args.video_url, args.audio_url, args.mode, **kwargs)
        print(f"✅ 视频改口型任务已提交")
        print(f"🆔 任务ID: {task_id}")
        print("💡 可以使用以下命令查询状态:")
        print(f"   python volcengine_ai.py vl query {task_id} --mode {args.mode}")
    except Exception as e:
        print(f"❌ 提交失败: {str(e)}")

def query_lip_sync(args):
    """查询视频改口型状态"""
    ai = VolcEngineAI()
    try:
        print(f"🔍 查询任务ID: {args.task_id} ({args.mode}模式)")

        # 循环查询直到任务完成
        import time
        start_time = time.time()
        max_wait_time = 600  # 最大等待10分钟
        check_interval = 15  # 每15秒查询一次

        while time.time() - start_time < max_wait_time:
            try:
                result = ai.get_lip_sync_result(args.task_id, args.mode)

                # 显示当前状态
                if isinstance(result, dict):
                    status = result.get("status", "unknown")
                    if status == "done":
                        print(f"📋 API响应: {result}")

                        # 下载视频
                        if result.get("video_url"):
                            video_url = result["video_url"]
                            filename = args.filename or f"lip_sync_video_{args.task_id}.mp4"
                            download_video(video_url, filename)
                            print("\n🎉 视频改口型完成！")
                            print("=" * 50)
                            print(f"🆔 任务ID: {args.task_id}")
                            print(f"📹 视频URL: {video_url}")
                            print("=" * 50)
                        return

                    elif status in ["not_found", "expired"]:
                        print(f"❌ 任务异常: {status}")
                        return

                    elif result.get("video_url"):
                        # 如果有video_url说明任务已完成
                        print(f"📋 API响应: {result}")
                        video_url = result["video_url"]
                        filename = args.filename or f"lip_sync_video_{args.task_id}.mp4"
                        download_video(video_url, filename)
                        print("\n🎉 视频改口型完成！")
                        print("=" * 50)
                        print(f"🆔 任务ID: {args.task_id}")
                        print("=" * 50)
                        return

                    else:
                        # 优先使用API返回的中文message，如果没有则使用status
                        message = result.get("message", f"任务状态: {status}")
                        print(f"⏳ 任务进行中... {message}")

                else:
                    print(f"⏳ 任务进行中... 状态: {result}")

                time.sleep(check_interval)

            except Exception as e:
                print(f"⚠️ 查询出错: {str(e)}，{check_interval}秒后重试...")
                time.sleep(check_interval)

        print(f"⏰ 等待超时 ({max_wait_time}秒)，任务可能仍在处理")
        print(f"💡 提示: 可手动继续查询: python volcengine_ai.py vl query {args.task_id} --mode {args.mode}")

    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")

def change_lip_sync(args):
    """视频改口型（完整流程）"""
    ai = VolcEngineAI()
    try:
        # 构建可选参数
        kwargs = {}
        if args.separate_vocal:
            kwargs['separate_vocal'] = True
        if args.open_scenedet:
            kwargs['open_scenedet'] = True
        # align_audio在lite模式下默认为True
        if args.mode == 'lite':
            kwargs['align_audio'] = getattr(args, 'align_audio', True) or True
        if args.align_audio_reverse:
            kwargs['align_audio_reverse'] = True
            # 倒放循环需要同时开启正循环
            kwargs['align_audio'] = True
        if hasattr(args, 'templ_start_seconds') and args.templ_start_seconds is not None:
            kwargs['templ_start_seconds'] = args.templ_start_seconds

        print(f"开始视频改口型（{args.mode}模式）...")

        # 提交视频改口型任务
        task_id = ai.submit_lip_sync_task(
            args.video_url,
            args.audio_url,
            args.mode,
            **kwargs
        )
        print(f"✅ 视频改口型任务已提交")
        print(f"🆔 任务ID: {task_id}")
        print("⏳ 正在等待处理完成...")

        # 调用query_lip_sync处理查询和下载
        class QueryArgs:
            def __init__(self):
                self.task_id = task_id
                self.mode = args.mode
                self.download = True  # 总是下载
                self.filename = None

        query_lip_sync(QueryArgs())

    except Exception as e:
        print(f"❌ 视频改口型失败: {str(e)}")


def list_effect_templates():
    """列出可用的特效模板"""
    # V1版本模板
    v1_templates = {
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

    # V2版本模板
    v2_templates = {
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

    print("🎨 可用的特效模板:")
    print("=" * 80)

    # V1版本分类
    v1_categories = {
        "🎭 V1 - 卡通变身": ["becoming_doll", "becoming_doll_720p"],
        "🐉 V1 - 召唤坐骑": ["all_things_ridability_pig", "all_things_ridability_pig_720p", "all_things_ridability_tiger", "all_things_ridability_tiger_720p", "all_things_ridability_loong", "all_things_ridability_loong_720p"],
        "🌸 V1 - 万物生花": ["all_things_bloom_with_flowers", "all_things_bloom_with_flowers_720p"],
        "💕 V1 - 情感互动": ["double_embrace_single_person", "double_embrace_single_person_720p", "double_embrace", "double_embrace_720p"],
        "😊 V1 - AI环绕": ["beauty_surround", "beauty_surround_720p", "handsome_man_surround", "handsome_man_surround_720p"],
        "👶 V1 - 天赐宝宝": ["ai_baby", "ai_baby_720p"]
    }

    # V2版本分类
    v2_categories = {
        "🎭 V2 - 卡通变身": ["multi_style_stacking_dolls", "fluffy_dream_doll_s2e", "fluffy_dream_doll_s2e_720p", "fluffy_dream_doll", "fluffy_dream_doll_720p", "my_world", "my_world_720p", "angel_figure", "angel_figure_720p", "felt_keychain", "felt_keychain_720p", "acrylic_charm", "acrylic_charm_720p", "blister_pack_action_figure", "blister_pack_action_figure_720p"],
        "💫 V2 - 特效场景": ["crystal_ball", "crystal_ball_720p", "lying_on_fluffy_belly", "lying_on_fluffy_belly_720p", "polaroid", "polaroid_720p"],
        "💕 V2 - 情感互动": ["french_kiss_dual_version", "french_kiss_dual_version_720p", "french_kiss_solo_version", "french_kiss_solo_version_720p"],
        "👗 V2 - 变装换装": ["costume_bikini", "costume_bikini_720p", "transform_into_mermaid", "transform_into_mermaid_720p"],
        "💃 V2 - 动感舞蹈": ["hot_dance", "hot_dance_720p"]
    }

    print("\n📱 V1版本接口 (20个模板):")
    print("-" * 40)
    for category, template_list in v1_categories.items():
        print(f"\n{category}:")
        for template_id in template_list:
            if template_id in v1_templates:
                print(f"  {template_id}: {v1_templates[template_id]}")

    print("\n🚀 V2版本接口 (29个模板):")
    print("-" * 40)
    for category, template_list in v2_categories.items():
        print(f"\n{category}:")
        for template_id in template_list:
            if template_id in v2_templates:
                print(f"  {template_id}: {v2_templates[template_id]}")

    print(f"\n📝 说明:")
    print("  - V1和V2版本使用不同的接口，但会自动根据模板ID识别")
    print("  - 带'_720p'后缀的为高清版本")
    print("  - V1双图模板: double_embrace 系列，需要用'|'连接两个图片URL")
    print("  - V2双图模板: french_kiss_dual_version 系列，需要用'|'连接两个图片URL")
    print("  - V2的emoji小人变身_480p不支持分屏功能")
    print(f"🎯 模板总数: {len(v1_templates) + len(v2_templates)} 个模板")
    print("🔍 使用示例: python volcengine_ai.py ve create '图片URL' '模板ID'")


def generate_all(args):
    """一键生成完整流程（模块化组合）"""
    try:
        print(f"开始生成视频（{args.mode}模式）...")
        print("💡 提示: 视频生成需要3-10分钟，请耐心等待")

        # 步骤1：创建形象（使用现有的create_avatar函数）
        print("步骤1：创建数字形象...")
        create_avatar(args)

        # 步骤2：生成视频（需要从create_avatar的结果中获取resource_id）
        # create_avatar已经保存到本地，可以直接读取
        from src.modules.avatar_manager import avatar_manager
        latest_avatar = avatar_manager.get_latest_avatar(args.mode)
        if not latest_avatar:
            raise Exception("无法获取刚创建的形象信息")

        resource_id = latest_avatar['resource_id']
        print(f"📝 使用形象ID: {resource_id}")

        # 步骤3：生成视频并查询（使用现有的generate_video + query_video）
        print("步骤2：生成视频...")

        class VideoArgs:
            def __init__(self):
                self.resource_id = resource_id
                self.audio_url = args.audio_url
                self.mode = args.mode

        # 使用组合函数：generate_video + query_video
        generate_video_with_query(VideoArgs())

    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")
        if "超时" in str(e):
            print("💡 建议: 可以单独查询任务状态")


def generate_video_with_query(args):
    """生成视频并查询结果（模块化组合）"""
    # 步骤1：生成视频（提交任务）
    task_id = generate_video(args)
    if not task_id:
        raise Exception("视频任务提交失败")

    # 步骤2：查询视频状态（使用现有的query_video函数）
    print("⏳ 等待视频生成完成...")

    # 创建一个临时的args对象来传递给query_video
    class QueryArgs:
        def __init__(self):
            self.task_id = task_id
            self.mode = args.mode
            self.download = True  # 总是下载
            self.filename = None

    query_video(QueryArgs())


# === 新命令处理器 ===

# 音频驱动 (va) 处理器
def va_create_avatar_handler(args):
    """创建数字形象"""
    class Args:
        def __init__(self):
            self.image_url = args.image_url
            self.mode = args.mode

    create_avatar(Args())

def va_query_avatar_handler(args):
    """查询形象创建状态"""
    class Args:
        def __init__(self):
            self.task_id = args.task_id
            self.mode = args.mode

    query_avatar(Args())

def va_create_video_handler(args):
    """生成角色视频"""
    class Args:
        def __init__(self):
            self.resource_id = args.resource_id
            self.audio_url = args.audio_url
            self.mode = args.mode

    generate_video(Args())

def va_query_video_handler(args):
    """查询视频生成状态"""
    class Args:
        def __init__(self):
            self.task_id = args.task_id
            self.mode = args.mode
            self.download = True  # 总是下载
            self.filename = args.filename

    query_video(Args())

def va_create_handler(args):
    """一键生成完整流程"""
    class Args:
        def __init__(self):
            self.image_url = args.image_url
            self.audio_url = args.audio_url
            self.mode = args.mode

    generate_all(Args())

# 特效视频 (ve) 处理器
def ve_create_handler(args):
    """生成创意特效视频"""
    class Args:
        def __init__(self):
            self.image_url = args.image_url
            self.template_id = args.template_id
            self.final_stitch_switch = args.final_stitch_switch

    generate_effect_video(Args())

def ve_query_handler(args):
    """查询特效视频生成状态"""
    class Args:
        def __init__(self):
            self.task_id = args.task_id
            self.download = True  # 总是下载
            self.filename = args.filename

    query_effect_video(Args())

def ve_templates_handler(args):
    """列出可用的特效模板"""
    list_effect_templates()

# 音频驱动 (va) 额外处理器
def va_avatars_handler(args):
    """查看可用形象"""
    class Args:
        def __init__(self):
            self.mode = args.mode

    list_avatars(Args())

# 视频改口型 (vl) 处理器
def vl_create_handler(args):
    """生成视频改口型"""
    class Args:
        def __init__(self):
            self.video_url = args.video_url
            self.audio_url = args.audio_url
            self.mode = args.mode
            self.separate_vocal = args.separate_vocal
            self.open_scenedet = args.open_scenedet
            self.align_audio = args.align_audio
            self.align_audio_reverse = args.align_audio_reverse
            self.templ_start_seconds = args.templ_start_seconds

    change_lip_sync(Args())

def vl_query_handler(args):
    """查询视频改口型状态"""
    class Args:
        def __init__(self):
            self.task_id = args.task_id
            self.mode = args.mode
            self.download = True  # 总是下载
            self.filename = args.filename

    query_lip_sync(Args())

# 即梦AI数字人 (jm) 处理器
def jm_detect_avatar_handler(args):
    """主体识别"""
    class Args:
        def __init__(self):
            self.image_url = args.image_url
            self.version = args.version

    jm_detect_avatar(Args())


def jm_detect_avatar(args):
    """主体识别"""
    ai = VolcEngineAI()
    try:
        print(f"🔍 开始主体识别，版本: {args.version}")

        result = ai.jm_detect_avatar(args.image_url, args.version)

        # 直接显示原始API响应，不进行二次处理
        print(f"📋 API响应: {result}")

    except Exception as e:
        print(f"❌ 主体识别失败: {str(e)}")

def jm_detect_object_handler(args):
    """对象检测"""
    class Args:
        def __init__(self):
            self.image_url = args.image_url

    jm_detect_object(Args())

def jm_detect_object(args):
    """对象检测"""
    ai = VolcEngineAI()
    try:
        print(f"🔍 开始对象检测（仅1.5版支持）")

        result = ai.jm_detect_object(args.image_url)

        # 直接显示原始API响应，不进行二次处理
        print(f"📋 API响应: {result}")

    except Exception as e:
        print(f"❌ 对象检测失败: {str(e)}")

def jm_create_handler(args):
    """生成视频"""
    class Args:
        def __init__(self):
            self.image_url = args.image_url
            self.audio_url = args.audio_url
            self.version = args.version
            self.prompt = args.prompt
            self.mask_url = args.mask_url
            self.seed = args.seed
            self.pe_fast_mode = args.pe_fast_mode

    jm_create_video(Args())

def jm_create_video(args):
    """生成数字人视频（提交任务并自动查询下载）"""
    ai = VolcEngineAI()
    try:
        print(f"🎬 开始生成数字人视频，版本: {args.version}")
        print(f"📷 图片URL: {args.image_url}")
        print(f"🎵 音频URL: {args.audio_url}")

        # 显示额外参数
        if args.prompt:
            print(f"💭 提示词: {args.prompt}")
        if args.mask_url:
            print(f"🎭 Mask图数量: {len(args.mask_url)}")
        if args.seed:
            print(f"🎲 随机种子: {args.seed}")
        if args.pe_fast_mode:
            print("⚡ 快速模式: 开启")

        # 步骤1：提交任务
        task_id = ai.jm_create_video(
            args.image_url,
            args.audio_url,
            args.version,
            args.prompt,
            args.mask_url,
            args.seed,
            args.pe_fast_mode
        )

        print(f"✅ 视频生成任务已提交")
        print(f"🆔 任务ID: {task_id}")
        print("⏳ 正在等待处理完成...")

        # 步骤2：自动查询并等待完成（调用现有的query逻辑）
        class QueryArgs:
            def __init__(self):
                self.task_id = task_id
                self.operation_type = "generate"
                self.version = args.version
                self.filename = None  # create命令使用默认文件名

        jm_query_result(QueryArgs())

    except Exception as e:
        print(f"❌ 视频生成失败: {str(e)}")

def jm_query_handler(args):
    """查询状态"""
    class Args:
        def __init__(self):
            self.task_id = args.task_id
            self.operation_type = args.operation_type
            self.version = args.version
            self.filename = args.filename

    jm_query_result(Args())

def jm_query_result(args):
    """查询即梦AI任务结果（循环等待直到完成）"""
    import time
    ai = VolcEngineAI()
    start_time = time.time()
    max_wait_time = 600  # 10分钟
    check_interval = 15  # 15秒检查一次

    try:
        print(f"🔍 开始查询任务ID: {args.task_id} ({args.operation_type}操作)")
        print(f"🔢 版本: {args.version}")
        print(f"⏰ 最大等待时间: {max_wait_time}秒，每{check_interval}秒检查一次")

        while time.time() - start_time < max_wait_time:
            try:
                result = ai.jm_query_result(args.task_id, args.operation_type, args.version)
                print(f"📋 API响应: {result}")

                # 检查任务状态
                if isinstance(result, dict):
                    status = result.get("status", "unknown")
                    if status == "done":
                        print(f"✅ 任务完成！")

                        # 如果是视频生成且有视频URL，自动下载
                        if args.operation_type == "generate" and result.get("video_url"):
                            video_url = result["video_url"]
                            filename = args.filename or f"jm_video_{args.task_id}.mp4"
                            download_video(video_url, filename)
                            print("\n🎉 视频生成完成！")
                            print("=" * 50)
                            print(f"🆔 任务ID: {args.task_id}")
                            print(f"📹 视频URL: {video_url}")
                            print(f"📁 本地文件: {filename}")
                            print("=" * 50)
                        return

                    elif status in ["not_found", "expired"]:
                        print(f"❌ 任务异常: {status}")
                        return

                    elif args.operation_type == "generate" and result.get("video_url"):
                        # 如果有video_url说明任务已完成
                        print(f"✅ 任务完成！")
                        video_url = result["video_url"]
                        filename = args.filename or f"jm_video_{args.task_id}.mp4"
                        download_video(video_url, filename)
                        print("\n🎉 视频生成完成！")
                        print("=" * 50)
                        print(f"🆔 任务ID: {args.task_id}")
                        print("=" * 50)
                        return

                    else:
                        # 优先使用API返回的中文message，如果没有则使用status
                        message = result.get("message", f"任务状态: {status}")
                        print(f"⏳ 任务进行中... {message}")

                else:
                    print(f"⏳ 任务进行中... 状态: {result}")

                time.sleep(check_interval)

            except Exception as e:
                print(f"⚠️ 查询出错: {str(e)}，{check_interval}秒后重试...")
                time.sleep(check_interval)

        print(f"⏰ 等待超时 ({max_wait_time}秒)，任务可能仍在处理")
        print(f"💡 提示: 可手动继续查询: python volcengine_ai.py jm omni query {args.task_id} --version {args.version} --operation-type {args.operation_type}")

    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")

# 即梦AI动作模仿 (jm mimic) 处理器
def jm_mimic_create_handler(args):
    """创建动作模仿任务（提交任务并自动查询下载）"""
    class Args:
        def __init__(self):
            self.image_url = args.image_url
            self.video_url = args.video_url
            self.filename = args.filename

    jm_mimic_create(Args())

def jm_mimic_create(args):
    """创建动作模仿任务（提交任务并自动查询下载）"""
    ai = VolcEngineAI()
    try:
        # 步骤1：提交任务
        task_id = ai.jm_mimic_submit_task(args.image_url, args.video_url)

        print(f"✅ 动作模仿任务已提交")
        print(f"🆔 任务ID: {task_id}")
        print("⏳ 正在等待处理完成...")

        # 步骤2：自动查询并等待完成（调用现有的query逻辑）
        class QueryArgs:
            def __init__(self):
                self.task_id = task_id
                self.filename = args.filename

        jm_mimic_query(QueryArgs())

    except Exception as e:
        print(f"❌ 动作模仿任务创建失败: {str(e)}")

def jm_mimic_query_handler(args):
    """查询动作模仿任务状态"""
    class Args:
        def __init__(self):
            self.task_id = args.task_id
            self.filename = args.filename

    jm_mimic_query(Args())

def jm_mimic_query(args):
    """查询动作模仿任务结果（循环等待直到完成）"""
    import time
    ai = VolcEngineAI()
    start_time = time.time()
    max_wait_time = 600  # 10分钟
    check_interval = 15  # 15秒检查一次

    try:
        print(f"🔍 开始查询动作模仿任务ID: {args.task_id}")
        print(f"⏰ 最大等待时间: {max_wait_time}秒，每{check_interval}秒检查一次")

        while time.time() - start_time < max_wait_time:
            try:
                result = ai.jm_mimic_get_result(args.task_id)
                print(f"📋 API响应: {result}")

                # 检查任务状态
                if isinstance(result, dict):
                    status = result.get("status", "unknown")
                    if status == "done":
                        print(f"✅ 任务完成！")

                        # 如果有视频URL，自动下载
                        if result.get("video_url"):
                            video_url = result["video_url"]
                            filename = args.filename or f"jm_mimic_{args.task_id}.mp4"
                            download_video(video_url, filename)
                            print("\n🎉 动作模仿视频生成完成！")
                            print("=" * 50)
                            print(f"🆔 任务ID: {args.task_id}")
                            print(f"📹 视频URL: {video_url}")
                            print(f"📁 本地文件: {filename}")
                            print("=" * 50)
                        return

                    elif status in ["not_found", "expired"]:
                        print(f"❌ 任务异常: {status}")
                        return

                    elif result.get("video_url"):
                        # 如果有video_url说明任务已完成
                        print(f"✅ 任务完成！")
                        video_url = result["video_url"]
                        filename = args.filename or f"jm_mimic_{args.task_id}.mp4"
                        download_video(video_url, filename)
                        print("\n🎉 动作模仿视频生成完成！")
                        print("=" * 50)
                        print(f"🆔 任务ID: {args.task_id}")
                        print("=" * 50)
                        return

                    else:
                        # 优先使用API返回的中文message，如果没有则使用status
                        message = result.get("message", f"任务状态: {status}")
                        print(f"⏳ 任务进行中... {message}")

                else:
                    print(f"⏳ 任务进行中... 状态: {result}")

                time.sleep(check_interval)

            except Exception as e:
                print(f"⚠️ 查询出错: {str(e)}，{check_interval}秒后重试...")
                time.sleep(check_interval)

        print(f"⏰ 等待超时 ({max_wait_time}秒)，任务可能仍在处理")
        print(f"💡 提示: 可手动继续查询: python volcengine_ai.py jm mimic query {args.task_id}")

    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")


def main():
    """统一入口主函数"""
    parser = argparse.ArgumentParser(description="火山引擎AI平台")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # === 单图音频驱动 (va) ===
    va_parser = subparsers.add_parser('va', help='单图音频驱动视频生成')
    va_subparsers = va_parser.add_subparsers(dest='va_action', help='单图音频驱动操作')

    # va create-avatar
    va_create_avatar = va_subparsers.add_parser('create-avatar', help='创建数字形象')
    va_create_avatar.add_argument('image_url', help='图片URL')
    va_create_avatar.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], required=True, help='模式选择')
    va_create_avatar.set_defaults(func=va_create_avatar_handler)

    # va query-avatar (备用查询功能，用于重新查询或自动化查询失败时使用)
    va_query_avatar = va_subparsers.add_parser('query-avatar', help='查询形象创建状态（备用功能）')
    va_query_avatar.add_argument('task_id', help='任务ID')
    va_query_avatar.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], required=True, help='创建时使用的模式')
    va_query_avatar.set_defaults(func=va_query_avatar_handler)

    # va create-video
    va_create_video = va_subparsers.add_parser('create-video', help='生成角色视频')
    va_create_video.add_argument('resource_id', help='形象ID')
    va_create_video.add_argument('audio_url', help='音频URL')
    va_create_video.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], default='normal', help='模式选择')
    va_create_video.set_defaults(func=va_create_video_handler)

    # va query-video
    va_query_video = va_subparsers.add_parser('query-video', help='查询视频生成状态')
    va_query_video.add_argument('task_id', help='任务ID')
    va_query_video.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], required=True, help='生成时使用的模式')
    va_query_video.add_argument('--filename', help='保存文件名（可选，默认为video_<task_id>.mp4）')
    va_query_video.set_defaults(func=va_query_video_handler)

    # va create (一键生成)
    va_create = va_subparsers.add_parser('create', help='一键生成视频（形象+视频）')
    va_create.add_argument('image_url', help='图片URL')
    va_create.add_argument('audio_url', help='音频URL')
    va_create.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], default='normal', help='模式选择')
    va_create.set_defaults(func=va_create_handler)

    # === 特效视频 (ve) ===
    ve_parser = subparsers.add_parser('ve', help='单图创意特效视频生成')
    ve_subparsers = ve_parser.add_subparsers(dest='ve_action', help='单图创意特效视频操作')

    # ve create
    ve_create = ve_subparsers.add_parser('create', help='生成创意特效视频')
    ve_create.add_argument('image_url', help='图片URL')
    ve_create.add_argument('template_id', help='特效模板ID')
    ve_create.add_argument('--final-stitch-switch', type=bool, default=True, help='分屏设置 (false: 开启上下分屏, true: 关闭分屏)')
    ve_create.set_defaults(func=ve_create_handler)

    # ve query
    ve_query = ve_subparsers.add_parser('query', help='查询特效视频生成状态')
    ve_query.add_argument('task_id', help='任务ID')
    ve_query.add_argument('--filename', help='保存文件名（可选，默认为effect_video_<task_id>.mp4）')
    ve_query.set_defaults(func=ve_query_handler)

    # ve templates
    ve_templates = ve_subparsers.add_parser('templates', help='列出可用的特效模板')
    ve_templates.set_defaults(func=ve_templates_handler)

    # === 视频改口型 (vl) ===
    vl_parser = subparsers.add_parser('vl', help='音频驱动单人口播视频改口型')
    vl_subparsers = vl_parser.add_subparsers(dest='vl_action', help='音频驱动视频改口型操作')

    # vl create
    vl_create = vl_subparsers.add_parser('create', help='生成视频改口型')
    vl_create.add_argument('video_url', help='视频素材URL')
    vl_create.add_argument('audio_url', help='音频URL')
    vl_create.add_argument('--mode', choices=['lite', 'basic'], default='lite', help='模式选择 (lite: 单人正面视频, basic: 单人复杂场景)')
    vl_create.add_argument('--separate-vocal', action='store_true', help='开启人声分离（仅basic模式）')
    vl_create.add_argument('--open-scenedet', action='store_true', help='开启场景切分与说话人识别（仅basic模式）')
    vl_create.add_argument('--align-audio', action='store_true', help='开启视频循环（仅lite模式）')
    vl_create.add_argument('--align-audio-reverse', action='store_true', help='开启倒放循环（仅lite模式，需同时开启align-audio）')
    vl_create.add_argument('--templ-start-seconds', type=float, help='模板视频开始时间（仅lite模式）')
    vl_create.set_defaults(func=vl_create_handler)

    # vl query
    vl_query = vl_subparsers.add_parser('query', help='查询视频改口型状态')
    vl_query.add_argument('task_id', help='任务ID')
    vl_query.add_argument('--mode', choices=['lite', 'basic'], required=True, help='生成时使用的模式')
    vl_query.add_argument('--filename', help='保存文件名（可选，默认为lip_sync_video_<task_id>.mp4）')
    vl_query.set_defaults(func=vl_query_handler)

    # === 单图视频驱动 (vv) ===
    vv_parser = subparsers.add_parser('vv', help='单图视频驱动视频生成')
    vv_subparsers = vv_parser.add_subparsers(dest='vv_action', help='单图视频驱动操作')

    # vv create - 创建单图视频驱动任务
    vv_create = vv_subparsers.add_parser('create', help='创建单图视频驱动任务')
    vv_create.add_argument('image_url', help='图片URL（需公网可访问）')
    vv_create.add_argument('video_url', help='驱动视频URL（需公网可访问）')
    vv_create.add_argument('--filename', help='保存文件名（可选，默认为video_driven_<task_id>.mp4）')
    vv_create.set_defaults(func=vv_create_handler)

    # vv query - 查询单图视频驱动任务
    vv_query = vv_subparsers.add_parser('query', help='查询单图视频驱动任务状态')
    vv_query.add_argument('task_id', help='任务ID')
    vv_query.add_argument('--filename', help='保存文件名（可选，默认为video_driven_<task_id>.mp4）')
    vv_query.set_defaults(func=vv_query_handler)

    # === 图片换装 (io) ===
    io_parser = subparsers.add_parser('io', help='图片换装生成')
    io_subparsers = io_parser.add_subparsers(dest='io_action', help='图片换装操作')

    # io generate - 一键生成换装图片
    io_generate = io_subparsers.add_parser('generate', help='生成换装图片')
    io_generate.add_argument('model_url', help='模特图片URL（需公网可访问）')
    io_generate.add_argument('garment_url', help='服装图片URL（需公网可访问）')
    io_generate.add_argument('--filename', help='保存文件名（可选，默认为outfit_<timestamp>.png）')
    io_generate.add_argument('--no-download', action='store_true', help='不自动下载图片，只返回URL')
    io_generate.add_argument('--model-id', default='1', help='模特ID（默认: 1）')
    io_generate.add_argument('--garment-id', default='1', help='服装ID（默认: 1）')
    io_generate.add_argument('--seed', type=int, help='随机种子参数（-1表示随机）')
    io_generate.add_argument('--no-keep-head', action='store_false', dest='keep_head', help='不保持模特原图的头（包括发型）')
    io_generate.add_argument('--no-keep-hand', action='store_false', dest='keep_hand', help='不保持模特原图的手')
    io_generate.add_argument('--no-keep-foot', action='store_false', dest='keep_foot', help='不保持模特原图的足')
    io_generate.add_argument('--keep-upper', action='store_true', help='保持模特原图的上装（默认不保持）')
    io_generate.add_argument('--keep-lower', action='store_true', help='保持模特原图的下装（默认不保持）')
    io_generate.add_argument('--no-sr', action='store_false', dest='do_sr', help='不对结果进行超分处理（默认启用）')
    io_generate.add_argument('--num-steps', type=int, choices=range(25, 51), help='模型推理步数（25-50，默认: 50）')
    io_generate.add_argument('--version', choices=['1', '2'], default='1', help='API版本选择（1: V1版同步接口, 2: V2版异步接口，默认: 1）')
    io_generate.add_argument('--garment-types', nargs='+', help='服装类型列表（V2版专用，取值: upper/bottom/full，用空格分隔）')
    io_generate.add_argument('--protect-mask-url', help='模特保护区域图URL（V2版专用，PNG格式）')
    io_generate.add_argument('--tight-mask', choices=['tight', 'loose', 'bbox'], default='loose', help='模特图遮挡区域范围（V2版专用，默认: loose）')
    io_generate.add_argument('--p-bbox-iou-ratio', type=float, help='bbox与主体相交比例（V2版专用，范围: [0, 1.0]，默认: 0.3）')
    io_generate.add_argument('--p-bbox-expand-ratio', type=float, help='bbox扩大比例（V2版专用，范围: [1.0, 1.5]，默认: 1.1）')
    io_generate.add_argument('--max-process-side-length', type=int, help='最大边长（V2版专用，范围: [1080, 4096]，默认: 1920）')
    io_generate.add_argument('--req-image-store-type', type=int, choices=[0, 1], default=1, help='图片传入方式（0:base64, 1:URL，默认: 1）')
    io_generate.set_defaults(func=io_generate_handler)

    # === 即梦AI数字人 (jm) ===
    jm_parser = subparsers.add_parser('jm', help='即梦AI多功能生成平台')
    jm_subparsers = jm_parser.add_subparsers(dest='jm_action', help='即梦AI视频生成操作')

    # jm omni - OmniHuman数字人视频
    jm_omni_parser = jm_subparsers.add_parser('omni', help='即梦OmniHuman数字人视频')
    jm_omni_subparsers = jm_omni_parser.add_subparsers(dest='jm_omni_action', help='即梦OmniHuman数字人视频操作')

    # jm omni detect-avatar - 主体识别
    jm_omni_detect = jm_omni_subparsers.add_parser('detect-avatar', help='即梦数字人 - 主体识别')
    jm_omni_detect.add_argument('image_url', help='图片URL')
    jm_omni_detect.add_argument('--version', choices=['1.0', '1.5'], required=True, help='版本选择 (1.0: 480P基础版, 1.5: 1080P增强版)')
    jm_omni_detect.set_defaults(func=jm_detect_avatar_handler)

    # jm omni detect-object - 对象检测
    jm_omni_detect_object = jm_omni_subparsers.add_parser('detect-object', help='即梦数字人 - 对象检测（1.5版）')
    jm_omni_detect_object.add_argument('image_url', help='图片URL')
    jm_omni_detect_object.set_defaults(func=jm_detect_object_handler)

    # jm omni create - 生成视频
    jm_omni_create = jm_omni_subparsers.add_parser('create', help='即梦数字人 - 生成视频')
    jm_omni_create.add_argument('image_url', help='图片URL')
    jm_omni_create.add_argument('audio_url', help='音频URL')
    jm_omni_create.add_argument('--version', choices=['1.0', '1.5'], required=True, help='版本选择 (1.0: 480P基础版, 1.5: 1080P增强版)')
    jm_omni_create.add_argument('--prompt', help='提示词（仅1.5版支持）')
    jm_omni_create.add_argument('--mask-url', nargs='+', help='mask图URL列表（仅1.5版，用于指定主体）')
    jm_omni_create.add_argument('--seed', type=int, help='随机种子（仅1.5版）')
    jm_omni_create.add_argument('--pe-fast-mode', action='store_true', help='启用快速模式（仅1.5版）')
    jm_omni_create.set_defaults(func=jm_create_handler)

    # jm omni query - 查询状态
    jm_omni_query = jm_omni_subparsers.add_parser('query', help='即梦数字人 - 查询状态')
    jm_omni_query.add_argument('task_id', help='任务ID')
    jm_omni_query.add_argument('--operation-type', choices=['detect', 'detect_object', 'generate'], default='generate', help='操作类型')
    jm_omni_query.add_argument('--version', choices=['1.0', '1.5'], required=True, help='版本选择')
    jm_omni_query.add_argument('--filename', help='保存文件名（可选，默认为jm_video_<task_id>.mp4）')
    jm_omni_query.set_defaults(func=jm_query_handler)

    # jm mimic - 动作模仿
    jm_mimic_parser = jm_subparsers.add_parser('mimic', help='即梦动作模仿')
    jm_mimic_subparsers = jm_mimic_parser.add_subparsers(dest='jm_mimic_action', help='即梦动作模仿操作')

    # jm mimic create - 创建动作模仿任务
    jm_mimic_create = jm_mimic_subparsers.add_parser('create', help='创建动作模仿任务')
    jm_mimic_create.add_argument('image_url', help='图片URL（需公网可访问）')
    jm_mimic_create.add_argument('video_url', help='视频URL（需公网可访问）')
    jm_mimic_create.add_argument('--filename', help='保存文件名（可选，默认为jm_mimic_<task_id>.mp4）')
    jm_mimic_create.set_defaults(func=jm_mimic_create_handler)

    # jm mimic query - 查询动作模仿任务
    jm_mimic_query = jm_mimic_subparsers.add_parser('query', help='查询动作模仿任务状态')
    jm_mimic_query.add_argument('task_id', help='任务ID')
    jm_mimic_query.add_argument('--filename', help='保存文件名（可选，默认为jm_mimic_<task_id>.mp4）')
    jm_mimic_query.set_defaults(func=jm_mimic_query_handler)

    # === 形象管理 (va) - 添加到va子命令中 ===
    va_avatars = va_subparsers.add_parser('avatars', help='查看可用形象')
    va_avatars.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], help='按模式筛选')
    va_avatars.set_defaults(func=va_avatars_handler)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 检查环境变量
    if not ACCESS_KEY:
        print("❌ 错误：未设置环境变量 VOLCENGINE_ACCESS_KEY")
        return

    if not SECRET_KEY:
        print("❌ 错误：未设置环境变量 VOLCENGINE_SECRET_KEY")
        return

    # 执行对应命令
    if args.command == 'va':
        if not args.va_action:
            va_parser.print_help()
            return
        args.func(args)
    elif args.command == 've':
        if not args.ve_action:
            ve_parser.print_help()
            return
        args.func(args)
    elif args.command == 'vl':
        if not args.vl_action:
            vl_parser.print_help()
            return
        args.func(args)
    elif args.command == 'vv':
        if not args.vv_action:
            vv_parser.print_help()
            return
        args.func(args)
    elif args.command == 'io':
        if not args.io_action:
            io_parser.print_help()
            return
        args.func(args)
    elif args.command == 'jm':
        if not args.jm_action:
            jm_parser.print_help()
            return
        elif args.jm_action == 'omni':
            if not args.jm_omni_action:
                jm_omni_parser.print_help()
                return
            args.func(args)
        elif args.jm_action == 'mimic':
            if not args.jm_mimic_action:
                jm_mimic_parser.print_help()
                return
            args.func(args)
        else:
            jm_parser.print_help()


def vv_create_handler(args):
    """处理单图视频驱动创建命令"""
    vv_create(args)


def vv_query_handler(args):
    """处理单图视频驱动查询命令"""
    vv_query(args)


def vv_create(args):
    """创建单图视频驱动任务（自动查询并等待完成）"""
    ai = VolcEngineAI()
    try:
        print(f"🎬 开始创建单图视频驱动任务")
        print(f"📷 图片URL: {args.image_url}")
        print(f"🎥 驱动视频URL: {args.video_url}")

        task_id = ai.submit_video_driven_task(args.image_url, args.video_url)
        print(f"✅ 单图视频驱动任务已提交")
        print(f"🆔 任务ID: {task_id}")
        print("⏳ 正在等待处理完成...")
        print("💡 可以使用以下命令查询状态:")
        print(f"   python volcengine_ai.py vv query {task_id}")

        # 创建一个临时的args对象来传递给vv_query
        class QueryArgs:
            def __init__(self):
                self.task_id = task_id
                self.filename = getattr(args, 'filename', None)

        vv_query(QueryArgs())

    except Exception as e:
        print(f"❌ 创建失败: {str(e)}")


def vv_query(args):
    """查询单图视频驱动任务状态（循环等待直到完成）"""
    import time
    ai = VolcEngineAI()
    start_time = time.time()
    max_wait_time = 600  # 10分钟
    check_interval = 15  # 15秒检查一次

    try:
        print(f"🔍 开始查询单图视频驱动任务ID: {args.task_id}")
        print(f"⏰ 最大等待时间: {max_wait_time}秒，每{check_interval}秒检查一次")

        while time.time() - start_time < max_wait_time:
            try:
                result = ai.get_video_driven_result(args.task_id)
                print(f"📋 API响应: {result}")

                # 检查任务状态
                if isinstance(result, dict):
                    status = result.get("status", "unknown")
                    if status == "done":
                        print(f"✅ 任务完成！")

                        # 下载视频
                        if result.get("video_url"):
                            video_url = result["video_url"]
                            filename = args.filename or f"video_driven_{args.task_id}.mp4"
                            download_video(video_url, filename)
                            print("\n🎉 单图视频驱动视频生成完成！")
                            print("=" * 50)
                            print(f"🆔 任务ID: {args.task_id}")
                            print(f"📹 视频URL: {video_url}")
                            print(f"🏷️ 隐式标识: {'已添加' if result.get('aigc_meta_tagged') else '未添加'}")
                            print("=" * 50)
                        return
                    elif status in ["not_found", "expired"]:
                        print(f"❌ 任务异常: {status}")
                        return

                    else:
                        # 优先使用API返回的中文message，如果没有则使用status
                        message = result.get("message", f"任务状态: {status}")
                        print(f"⏳ 任务进行中... {message}")

                else:
                    print(f"⏳ 任务进行中... 状态: {result}")

                time.sleep(check_interval)

            except Exception as e:
                print(f"⚠️ 查询出错: {str(e)}，{check_interval}秒后重试...")
                time.sleep(check_interval)

        print(f"⏰ 等待超时 ({max_wait_time}秒)，任务可能仍在处理")
        print(f"💡 提示: 可手动继续查询: python volcengine_ai.py vv query {args.task_id}")

    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")


def io_generate_handler(args):
    """处理图片换装生成命令"""
    io_generate(args)


def io_generate(args):
    """生成图片换装"""
    ai = VolcEngineAI()
    try:
        version = getattr(args, 'version', '1')
        print(f"👗 开始图片换装生成 (V{version}版)")

        if version == '2':
            # V2版：支持多件服装
            print(f"👤 模特图片URL: {args.model_url}")

            # 解析服装URL列表
            garment_urls = args.garment_url.split('|') if '|' in args.garment_url else [args.garment_url]
            print(f"👔 服装图片URL: {garment_urls}")

            # 解析服装类型
            garment_types = getattr(args, 'garment_types', None)
            if garment_types and len(garment_types) != len(garment_urls):
                raise ValueError(f"服装类型数量({len(garment_types)})与服装图片数量({len(garment_urls)})不匹配")

            if garment_types:
                print(f"🏷️ 服装类型: {garment_types}")

            # 构建推理配置 - 只有明确指定时才覆盖默认值
            inference_config = {}

            if hasattr(args, 'seed') and args.seed is not None:
                inference_config["seed"] = args.seed
            if hasattr(args, 'keep_head') and not args.keep_head:
                inference_config["keep_head"] = False
            if hasattr(args, 'keep_hand') and not args.keep_hand:
                inference_config["keep_hand"] = False
            if hasattr(args, 'keep_foot') and not args.keep_foot:
                inference_config["keep_foot"] = False
            if hasattr(args, 'keep_upper') and args.keep_upper:
                inference_config["keep_upper"] = True
            if hasattr(args, 'keep_lower') and args.keep_lower:
                inference_config["keep_lower"] = True
            if hasattr(args, 'do_sr') and args.do_sr is not None:
                inference_config["do_sr"] = args.do_sr
            if hasattr(args, 'num_steps') and args.num_steps is not None:
                inference_config["num_steps"] = args.num_steps

            # V2版专用参数
            if hasattr(args, 'tight_mask') and args.tight_mask != 'loose':
                inference_config["tight_mask"] = args.tight_mask
            if hasattr(args, 'p_bbox_iou_ratio') and args.p_bbox_iou_ratio is not None:
                inference_config["p_bbox_iou_ratio"] = args.p_bbox_iou_ratio
            if hasattr(args, 'p_bbox_expand_ratio') and args.p_bbox_expand_ratio is not None:
                inference_config["p_bbox_expand_ratio"] = args.p_bbox_expand_ratio
            if hasattr(args, 'max_process_side_length') and args.max_process_side_length is not None:
                inference_config["max_process_side_length"] = args.max_process_side_length

            # 构建水印配置
            logo_info = {
                "add_logo": False,
                "position": 0,
                "language": 0,
                "opacity": 1.0
            }

            # AIGC隐式标识配置
            aigc_meta = {
                "content_producer": "volcengine_outfit_v2",
                "producer_id": f"outfit_v2_{int(time.time())}",
                "content_propagator": "volcengine",
                "propagate_id": f"propagate_v2_{int(time.time())}"
            }

            # 生成V2版换装图片
            result = ai.generate_outfit_image_v2(
                garment_urls=garment_urls,
                model_url=args.model_url,
                garment_types=garment_types,
                model_id=getattr(args, 'model_id', None),
                protect_mask_url=getattr(args, 'protect_mask_url', None),
                inference_config=inference_config,
                logo_info=logo_info,
                aigc_meta=aigc_meta,
                download=not getattr(args, 'no_download', False),
                filename=getattr(args, 'filename', None),
                req_image_store_type=getattr(args, 'req_image_store_type', 1)
            )
        else:
            # V1版：单件服装
            print(f"👤 模特图片URL: {args.model_url}")
            print(f"👔 服装图片URL: {args.garment_url}")

            # 构建推理配置 - 只有明确指定时才覆盖默认值
            inference_config = {}

            if hasattr(args, 'seed') and args.seed is not None:
                inference_config["seed"] = args.seed
            if hasattr(args, 'keep_head') and not args.keep_head:
                inference_config["keep_head"] = False
            if hasattr(args, 'keep_hand') and not args.keep_hand:
                inference_config["keep_hand"] = False
            if hasattr(args, 'keep_foot') and not args.keep_foot:
                inference_config["keep_foot"] = False
            if hasattr(args, 'keep_upper') and args.keep_upper:
                inference_config["keep_upper"] = True
            if hasattr(args, 'keep_lower') and args.keep_lower:
                inference_config["keep_lower"] = True
            if hasattr(args, 'do_sr') and args.do_sr is not None:
                inference_config["do_sr"] = args.do_sr
            if hasattr(args, 'num_steps') and args.num_steps is not None:
                inference_config["num_steps"] = args.num_steps

            # 构建水印配置
            logo_info = {
                "add_logo": False,
                "position": 0,
                "language": 0
            }

            # AIGC隐式标识配置
            aigc_meta = {
                "content_producer": "volcengine_outfit",
                "producer_id": f"outfit_{int(time.time())}",
                "content_propagator": "volcengine",
                "propagate_id": f"propagate_{int(time.time())}"
            }

            # 生成V1版换装图片
            result = ai.generate_outfit_image(
                model_url=args.model_url,
                garment_url=args.garment_url,
                model_id=getattr(args, 'model_id', '1'),
                garment_id=getattr(args, 'garment_id', '1'),
                inference_config=inference_config,
                logo_info=logo_info,
                aigc_meta=aigc_meta,
                download=not getattr(args, 'no_download', False),
                filename=getattr(args, 'filename', None)
            )

        if result:
            print("\n🎉 图片换装生成完成！")
            print("=" * 50)
            print(f"📄 结果文件: {result}")
            print("=" * 50)

    except Exception as e:
        print(f"❌ 换装失败: {str(e)}")


if __name__ == "__main__":
    main()