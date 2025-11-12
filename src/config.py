"""
火山引擎API配置文件
"""
import os

# API配置 - 从环境变量读取
ACCESS_KEY = os.getenv("VOLCENGINE_ACCESS_KEY")
SECRET_KEY = os.getenv("VOLCENGINE_SECRET_KEY")

# 区域配置
REGION = "cn-north-1"  # 固定值
SERVICE = "cv"         # 固定值

# API版本
API_VERSION = "2022-08-31"

# 服务标识映射
REQ_KEYS = {
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

# 超时配置
DEFAULT_TIMEOUT = 30  # 请求超时时间（秒）
MAX_WAIT_TIME = 600   # 最大等待时间（秒）
CHECK_INTERVAL = 5    # 检查间隔（秒）

# 重试配置
MAX_RETRIES = 3       # 最大重试次数
RETRY_DELAY = 2       # 重试延迟（秒）