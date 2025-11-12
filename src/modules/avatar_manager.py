"""
形象管理器 - 保存和管理形象ID
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

AVATAR_DATA_FILE = "data/avatars.json"


class AvatarManager:
    """形象管理器"""

    def __init__(self, data_file: str = AVATAR_DATA_FILE):
        self.data_file = data_file
        self._load_data()

    def _load_data(self):
        """加载形象数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except:
                self.data = {"avatars": {}, "created_at": datetime.now().isoformat()}
        else:
            self.data = {"avatars": {}, "created_at": datetime.now().isoformat()}

    def _save_data(self):
        """保存形象数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def save_avatar(self, task_id: str, result: Dict[str, Any], mode: str, resp_data: Dict[str, Any] = None):
        """保存形象结果"""
        if "resource_id" not in result:
            return False

        # 使用API返回的时间信息，如果没有则用当前时间
        avatar_time = None
        if resp_data:
            # 优先使用 finished_at，其次使用 processed_at
            avatar_time = resp_data.get("finished_at") or resp_data.get("processed_at")
            if avatar_time:
                # 转换时间戳为ISO格式
                avatar_time = datetime.fromtimestamp(avatar_time).isoformat()

        avatar_info = {
            "task_id": task_id,
            "resource_id": result["resource_id"],
            "role_type": result.get("role_type", "unknown"),
            "face_position": result.get("face_position", []),
            "mode": mode,
            "created_at": avatar_time or datetime.now().isoformat(),
            "api_times": {
                "received_at": resp_data.get("received_at"),
                "processed_at": resp_data.get("processed_at"),
                "finished_at": resp_data.get("finished_at")
            } if resp_data else None
        }

        self.data["avatars"][task_id] = avatar_info
        self.data["last_updated"] = datetime.now().isoformat()
        self._save_data()

        print(f"✅ 形象已保存: {result['resource_id']} ({mode}模式)")
        return True

    def get_avatar_by_task_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """根据任务ID获取形象信息"""
        return self.data["avatars"].get(task_id)

    def get_avatar_by_resource_id(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """根据形象ID获取形象信息"""
        for task_id, avatar_info in self.data["avatars"].items():
            if avatar_info["resource_id"] == resource_id:
                return avatar_info
        return None

    def get_latest_avatar(self, mode: str = None) -> Optional[Dict[str, Any]]:
        """获取最新的形象"""
        avatars = list(self.data["avatars"].values())

        if mode:
            avatars = [a for a in avatars if a.get("mode") == mode]

        if not avatars:
            return None

        # 按创建时间排序，返回最新的
        avatars.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return avatars[0]

    def list_avatars(self, mode: str = None):
        """列出所有形象"""
        avatars = self.data["avatars"]

        if mode:
            avatars = {k: v for k, v in avatars.items() if v.get("mode") == mode}

        if not avatars:
            print("📭 暂无保存的形象")
            return

        print(f"📋 保存的形象列表:")
        print("-" * 80)

        for task_id, info in avatars.items():
            status_icon = "🎭" if info.get("mode") == "normal" else "✨" if info.get("mode") == "loopy" else "🖼️"
            print(f"{status_icon} {info.get('mode', 'unknown')}模式")
            print(f"   形象ID: {info['resource_id']}")
            print(f"   任务ID: {task_id}")
            print(f"   类型: {info.get('role_type', 'unknown')}")
            print(f"   创建时间: {info.get('created_at', 'unknown')}")
            print("-" * 80)

    def get_resource_id_by_task_id(self, task_id: str) -> Optional[str]:
        """根据任务ID获取形象ID"""
        avatar_info = self.get_avatar_by_task_id(task_id)
        return avatar_info["resource_id"] if avatar_info else None


# 全局形象管理器实例
avatar_manager = AvatarManager()