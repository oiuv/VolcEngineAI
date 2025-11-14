# 火山引擎AI视频生成客户端

基于火山引擎API的AI视频生成客户端，支持单图音频驱动视频生成、视频改口型和创意特效视频生成。

## 产品介绍

### 1. 单图音频驱动视频生成
根据用户上传的单张图片+音频，生成该图片对应的视频效果。用户上传的单张图片可以是人像图片，也可以是宠物图片/动漫图片等。

### 2. 视频改口型
输入一段单人口播视频+音频，在保留说话人形象特点的前提下，将视频中的人物口型根据指定的音频输入进行修改。支持Lite模式和Basic模式，适用于各种场景需求。

### 3. 创意特效视频生成
基于单张图片或双张图片，使用AI技术生成各种创意特效视频，支持49种不同的特效模板，涵盖卡通变身、情感互动、变装换装等多种风格。

## 驱动模式说明

### 单图音频驱动模式

| 模式 | 驱动范围 | 输出比例 | 最大音频长度 | 支持类型 | 特点 |
|------|----------|----------|--------------|----------|------|
| **普通模式**<br>(normal) | 嘴部 | 原图比例 | 180秒 | 真人、动漫、宠物 | 嘴部精准驱动，支持多人/多宠物 |
| **灵动模式**<br>(loopy) | 全脸 | 固定1:1<br>(512*512) | 180秒(真人)<br>90秒(宠物) | 真人、动漫、宠物 | 运动幅度大，表情丰富，随机性强 |
| **大画幅灵动模式**<br>(loopyb) | 全脸+膝盖以上身体 | 多种比例<br>(16:9,9:16,3:4,4:3) | 45秒 | 真人、动漫<br>(不支持宠物) | 半身驱动，身体+脸部动作 |

### 视频改口型模式

| 模式 | 适用场景 | 最大音频长度 | 视频要求 | 特殊功能 |
|------|----------|--------------|----------|----------|
| **Lite模式**<br>(lite) | 单人正面视频 | 240秒 | 360p-1080p，mp4/mov格式 | 视频循环、倒放循环、开始时间设置 |
| **Basic模式**<br>(basic) | 单人复杂场景 | 150秒 | 360p-1080p，mp4/mov格式 | 人声分离、场景切分、说话人识别 |

## 场景对比

### 真人图片
- **五官清晰正面的单人人像**：灵动模式 > 普通模式
- **多人照片**：普通模式支持识别任意一人，灵动模式最多支持双人

### 宠物图片
- **五官清晰完整的正脸宠物**：灵动模式 > 普通模式
- **非正面或遮挡**：灵动模式表现更好
- **多宠物照片**：普通模式支持识别任意一个

### 动漫图片
- **偏真人五官**：灵动模式 > 普通模式
- **漫画鼻/漫画嘴**：普通模式驱动微弱，灵动模式可以驱动

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

## 使用方法

### 查看帮助

```bash
python volcengine_ai.py -h
```

### 单图音频驱动一键生成（推荐）

```bash
# 普通模式
python volcengine_ai.py va create "图片URL" "音频URL" --mode normal

# 灵动模式
python volcengine_ai.py va create "图片URL" "音频URL" --mode loopy

# 大画幅模式
python volcengine_ai.py va create "图片URL" "音频URL" --mode loopyb
```

### 分步操作

#### 1. 创建形象
```bash
python volcengine_ai.py va create-avatar "图片URL" --mode normal
```

#### 2. 查询形象状态
```bash
python volcengine_ai.py va query-avatar "任务ID" --mode normal
```

#### 3. 生成视频
```bash
python volcengine_ai.py va create-video "形象ID" "音频URL" --mode normal
```

#### 4. 查询视频状态
```bash
python volcengine_ai.py va query-video "任务ID" --mode normal
```

#### 5. 下载视频
```bash
python volcengine_ai.py va query-video "任务ID" --mode normal --download --filename "视频名称.mp4"
```

### 形象管理

#### 查看保存的形象
```bash
python volcengine_ai.py va avatars
```

#### 使用最新形象生成视频
```bash
python volcengine_ai.py va create-video "形象ID" "音频URL" --mode normal
```

## 视频改口型

### 生成视频改口型

#### Lite模式（推荐，适用于正面视频）
```bash
# 基础用法
python volcengine_ai.py vl create "视频URL" "音频URL" --mode lite

# 开启视频循环（音频长于视频时）
python volcengine_ai.py vl create "视频URL" "音频URL" --mode lite --align-audio

# 设置视频开始时间（从第5秒开始）
python volcengine_ai.py vl create "视频URL" "音频URL" --mode lite --templ-start-seconds 5

# 开启倒放循环（解决循环跳变问题）
python volcengine_ai.py vl create "视频URL" "音频URL" --mode lite --align-audio --align-audio-reverse
```

#### Basic模式（适用于复杂场景）
```bash
# 基础用法
python volcengine_ai.py vl create "视频URL" "音频URL" --mode basic

# 开启人声分离（抑制背景杂音）
python volcengine_ai.py vl create "视频URL" "音频URL" --mode basic --separate-vocal

# 开启场景切分与说话人识别
python volcengine_ai.py vl create "视频URL" "音频URL" --mode basic --open-scenedet

# 组合使用
python volcengine_ai.py vl create "视频URL" "音频URL" --mode basic --separate-vocal --open-scenedet
```

### 查询视频改口型状态
```bash
# 查询状态
python volcengine_ai.py vl query "任务ID" --mode lite

# 查询状态并下载
python volcengine_ai.py vl query "任务ID" --mode lite --download

# 下载并指定文件名
python volcengine_ai.py vl query "任务ID" --mode lite --download --filename "我的改口型视频.mp4"
```

## 创意特效视频生成

### 列出所有特效模板
```bash
python volcengine_ai.py ve templates
```

### 生成特效视频

#### V1版本模板（20个模板）
```bash
# 卡通变身
python volcengine_ai.py ve create "图片URL" becoming_doll

# 召唤坐骑
python volcengine_ai.py ve create "图片URL" all_things_ridability_pig

# 万物生花
python volcengine_ai.py ve create "图片URL" all_things_bloom_with_flowers

# AI环绕（美女/帅哥）
python volcengine_ai.py ve create "图片URL" beauty_surround_720p

# 天赐宝宝
python volcengine_ai.py ve create "图片URL" ai_baby_720p

# 双图模板 - 爱的拥抱
python volcengine_ai.py ve create "图片1.jpg|图片2.jpg" double_embrace
```

#### V2版本模板（29个模板）
```bash
# emoji小人变身
python volcengine_ai.py ve create "图片URL" multi_style_stacking_dolls

# 梦幻娃娃变身
python volcengine_ai.py ve create "图片URL" fluffy_dream_doll_s2e_720p

# 我的世界风
python volcengine_ai.py ve create "图片URL" my_world_720p

# 装进水晶球
python volcengine_ai.py ve create "图片URL" crystal_ball_720p

# 天使手办变身
python volcengine_ai.py ve create "图片URL" angel_figure_720p

# 毛毡钥匙扣变身
python volcengine_ai.py ve create "图片URL" felt_keychain_720p

# 拍立得风
python volcengine_ai.py ve create "图片URL" polaroid_720p

# 潮玩手办变身
python volcengine_ai.py ve create "图片URL" blister_pack_action_figure_720p

# 双图模板 - 法式热吻
python volcengine_ai.py ve create "图片1.jpg|图片2.jpg" french_kiss_dual_version_720p

# 变装比基尼
python volcengine_ai.py ve create "图片URL" costume_bikini_720p

# 热舞
python volcengine_ai.py ve create "图片URL" hot_dance_720p

# 变身美人鱼
python volcengine_ai.py ve create "图片URL" transform_into_mermaid_720p
```

### 查询特效视频状态
```bash
python volcengine_ai.py ve query "任务ID"
```

### 下载特效视频
```bash
# 使用默认文件名下载
python volcengine_ai.py ve query "任务ID" --download

# 指定文件名下载
python volcengine_ai.py ve query "任务ID" --download --filename "我的特效视频.mp4"
```

## 特效视频模板分类

### V1版本接口（20个模板）
- **🎭 卡通变身**: 变身玩偶系列（2个模板）
- **🐉 召唤坐骑**: 猪、老虎、龙系列（6个模板）
- **🌸 万物生花**: 花朵特效（2个模板）
- **💕 情感互动**: 爱的拥抱系列（4个模板，含单图/双图）
- **😊 AI环绕**: 美女/帅哥环绕（4个模板）
- **👶 天赐宝宝**: 宝宝特效（2个模板）

### V2版本接口（29个模板）
- **🎭 卡通变身**: emoji小人、梦幻娃娃、我的世界风等（13个模板）
- **💫 特效场景**: 水晶球、猫星人守护、拍立得风等（6个模板）
- **💕 情感互动**: 法式热吻系列（4个模板，含单图/双图）
- **👗 变装换装**: 比基尼、美人鱼变身（4个模板）
- **💃 动感舞蹈**: 热舞系列（2个模板）

### 特效视频特点
- **自动版本识别**: 根据模板ID自动选择V1或V2接口
- **双图模板支持**: 部分模板支持两张图片输入，用`|`分隔
- **高清版本**: 大部分模板提供480p和720p两种分辨率
- **分屏设置**: V2版本部分模板支持分屏功能（除emoji小人变身）

## 输出规格

### 大画幅模式输出尺寸
根据裁剪后图片比例自动调整：
- 4:3 → 768×576
- 3:4 → 576×768
- 16:9 → 896×504
- 9:16 → 504×896

## 服务计费

- **形象创建费用**：0.1元/形象（创建失败不收费）
- **视频生成费用**：0.3元/秒（生成失败不收费）

## 注意事项

### 单图音频驱动视频要求

#### 图片要求
- 传入完整、清晰的单人正脸图片
- 避免侧脸、遮挡、过曝、多人等情况
- 大画幅模式必须为指定比例的半身图片

#### 音频要求
- 普通模式：最长180秒
- 灵动模式：真人180秒，宠物90秒
- 大画幅模式：最长45秒

### 视频改口型要求

#### 视频要求
- 有效视频长度：3秒~350秒
- 分辨率：360p~1080p（超过1080p会自动压缩，小于360p不处理）
- 格式：支持mov、mp4、hdr（其他格式会转码）
- 编码：支持h264（其他编码会转码）
- 大小：不超过500M
- 码率：1Mbps-30Mbps
- 帧率：24~60fps
- 人脸角度：45度为极限，建议左右偏角不超过30度、上下仰角不超过15度、歪头不超过20度

#### 音频要求
- Lite模式：最长240秒，最短1秒
- Basic模式：最长150秒，最短1秒
- 格式：建议使用mp3等常见音频格式

### 创意特效视频要求

#### 图片要求
- 图片格式：JPG(JPEG), PNG等常见格式，建议使用JPG格式
- 文件大小：建议小于5MB
- 分辨率：建议大于1000*1000，小于4096*4096
- 宽高比例：推荐9:16~16:9（极端比例效果欠佳）

#### 双图模板要求
- V1版本双图模板：`double_embrace`、`double_embrace_720p`
- V2版本双图模板：`french_kiss_dual_version`、`french_kiss_dual_version_720p`
- 使用格式：用`|`分隔两个图片URL，例如：`"图片1.jpg|图片2.jpg"`

#### 分屏设置
- 仅V2版本支持分屏设置
- emoji小人变身_480p模板不支持分屏功能
- 使用`--final-stitch-switch false`开启分屏，`true`关闭分屏

### 通用输出限制
- 视频链接有效期：1小时
- 任务结果有效期：12小时

## 错误处理

客户端内置完整的错误处理机制：
- 网络超时自动重试（最多3次）
- HTTP状态码错误识别
- API错误码处理
- 参数验证
- 模式强制验证

## 文件结构

```
VolcEngineAI/
├── volcengine_ai.py              # 主入口文件
├── src/                          # 源代码目录
│   ├── config.py                 # 配置管理
│   ├── utils.py                  # 工具函数
│   ├── core/                     # 核心模块
│   │   ├── video_audio_driven_client.py  # 单图音频驱动视频客户端
│   │   ├── video_lip_sync_client.py      # 视频改口型客户端
│   │   └── video_effect_client.py        # 创意特效视频客户端
│   └── modules/                  # 功能模块
│       └── avatar_manager.py     # 形象管理
├── data/                         # 数据目录
│   └── avatars.json              # 保存的形象数据
├── requirements.txt              # 依赖列表
├── .gitignore                    # Git忽略规则
└── README.md                     # 说明文档
```

## 功能特性

### 单图音频驱动视频生成
- **三种驱动模式**: 普通模式、灵动模式、大画幅灵动模式
- **智能识别**: 支持真人、动漫、宠物等多种图片类型
- **形象管理**: 本地保存和管理创建的数字形象
- **自动重试**: 内置网络超时重试机制
- **状态监控**: 实时查询任务处理状态

### 视频改口型
- **双模式支持**: Lite模式（正面视频）和Basic模式（复杂场景）
- **智能处理**: 保留说话人形象特点，精准修改口型
- **高级功能**: 人声分离、场景切分、视频循环、倒放循环等
- **自动重试**: 内置网络超时重试机制
- **格式兼容**: 支持多种视频格式自动转码

### 创意特效视频生成
- **双版本支持**: 自动识别V1和V2接口，支持49种特效模板
- **模板分类**: 卡通变身、召唤坐骑、情感互动、变装换装、动感舞蹈等
- **双图模板**: 支持两张图片输入的特殊互动效果
- **高清输出**: 支持480p和720p两种分辨率
- **分屏设置**: V2版本支持分屏功能控制
- **自动下载**: 支持生成完成后自动下载视频到本地

### 通用特性
- **环境变量配置**: 安全的API密钥管理
- **完整错误处理**: 详细的错误信息和处理建议
- **参数验证**: 严格的输入参数校验
- **命令行友好**: 直观的CLI界面和帮助信息

## 许可证

本项目仅供学习和研究使用，请遵守火山引擎API的使用条款。