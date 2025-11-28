# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述
火山引擎AI视频生成客户端，支持多种AI功能：单图音频驱动视频生成、创意特效视频生成、视频改口型、即梦AI、单图视频驱动、图片换装等。

## 核心架构

### 命名规范
采用统一的客户端命名规范：`功能类型_具体用途_client.py`

#### 视频类 (video_)
- `video_audio_driven_client.py` - 单图音频驱动视频生成
- `video_effect_client.py` - 创意特效视频生成
- `video_translation_client.py` - 视频翻译（待开发）
- `video_lip_sync_client.py` - 视频改口型
- `video_video_driven_client.py` - 单图视频驱动
- `jimeng_omni_client.py` - 即梦AI OmniHuman数字人生成
- `jimeng_mimic_client.py` - 即梦AI动作模仿
- `video_product_client.py` - 商品互动（待开发）

#### 图像类 (image_)
- `image_generation_client.py` - 文生图、图生图（待开发）
- `image_effect_client.py` - 图像特效（待开发）
- `image_cartoon_client.py` - 智能绘图漫画版（待开发）
- `image_outfit_client.py` - 图片换装

#### 音频类 (audio_)
- `audio_clone_client.py` - 声音克隆（待开发）
- `audio_music_client.py` - 音乐生成（待开发）

### 目录结构
```
VolcEngineAI/
├── volcengine_ai.py              # 主入口文件
├── src/                          # 源代码目录
│   ├── config.py                 # 配置管理
│   ├── utils.py                  # 工具函数
│   ├── core/                     # 核心模块
│   │   ├── video_audio_driven_client.py
│   │   ├── video_lip_sync_client.py
│   │   ├── video_effect_client.py
│   │   ├── video_video_driven_client.py
│   │   ├── jimeng_omni_client.py
│   │   ├── jimeng_mimic_client.py
│   │   └── image_outfit_client.py
│   └── modules/                  # 功能模块
│       └── avatar_manager.py     # 形象管理
├── data/                         # 数据目录
│   └── avatars.json              # 保存的形象数据
├── requirements.txt              # 依赖列表
├── .gitignore                    # Git忽略规则
├── README.md                     # 说明文档
└── CLAUDE.md                     # Claude开发记忆文件
```

## 已实现功能

### 1. 单图音频驱动视频生成 (VideoAudioDrivenClient)
- **支持模式**: normal(普通), loopy(灵动), loopyb(大画幅灵动)
- **功能特点**:
  - 普通模式：嘴部驱动，支持多人/多宠物
  - 灵动模式：全脸驱动，1:1输出
  - 大画幅模式：全身+脸部驱动，多种比例
- **命令结构**:
  - `va create-avatar <image-url> [--mode normal|loopy|loopyb]`
  - `va query-avatar <task-id> --mode <mode>`
  - `va create-video <resource-id> <audio-url> [--mode normal|loopy|loopyb]`
  - `va query-video <task-id> --mode <mode> [--download]`
  - `va create <image-url> <audio-url> [--mode normal|loopy|loopyb]`  # 一键生成
  - `va avatars [--mode normal|loopy|loopyb]`  # 查看可用形象

### 2. 视频改口型 (VideoLipSyncClient)
- **支持模式**: lite(Lite模式), basic(Basic模式)
- **功能特点**:
  - Lite模式：支持单人正面视频，最大音频长度240秒
  - Basic模式：支持单人复杂场景，最大音频长度150秒
  - 人声分离、场景切分、视频循环等高级功能
- **命令结构**:
  - `vl create <video-url> <audio-url> [--mode lite|basic] [--separate-vocal] [--open-scenedet] [--align-audio] [--align-audio-reverse] [--templ-start-seconds]`
  - `vl query <task-id> --mode <mode> [--download]`

### 3. 即梦AI数字人生成 (VideoJimengClient)
- **支持版本**: OmniHuman 1.0和1.5两个版本
- **功能特点**:
  - 1.0版：主体识别 + 视频生成（480P，1元/秒，建议音频<15秒）
  - 1.5版：主体识别 + 对象检测 + 视频生成（1080P，1.2元/秒，音频<35秒）
  - 支持提示词控制、多主体指定、情感表演、宠物/动漫形象
  - 智能处理：自动格式转码、参数验证、错误处理
  - 完整的任务流程：主体检测 → 对象检测(1.5版) → 视频生成
- **命令结构**:
  - `jm va detect <image-url> <prompt> [--mode 1.0|1.5]`  # 主体检测
  - `jm va detect-object <subject-id> <detect-task-id> --mode 1.5`  # 对象检测（1.5版专用）
  - `jm va generate <subject-id> <detect-task-id> <audio-url> [--mode 1.0|1.5] [--object-task-id ID]`  # 生成视频
  - `jm va query <task-id> --mode <mode>`  # 查询结果
  - `jm va create-avatar <image-url> <audio-url> <prompt> --mode <mode> [--subject-id ID] [--enable-object-detection] [--no-wait]`  # 一键生成
  - `jm query <task-id> [--operation-type detect|detect_object|generate] [--version 1.0|1.5] [--download]`

### 4. 创意特效视频生成 (VideoEffectClient)
- **支持版本**: V1和V2接口，自动识别
- **模板数量**: 49个模板（V1: 20个，V2: 29个）
- **模板分类**:
  - V1版本：卡通变身、召唤坐骑、万物生花、情感互动、AI环绕、天赐宝宝
  - V2版本：卡通变身、特效场景、情感互动、变装换装、动感舞蹈
- **特殊功能**:
  - 双图模板支持（用`|`分隔URL）
  - 高清版本（480p/720p）
  - 分屏设置（V2版本）
- **命令结构**:
  - `ve create <image-url> <template-id>`
  - `ve query <task-id> [--download]`
  - `ve templates`  # 查看可用模板

### 5. 即梦AI动作模仿 (VideoJimengMimicClient)
- **服务标识**: jimeng_dream_actor_m1_gen_video_cv
- **功能特点**:
  - 输入图片+模板视频，生成动作模仿视频
  - 支持真人、动漫、宠物的动作和表情模仿
  - 使用CVSync2AsyncSubmitTask/GetResult异步接口
- **命令结构**:
  - `jm mimic create <image-url> <video-url>`  # 创建动作模仿任务
  - `jm mimic query <task-id>`  # 查询任务状态

### 6. 单图视频驱动 (VideoVideoDrivenClient)
- **服务标识**: realman_avatar_imitator_v2v_gen_video
- **功能特点**:
  - 输入图片+驱动视频，生成模仿视频动作的视频
  - 支持人脸表情和肢体动作驱动
  - 输出分辨率：960x540或896x672
  - 驱动视频限制：最大30秒，支持mp4/mov/webm格式
- **配置信息**:
  - 图片格式：jpeg/jpg/png，分辨率512x512以上，最大4096x4096
  - 视频格式：mp4/mov/webm，分辨率540-2048，最大30秒
  - 收费标准：0.3元/秒，并发限制1
- **命令结构**:
  - `vv create <image-url> <video-url>`  # 创建单图视频驱动任务
  - `vv query <task-id>`  # 查询任务状态

### 7. 图片换装 (ImageOutfitClient)
- **服务标识**:
  - V1版：dressing_diffusion（同步接口）
  - V2版：dressing_diffusionV2（异步接口）
- **功能特点**:
  - 输入模特图 + 服装图，输出模特穿着指定服装的图片
  - 支持复杂的模特pose和任意品类/款式的服装图输入
  - 支持非服饰和低质量的服饰输入，能合成真实的褶皱和光影
  - V1版同步接口，一次返回结果
  - V2版异步接口，支持多件服装组合（上衣+下衣），丰富推理参数
- **配置信息**:
  - 图片格式：JPG/JPEG/PNG/JFIF，小于5MB，小于4096*4096
  - 收费标准：1元/次，并发限制1
  - V2版最多支持2件服装，支持服装类型分类（upper/bottom/full）
- **命令结构**:
  - `io generate <model_url> <garment_url>`  # V1版生成换装图片
  - `io generate <model_url> <garment_url> --version 2`  # V2版生成换装图片
  - `io generate <model_url> "upper-url|bottom-url" --version 2 --garment-types upper bottom`  # V2版多件服装

### 8. 形象管理系统 (avatar_manager)
- 本地JSON存储形象信息
- 支持按模式筛选和管理
- 自动保存创建成功的形象

## 技术实现

### API认证
- 使用火山引擎HMAC-SHA256签名
- 环境变量管理API密钥
- 完整的请求头和签名生成

### 错误处理
- 网络超时自动重试（最多3次）
- HTTP状态码详细处理
- API错误码识别
- 参数验证和模式强制验证

### 状态管理
- 异步任务状态查询
- 智能等待机制
- 自动版本检测（特效视频）

## 环境配置
```bash
# Linux/Mac
export VOLCENGINE_ACCESS_KEY=your_access_key_here
export VOLCENGINE_SECRET_KEY=your_secret_key_here

# Windows
set VOLCENGINE_ACCESS_KEY=your_access_key_here
set VOLCENGINE_SECRET_KEY=your_secret_key_here
```

## 常用命令

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行程序
```bash
# 查看帮助
python volcengine_ai.py -h

# 列出所有特效模板
python volcengine_ai.py ve templates

# 单图音频驱动 - 一键生成
python volcengine_ai.py va create https://image.jpg https://audio.mp3 --mode loopyb

# 创建数字形象
python volcengine_ai.py va create-avatar https://image.jpg --mode loopyb

# 查询形象状态
python volcengine_ai.py va query-avatar 123456 --mode loopyb

# 视频改口型 - Lite模式（推荐）
python volcengine_ai.py vl create https://video.mp4 https://audio.mp3 --mode lite

# 视频改口型 - Basic模式（复杂场景）
python volcengine_ai.py vl create https://video.mp4 https://audio.mp3 --mode basic --separate-vocal --open-scenedet

# 查询视频改口型状态
python volcengine_ai.py vl query 123456 --mode lite --download

# 创意特效视频生成
python volcengine_ai.py ve create https://image.jpg multi_style_stacking_dolls

# 查询视频状态并下载
python volcengine_ai.py va query-video 123456 --mode loopyb --download
python volcengine_ai.py ve query 789012 --download

# 查看可用形象
python volcengine_ai.py va avatars --mode loopyb

# 即梦AI数字人生成 - 1.0版一键生成
python volcengine_ai.py jm va create-avatar https://image.jpg https://audio.mp3 "一个微笑的年轻女性" --mode 1.0

# 即梦AI数字人生成 - 1.5版带对象检测
python volcengine_ai.py jm va create-avatar https://image.jpg https://audio.mp3 "一个穿着蓝色衬衫的男性" --mode 1.5 --subject-id 1 --enable-object-detection

# 即梦AI分步操作 - 主体检测
python volcengine_ai.py jm va detect https://image.jpg "一个可爱的宠物" --mode 1.5

# 即梦AI分步操作 - 对象检测（1.5版）
python volcengine_ai.py jm va detect-object 1 12345678 --mode 1.5

# 即梦AI分步操作 - 查询结果
python volcengine_ai.py jm va query 87654321 --mode 1.5

# 即梦AI动作模仿
python volcengine_ai.py jm mimic create https://image.jpg https://video.mp4

# 查询即梦AI动作模仿状态
python volcengine_ai.py jm mimic query 123456789

# 单图视频驱动
python volcengine_ai.py vv create https://image.jpg https://driving_video.mp4

# 查询单图视频驱动状态
python volcengine_ai.py vv query 987654321

# 图片换装
python volcengine_ai.py io generate https://model.jpg https://garment.jpg

# 图片换装（指定保存文件名）
python volcengine_ai.py io generate https://model.jpg https://garment.jpg --filename my_outfit.png
```

## 开发规范

### 代码风格
- 使用类型注解
- 完整的docstring文档
- 异常处理全覆盖
- 模块化设计

### 模块化架构原则（新增）
**所有功能必须遵循模块化组合原则，避免重复造轮子：**

1. **基础函数**：只负责单一操作
   - `create_xxx()` / `submit_xxx_task()`: 只提交任务，返回task_id
   - `query_xxx()`: 循环查询直到完成，自动下载

2. **组合函数**：调用基础函数
   - `generate_xxx()` / `change_xxx()`: create_xxx() + query_xxx()
   - 严禁在组合函数中重复实现查询逻辑

### 异步任务处理模式
火山引擎API统一采用异步任务模式：
1. 提交任务 → 获得task_id
2. 循环查询 → 检查任务状态（15秒间隔，10分钟超时）
3. 获取结果 → 自动下载内容

### 查询函数统一标准（新增）
所有异步查询函数必须具备：
```python
def query_xxx(args):
    """查询任务状态（循环等待直到完成）"""
    import time
    start_time = time.time()
    max_wait_time = 600  # 10分钟
    check_interval = 15  # 15秒检查一次

    while time.time() - start_time < max_wait_time:
        # 查询逻辑
        # 状态检查
        # 自动下载
        time.sleep(check_interval)
```

### 禁止模式（新增）
```python
# ❌ 错误：在组合函数中重复实现查询逻辑
def generate_xxx(args):
    task_id = submit_task(args)
    # 禁止：重复实现查询逻辑
    while True:
        result = query_status(task_id)
        if result['status'] == 'done':
            break
        time.sleep(15)

# ✅ 正确：调用现有查询函数
def generate_xxx(args):
    task_id = submit_xxx_task(args)
    class QueryArgs:
        def __init__(self):
            self.task_id = task_id
            # 其他必要参数
    query_xxx(QueryArgs())
```

### 测试流程
1. 功能测试：验证所有命令正常工作
2. 错误测试：验证异常情况处理
3. 集成测试：验证完整流程

### 开发流程
1. 更新核心客户端代码（src/core/）
2. 更新主程序导入和调用（volcengine_ai.py）
3. 更新README文档
4. 更新CLAUDE.md记忆文件

## 重要架构说明

### 统一入口模式
项目采用统一入口设计，`volcengine_ai.py` 是主入口文件，通过 `argparse` 解析命令行参数并调用相应功能模块。

### 延迟导入机制
为避免循环依赖，主程序采用延迟导入机制：
```python
# 在 _init_clients() 中延迟导入
from src.core.video_audio_driven_client import VideoAudioDrivenClient
from src.core.video_effect_client import VideoEffectClient
```

### 异步任务处理
火山引擎API采用异步任务模式：
1. 提交任务 → 获得task_id
2. 轮询查询 → 检查任务状态
3. 获取结果 → 下载/处理内容

### 自动版本检测
特效视频支持V1和V2两个版本接口，系统会根据模板ID自动选择对应版本：
- V1版本：req_key = "i2v_bytedance_effects_v1"
- V2版本：req_key = "i2v_template_cv_v2"

## 开发经验总结

### 已解决的技术挑战
1. **特效视频结果类型处理**: 通过检查返回结果类型，智能区分完整结果和任务ID
2. **多版本接口统一**: 通过自动版本检测，无缝支持V1和V2两个版本的特效视频接口
3. **命名规范统一**: 建立了清晰的`功能类型_具体用途_client.py`命名体系
4. **模块化架构统一**: 所有异步功能采用create+query组合模式，避免重复造轮子

## 未来开发计划

### 视频类功能
- 视频翻译 (video_translation_client.py)
- 商品互动 (video_product_client.py)

### 图像类功能
- 文生图、图生图 (image_generation_client.py)
- 图像特效 (image_effect_client.py)
- 智能绘图漫画版 (image_cartoon_client.py)
- 图片换装V2版 (image_outfit_client.py V2版)

### 音频类功能
- 声音克隆 (audio_clone_client.py)
- 音乐生成 (audio_music_client.py)

## 重要提醒

1. **保持命名规范一致**: 新功能必须遵循统一的命名规范
2. **模块化原则**: 永远不要重复实现已有功能，必须调用现有模块
3. **一致性**: 所有查询函数必须具备相同的循环等待逻辑
4. **完整文档更新**: 每次功能更新后必须同步更新README和CLAUDE.md
5. **错误处理**: 所有新功能必须包含完整的错误处理机制
6. **向后兼容**: 新版本应保持对旧版本的兼容性
7. **测试验证**: 新功能开发完成后必须经过完整测试

## 版本历史
- v1.0: 单图音频驱动视频生成
- v1.1: 创意特效视频生成（V1+V2）
- v1.2: 命名规范统一和架构优化
- v1.3: 命令行结构重构，优化用户体验
- v1.4: 修正命名不一致问题，统一命令前缀规范
- v1.5: 新增视频改口型功能（vl命令）
- v1.6: 新增即梦AI功能（jm命令）
- v2.0: 模块化架构统一，所有异步功能采用create+query组合模式
- v2.1: 新增单图视频驱动功能(vv命令)和即梦AI动作模仿功能
- v2.2: 新增图片换装功能(io命令)V1版
- v2.3: 新增图片换装功能V2版，支持多件服装和异步处理

---
*最后更新: 2025-11-28*