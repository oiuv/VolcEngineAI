# 火山引擎单图音频驱动视频生成客户端

基于火山引擎API的单图音频驱动视频生成客户端，支持普通模式、灵动模式和大画幅灵动模式。

## 功能特性

- ✅ 支持三种驱动模式：普通模式、灵动模式、大画幅灵动模式
- ✅ 完整的API签名认证机制
- ✅ 自动重试机制和错误处理
- ✅ 形象复用功能
- ✅ AIGC隐式标识支持
- ✅ 参数验证和模式信息展示

## 模式对比

| 模式 | 驱动范围 | 输出比例 | 最大音频长度 | 特点 |
|------|----------|----------|--------------|------|
| normal | 嘴部 | 原图比例 | 180秒 | 支持多人/多宠物，嘴部精准驱动 |
| loopy | 全脸 | 固定1:1 (512x512) | 180秒(真人)/90秒(宠物) | 运动幅度大，表情丰富 |
| loopyb | 全脸+身体 | 多种比例(16:9,9:16,3:4,4:3) | 45秒 | 半身驱动，不支持宠物 |

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境配置

在运行前需要设置环境变量：

**Windows:**
```cmd
set VOLCENGINE_ACCESS_KEY=your_access_key_here
set VOLCENGINE_SECRET_KEY=your_secret_key_here
```

**Linux/Mac:**
```bash
export VOLCENGINE_ACCESS_KEY=your_access_key_here
export VOLCENGINE_SECRET_KEY=your_secret_key_here
```

## 快速开始

### 基本用法

```python
from volcengine_avatar_client import VolcEngineAvatarClient

# 初始化客户端
client = VolcEngineAvatarClient(
    access_key="your_access_key",
    secret_key="your_secret_key"
)

# 从图片和音频生成视频（灵动模式）
result = client.generate_video_from_image_audio(
    image_url="https://example.com/image.jpg",
    audio_url="https://example.com/audio.mp3",
    mode="loopy"
)

print(f"视频URL: {result['video_url']}")
print(f"形象ID: {result['resource_id']}")
```

### 分步骤操作

```python
# 步骤1：创建形象
task_id = client.create_role(image_url, "normal")
role_result = client.wait_for_completion(task_id, "normal", "role")
resource_id = role_result["resource_id"]

# 步骤2：生成视频
video_task_id = client.generate_video(resource_id, audio_url, "normal")
video_result = client.wait_for_completion(video_task_id, "normal", "video")

print(f"视频URL: {video_result['video_url']}")
```

### 复用已有形象

```python
# 使用已创建的形象生成新视频
video_task_id = client.generate_video(existing_resource_id, new_audio_url, "normal")
video_result = client.wait_for_completion(video_task_id, "normal", "video")
```

### 添加AIGC隐式标识

```python
aigc_meta = {
    "content_producer": "your_producer_id",
    "producer_id": "unique_producer_id_123",
    "content_propagator": "your_propagator_id",
    "propagate_id": "unique_propagate_id_456"
}

result = client.generate_video_from_image_audio(
    image_url=image_url,
    audio_url=audio_url,
    mode="loopy",
    aigc_meta=aigc_meta
)
```

## 运行示例

```bash
python examples.py
```

示例程序提供：
1. 普通模式示例
2. 灵动模式示例
3. 大画幅灵动模式示例
4. 复用形象示例
5. 模式信息展示

## API方法说明

### VolcEngineAvatarClient

#### 初始化
```python
client = VolcEngineAvatarClient(access_key, secret_key, region="cn-north-1", service="cv")
```

#### 创建形象
```python
task_id = client.create_role(image_url, mode="normal")
```

#### 获取形象创建结果
```python
result = client.get_role_result(task_id, mode="normal")
```

#### 生成视频
```python
task_id = client.generate_video(resource_id, audio_url, mode="normal", aigc_meta=None)
```

#### 获取视频生成结果
```python
result = client.get_video_result(task_id, mode="normal", aigc_meta=None)
```

#### 等待任务完成
```python
result = client.wait_for_completion(task_id, mode, operation_type, max_wait_time=600)
```

#### 完整流程
```python
result = client.generate_video_from_image_audio(image_url, audio_url, mode="normal", aigc_meta=None)
```

## 注意事项

1. **图片要求**：
   - 普通模式：支持真人、动漫、宠物图片
   - 灵动模式：建议单人/单宠物正面清晰图片
   - 大画幅模式：必须是16:9、9:16、3:4、4:3比例的半身图片

2. **音频要求**：
   - 普通模式：最长180秒
   - 灵动模式：真人180秒，宠物90秒
   - 大画幅模式：最长45秒

3. **费用说明**：
   - 形象创建：0.1元/形象
   - 视频生成：0.3元/秒

4. **输出限制**：
   - 视频链接有效期：1小时
   - 任务结果有效期：12小时

## 错误处理

客户端内置了完整的错误处理机制：

- 网络超时自动重试
- HTTP状态码错误识别
- API错误码处理
- 参数验证

## 文件结构

```
VolcEngineAI/
├── volcengine_avatar_client.py  # 主客户端
├── config.py                   # 配置文件
├── utils.py                    # 工具函数
├── examples.py                 # 示例代码
├── requirements.txt            # 依赖列表
└── README.md                   # 说明文档
```

## 许可证

本项目仅供学习和研究使用，请遵守火山引擎API的使用条款。