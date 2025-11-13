"""
工具函数
"""

import time
from functools import wraps
from typing import Callable, Any


def retry(max_retries: int = 3, delay: int = 2, exceptions: tuple = (Exception,)):
    """
    重试装饰器

    Args:
        max_retries: 最大重试次数
        delay: 重试延迟时间（秒）
        exceptions: 需要重试的异常类型
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"操作失败：{str(e)}，{delay}秒后重试... (尝试 {attempt + 1}/{max_retries + 1})")
                        time.sleep(delay)
                    else:
                        print(f"操作失败，已达到最大重试次数 ({max_retries + 1})")
                        break

            raise last_exception

        return wrapper
    return decorator


def validate_url(url: str) -> bool:
    """
    验证URL格式

    Args:
        url: 要验证的URL

    Returns:
        是否为有效URL
    """
    if not url or not isinstance(url, str):
        return False

    return (url.startswith('http://') or url.startswith('https://')) and len(url) > 10


def validate_mode(mode: str) -> bool:
    """
    验证模式参数

    Args:
        mode: 模式名称

    Returns:
        是否为有效模式
    """
    valid_modes = ["normal", "loopy", "loopyb"]
    return mode in valid_modes


def get_mode_description(mode: str) -> str:
    """
    获取模式描述

    Args:
        mode: 模式名称

    Returns:
        模式描述
    """
    descriptions = {
        "normal": "普通模式 - 驱动范围：嘴部，支持原图比例输出",
        "loopy": "灵动模式 - 驱动范围：全脸，固定1:1比例输出(512*512)",
        "loopyb": "大画幅灵动模式 - 驱动范围：全脸+身体，支持多种比例输出"
    }
    return descriptions.get(mode, "未知模式")


def format_duration(seconds: float) -> str:
    """
    格式化时长

    Args:
        seconds: 秒数

    Returns:
        格式化后的时长字符串
    """
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}分{remaining_seconds:.1f}秒"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        remaining_seconds = seconds % 60
        return f"{hours}时{remaining_minutes}分{remaining_seconds:.1f}秒"


def get_supported_audio_length(mode: str) -> int:
    """
    获取模式支持的最大音频长度

    Args:
        mode: 模式名称

    Returns:
        最大音频长度（秒）
    """
    audio_limits = {
        "normal": 180,
        "loopy": 180,  # 真人180秒，宠物90秒，取较大值
        "loopyb": 45
    }
    return audio_limits.get(mode, 180)


def get_output_resolution(mode: str, aspect_ratio: str = None) -> tuple:
    """
    获取输出分辨率

    Args:
        mode: 模式名称
        aspect_ratio: 画幅比例（仅对loopyb有效）

    Returns:
        (宽度, 高度)
    """
    if mode == "loopyb" and aspect_ratio:
        resolutions = {
            "4:3": (768, 576),
            "3:4": (576, 768),
            "16:9": (896, 504),
            "9:16": (504, 896)
        }
        return resolutions.get(aspect_ratio, (512, 512))
    elif mode == "loopy":
        return (512, 512)
    else:
        return None  # 普通模式保持原图比例