# 火山引擎单图音频驱动视频生成客户端

基于火山引擎API的单图音频驱动视频生成客户端，支持普通模式、灵动模式和大画幅灵动模式。

## 产品介绍

根据用户上传的单张图片+音频，生成该图片对应的视频效果。用户上传的单张图片可以是人像图片，也可以是宠物图片/动漫图片等。

## 驱动模式说明

| 模式 | 驱动范围 | 输出比例 | 最大音频长度 | 支持类型 | 特点 |
|------|----------|----------|--------------|----------|------|
| **普通模式**<br>(normal) | 嘴部 | 原图比例 | 180秒 | 真人、动漫、宠物 | 嘴部精准驱动，支持多人/多宠物 |
| **灵动模式**<br>(loopy) | 全脸 | 固定1:1<br>(512*512) | 180秒(真人)<br>90秒(宠物) | 真人、动漫、宠物 | 运动幅度大，表情丰富，随机性强 |
| **大画幅灵动模式**<br>(loopyb) | 全脸+膝盖以上身体 | 多种比例<br>(16:9,9:16,3:4,4:3) | 45秒 | 真人、动漫<br>(不支持宠物) | 半身驱动，身体+脸部动作 |

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

### 一键生成（推荐）

```bash
# 普通模式
python volcengine_ai.py generate-all --image-url "图片URL" --audio-url "音频URL" --mode normal

# 灵动模式
python volcengine_ai.py generate-all --image-url "图片URL" --audio-url "音频URL" --mode loopy

# 大画幅模式
python volcengine_ai.py generate-all --image-url "图片URL" --audio-url "音频URL" --mode loopyb
```

### 分步操作

#### 1. 创建形象
```bash
python volcengine_ai.py create-avatar --image-url "图片URL" --mode normal
```

#### 2. 查询形象状态
```bash
python volcengine_ai.py query-avatar --task-id "任务ID" --mode normal
```

#### 3. 生成视频
```bash
python volcengine_ai.py generate-video --resource-id "形象ID" --audio-url "音频URL" --mode normal
```

#### 4. 查询视频状态
```bash
python volcengine_ai.py query-video --task-id "任务ID" --mode normal
```

#### 5. 下载视频
```bash
python volcengine_ai.py query-video --task-id "任务ID" --mode normal --download --filename "视频名称.mp4"
```

### 形象管理

#### 查看保存的形象
```bash
python volcengine_ai.py list-avatars
```

#### 使用最新形象生成视频
```bash
python volcengine_ai.py use-latest-avatar --audio-url "音频URL" --mode normal
```

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

### 图片要求
- 传入完整、清晰的单人正脸图片
- 避免侧脸、遮挡、过曝、多人等情况
- 大画幅模式必须为指定比例的半身图片

### 音频要求
- 普通模式：最长180秒
- 灵动模式：真人180秒，宠物90秒
- 大画幅模式：最长45秒

### 输出限制
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
│   │   └── volcengine_avatar_client.py
│   └── modules/                  # 功能模块
│       └── avatar_manager.py     # 形象管理
├── data/                         # 数据目录
│   └── avatars.json              # 保存的形象数据
├── requirements.txt              # 依赖列表
├── .gitignore                    # Git忽略规则
└── README.md                     # 说明文档
```

## 许可证

本项目仅供学习和研究使用，请遵守火山引擎API的使用条款。