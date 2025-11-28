# 火山引擎AI视频生成客户端

基于火山引擎API的AI视频生成客户端，支持单图音频驱动视频生成、视频改口型、创意特效视频生成、即梦AI数字人生成、即梦AI动作模仿、单图视频驱动和图片换装。

## 产品介绍

### 1. 单图音频驱动视频生成
根据用户上传的单张图片+音频，生成该图片对应的视频效果。用户上传的单张图片可以是人像图片，也可以是宠物图片/动漫图片等。

### 2. 视频改口型
输入一段单人口播视频+音频，在保留说话人形象特点的前提下，将视频中的人物口型根据指定的音频输入进行修改。支持Lite模式和Basic模式，适用于各种场景需求。

### 3. 创意特效视频生成
基于单张图片或双张图片，使用AI技术生成各种创意特效视频，支持49种不同的特效模板，涵盖卡通变身、情感互动、变装换装等多种风格。

### 4. 即梦AI数字人生成 (OmniHuman)
基于单张图片和音频，生成高质量的数字人视频。支持OmniHuman 1.0和1.5两个版本，具备主体识别、对象检测、提示词控制等高级功能。

### 5. 即梦AI动作模仿
输入单张图片和模板视频，生成模仿视频动作的视频。支持真人、动漫、宠物的动作和表情模仿。

### 6. 单图视频驱动
输入单张图片和驱动视频，生成以图片场景和人物模仿视频动作的视频。支持人脸表情和肢体动作驱动，输出高分辨率视频。

### 7. 图片换装
基于用户输入的服装图片，更换到指定的模特图上。即输入服装图 + 模特图，输出模特穿着指定服装的照片。支持复杂的模特pose和任意品类/款式的服装图输入，能够合成真实的褶皱和光影效果。

- **V1版**：同步接口，单件服装，快速响应
- **V2版**：异步接口，支持多件服装组合（上衣+下衣），丰富的推理参数

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

### 单图视频驱动规格

| 项目 | 要求说明 |
|------|----------|
| **输入图片** | 格式：jpeg/jpg/png<br>分辨率：512x512 - 4096x4096<br>需公网可访问 |
| **驱动视频** | 格式：mp4/mov/webm<br>分辨率：540-2048<br>时长：最大30秒<br>需公网可访问 |
| **输出视频** | 分辨率：960x540 或 896x672<br>格式：mp4<br>驱动范围：全脸+肢体动作 |
| **收费标准** | 0.3元/秒，并发限制1 |
| **支持场景** | 真人、正面场景、无遮挡、无快速运动 |

### 图片换装规格

| 项目 | 要求说明 |
|------|----------|
| **输入模特图** | 格式：JPG/JPEG/PNG/JFIF<br>文件大小：小于5MB<br>分辨率：小于4096*4096<br>需公网可访问，建议人物主体清晰 |
| **输入服装图** | 格式：JPG/JPEG/PNG/JFIF<br>文件大小：小于5MB<br>分辨率：小于4096*4096<br>支持平铺图、挂拍图、上身图等 |
| **输出图片** | 格式：PNG<br>含AI生成标识和隐式水印 |
| **收费标准** | 1元/次，并发限制1 |
| **支持类型** | 真人、动漫人物、CG人物<br>各种姿势和画幅 |
| **优势特点** | 支持复杂模特pose、任意品类服装、自动生成褶皱和光影 |

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

## 即梦AI数字人生成

### OmniHuman 1.0版一键生成（快速模式）
```bash
python volcengine_ai.py jm va create-avatar "图片URL" "音频URL" "一个微笑的年轻女性" --mode 1.0
```

### OmniHuman 1.5版带对象检测（高质量模式）
```bash
python volcengine_ai.py jm va create-avatar "图片URL" "音频URL" "一个穿着蓝色衬衫的男性" --mode 1.5 --subject-id 1 --enable-object-detection
```

### 即梦AI分步操作
```bash
# 主体检测
python volcengine_ai.py jm va detect "图片URL" "一个可爱的宠物" --mode 1.5

# 对象检测（1.5版专用）
python volcengine_ai.py jm va detect-object 1 12345678 --mode 1.5

# 查询结果
python volcengine_ai.py jm va query 87654321 --mode 1.5
```

## 即梦AI动作模仿

### 创建动作模仿任务
```bash
python volcengine_ai.py jm mimic create "图片URL" "视频URL"
```

### 查询动作模仿状态
```bash
python volcengine_ai.py jm mimic query "任务ID"
```

## 单图视频驱动

### 创建单图视频驱动任务
```bash
python volcengine_ai.py vv create "图片URL" "驱动视频URL"
```

### 查询单图视频驱动状态
```bash
python volcengine_ai.py vv query "任务ID"
```

### 下载并指定文件名
```bash
python volcengine_ai.py vv query "任务ID" --filename "我的驱动视频.mp4"
```

## 图片换装

### 生成图片换装

#### V1版 - 同步接口（单件服装）
```bash
# 基础用法
python volcengine_ai.py io generate "模特图片URL" "服装图片URL"

# 指定保存文件名
python volcengine_ai.py io generate "模特图片URL" "服装图片URL" --filename "我的换装图片.png"

# 不自动下载，只返回URL
python volcengine_ai.py io generate "模特图片URL" "服装图片URL" --no-download

# 自定义推理参数
python volcengine_ai.py io generate "模特图片URL" "服装图片URL" --seed 12345 --num-steps 40

# 保持模特原图的某些部位
python volcengine_ai.py io generate "模特图片URL" "服装图片URL" --keep-head --keep-hand --keep-foot
```

#### V2版 - 异步接口（支持多件服装）
```bash
# V2版单件服装
python volcengine_ai.py io generate "模特图片URL" "服装图片URL" --version 2

# V2版多件服装（上衣+下衣）
python volcengine_ai.py io generate "模特图片URL" "上衣URL|下衣URL" --version 2 --garment-types upper bottom

# V2版自定义推理参数
python volcengine_ai.py io generate "模特图片URL" "服装URL" --version 2 --num-steps 20 --tight-mask bbox

# V2版保护区域配置
python volcengine_ai.py io generate "模特图片URL" "服装URL" --version 2 --protect-mask-url "保护区域图URL"
```

### 版本对比

| 特性 | V1版 | V2版 |
|------|------|------|
| 接口类型 | 同步 | 异步 |
| 响应时间 | 快速 | 需等待任务完成 |
| 服装数量 | 单件 | 最多2件（上衣+下衣） |
| 服装类型 | 无需分类 | 支持分类（upper/bottom/full） |
| 推理参数 | 基础参数 | 丰富参数配置 |
| 保护区域 | 不支持 | 支持保护区域图 |
| 处理模式 | CVProcess | CVSubmitTask + CVGetResult |

### 图片换装参数说明

#### 基本参数
- `model_url`: 模特图片URL（必选）
- `garment_url`: 服装图片URL（必选，V2版支持多个URL用|分隔）

#### 版本控制
- `--version`: API版本选择（1: V1版同步接口, 2: V2版异步接口，默认: 1）

#### 通用可选参数
- `--filename`: 保存文件名
- `--no-download`: 不自动下载图片，只返回URL
- `--model-id`: 模特ID（V1版默认: 1）
- `--garment-id`: 服装ID（V1版默认: 1）

#### 通用推理配置
- `--seed`: 随机种子参数（-1表示随机）
- `--num-steps`: 模型推理步数
  - V1版：25-50（默认: 50）
  - V2版：8-50（默认: 16）
- `--no-sr`: 不对结果进行超分处理

#### 通用保护区域
- `--keep-head`: 保持模特原图的头（包括发型）
- `--no-keep-hand`: 不保持模特原图的手（V2版默认不保持）
- `--no-keep-foot`: 不保持模特原图的足（V2版默认不保持）
- `--keep-upper`: 保持模特原图的上装
- `--keep-lower`: 保持模特原图的下装

#### V2版专用参数
- `--garment-types`: 服装类型列表（取值: upper/bottom/full，用空格分隔）
- `--protect-mask-url`: 模特保护区域图URL（PNG格式）
- `--tight-mask`: 模特图遮挡区域范围（tight/loose/bbox，默认: loose）
- `--p-bbox-iou-ratio`: bbox与主体相交比例（范围: [0, 1.0]，默认: 0.3）
- `--p-bbox-expand-ratio`: bbox扩大比例（范围: [1.0, 1.5]，默认: 1.1）
- `--max-process-side-length`: 最大边长（范围: [1080, 4096]，默认: 1920）
- `--req-image-store-type`: 图片传入方式（0:base64, 1:URL，默认: 1）

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