"""
火山引擎AI统一入口
支持多种AI功能：单图音频驱动、图像生成、文本模型等
"""

import os
import sys
import argparse
import requests
from typing import Dict, Any, Optional

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
        self._init_clients()

    def _init_clients(self):
        """初始化各个功能模块的客户端"""
        # 延迟导入，避免循环依赖
        try:
            from src.core.volcengine_avatar_client import VolcEngineAvatarClient
            self._avatar_client = VolcEngineAvatarClient(self.access_key, self.secret_key)
        except ImportError:
            self._avatar_client = None

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

    def generate_avatar_video_from_image_audio(self, image_url: str, audio_url: str, mode: str = "normal", aigc_meta: Optional[Dict] = None):
        """从图片和音频生成完整视频"""
        if not self._avatar_client:
            raise Exception("单图音频驱动模块未正确加载")
        return self._avatar_client.generate_video_from_image_audio(image_url, audio_url, mode, aigc_meta)

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


def create_avatar(args):
    """创建形象"""
    ai = VolcEngineAI()
    try:
        task_id = ai.create_avatar(args.image_url, args.mode)
        print(f"✅ 形象创建任务已提交")
        print(f"🆔 任务ID: {task_id}")
    except Exception as e:
        print(f"❌ 创建失败: {str(e)}")


def query_avatar(args):
    """查询形象状态"""
    ai = VolcEngineAI()
    try:
        print(f"🔍 查询任务ID: {args.task_id} ({args.mode}模式)")

        result = ai.get_avatar_result(args.task_id, args.mode)

        if "resource_id" in result:
            print(f"✅ 形象创建成功！")
            print(f"🆔 形象ID: {result['resource_id']}")
            print(f"📋 类型: {result.get('role_type', 'unknown')}")
            print(f"🎯 模式: {args.mode}")

            # 保存形象信息，包含API响应数据
            avatar_manager.save_avatar(args.task_id, result, args.mode, result.get("resp_data"))
            return
        elif result.get("status") == "done":
            print(f"✅ 形象创建完成（{args.mode}模式）")
            return
        else:
            status = result.get("status", "unknown")

            # 根据状态显示具体信息
            if status == "in_queue":
                print(f"🔄 {args.mode}模式: 任务排队中")
            elif status == "generating":
                print(f"⚡ {args.mode}模式: 正在处理中")
                print("💡 提示: 通常需要1-5分钟，请耐心等待")
            elif status == "not_found":
                print(f"❌ {args.mode}模式: 任务未找到")
                print("💡 请检查任务ID是否正确，或使用正确的模式查询")
            elif status == "expired":
                print(f"⏰ {args.mode}模式: 任务已过期")
                print("💡 任务有效期为12小时，过期后需要重新提交")
            else:
                print(f"📊 任务状态: {status}")

    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")
        if "未找到" in str(e) or "not_found" in str(e).lower():
            print(f"💡 提示: 请确认使用正确的模式查询（--mode {args.mode}）")


def generate_video(args):
    """生成视频"""
    ai = VolcEngineAI()
    try:
        task_id = ai.generate_avatar_video(args.resource_id, args.audio_url, args.mode)
        print(f"✅ 视频生成任务已提交")
        print(f"🆔 任务ID: {task_id}")
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")


def query_video(args):
    """查询视频状态"""
    ai = VolcEngineAI()
    try:
        print(f"🔍 查询任务ID: {args.task_id} ({args.mode}模式)")

        result = ai.get_video_result(args.task_id, args.mode)

        if "video_url" in result:
            print(f"✅ 视频生成成功！")
            print(f"📹 视频URL: {result['video_url']}")
            if result.get('video_meta'):
                meta = result['video_meta']
                print(f"📐 尺寸: {meta.get('Width')}x{meta.get('Height')}")
                print(f"⏱️ 时长: {meta.get('Duration')}秒")
            print(f"🎯 模式: {args.mode}")

            # 自动下载视频
            if args.download:
                video_url = result['video_url']
                filename = args.filename or f"video_{args.task_id}.mp4"
                download_video(video_url, filename)
            return
        elif result.get("status") == "done":
            print(f"✅ 视频生成完成（{args.mode}模式）")
            return
        else:
            status = result.get("status", "unknown")

            # 根据状态显示具体信息
            if status == "in_queue":
                print(f"🔄 {args.mode}模式: 任务排队中")
            elif status == "generating":
                print(f"⚡ {args.mode}模式: 正在处理中")
                print("💡 提示: 通常需要1-5分钟，请耐心等待")
            elif status == "not_found":
                print(f"❌ {args.mode}模式: 任务未找到")
                print("💡 请检查任务ID是否正确，或使用正确的模式查询")
            elif status == "expired":
                print(f"⏰ {args.mode}模式: 任务已过期")
                print("💡 任务有效期为12小时，过期后需要重新提交")
            else:
                print(f"📊 任务状态: {status}")

    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")
        if "未找到" in str(e) or "not_found" in str(e).lower():
            print(f"💡 提示: 请确认使用正确的模式查询（--mode {args.mode}）")


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


def generate_all(args):
    """一键生成完整流程"""
    ai = VolcEngineAI()
    try:
        print(f"开始生成视频（{args.mode}模式）...")
        print("💡 提示: 大画幅模式处理时间较长，请耐心等待（3-10分钟）")

        # 根据模式设置不同的超时时间
        if args.mode == "loopyb":
            timeout = 600  # 大画幅模式10分钟
        else:
            timeout = 300  # 其他模式5分钟

        result = ai.generate_avatar_video_from_image_audio(
            image_url=args.image_url,
            audio_url=args.audio_url,
            mode=args.mode,
            max_wait_time=timeout
        )
        print("🎉 视频生成成功！")
        print(f"📹 视频URL: {result['video_url']}")
        print(f"🆔 形象ID: {result['resource_id']}")
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")
        if "超时" in str(e):
            print("💡 建议: 可以单独查询任务状态")
            print(f"   python volcengine_ai.py query-video --task-id 视频任务ID --mode {args.mode}")


def main():
    """统一入口主函数"""
    parser = argparse.ArgumentParser(description="火山引擎AI平台")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 创建形象
    parser_create = subparsers.add_parser('create-avatar', help='创建数字形象')
    parser_create.add_argument('--image-url', required=True, help='图片URL')
    parser_create.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], default='normal', help='模式选择')
    parser_create.set_defaults(func=create_avatar)

    # 查询形象状态
    parser_query_avatar = subparsers.add_parser('query-avatar', help='查询形象创建状态')
    parser_query_avatar.add_argument('--task-id', required=True, help='任务ID')
    parser_query_avatar.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], required=True, help='创建时使用的模式')
    parser_query_avatar.set_defaults(func=query_avatar)

    # 生成视频
    parser_video = subparsers.add_parser('generate-video', help='生成角色视频')
    parser_video.add_argument('--resource-id', required=True, help='形象ID')
    parser_video.add_argument('--audio-url', required=True, help='音频URL')
    parser_video.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], default='normal', help='模式选择')
    parser_video.set_defaults(func=generate_video)

    # 查询视频状态
    parser_query_video = subparsers.add_parser('query-video', help='查询视频生成状态')
    parser_query_video.add_argument('--task-id', required=True, help='任务ID')
    parser_query_video.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], required=True, help='生成时使用的模式')
    parser_query_video.add_argument('--download', action='store_true', help='下载视频到本地')
    parser_query_video.add_argument('--filename', help='保存文件名')
    parser_query_video.set_defaults(func=query_video)

    # 一键生成
    parser_all = subparsers.add_parser('generate-all', help='一键生成完整流程')
    parser_all.add_argument('--image-url', required=True, help='图片URL')
    parser_all.add_argument('--audio-url', required=True, help='音频URL')
    parser_all.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], default='normal', help='模式选择')
    parser_all.set_defaults(func=generate_all)

    # 列出保存的形象
    parser_list = subparsers.add_parser('list-avatars', help='列出保存的形象')
    parser_list.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], help='按模式筛选')
    parser_list.set_defaults(func=list_avatars)

    # 使用最新形象生成视频
    parser_use_latest = subparsers.add_parser('use-latest-avatar', help='使用最新的形象生成视频')
    parser_use_latest.add_argument('--audio-url', required=True, help='音频URL')
    parser_use_latest.add_argument('--mode', choices=['normal', 'loopy', 'loopyb'], help='指定模式的最新形象')
    parser_use_latest.set_defaults(func=use_latest_avatar)

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
    args.func(args)


if __name__ == "__main__":
    main()