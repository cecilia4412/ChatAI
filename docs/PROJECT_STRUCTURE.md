# Backend 项目结构说明

## 完整目录结构

```
backend/
├── agent/                      # AI 代理模块
│   ├── asr/                   # 语音识别 (ASR)
│   │   ├── __init__.py
│   │   ├── base.py           # ASR 基类
│   │   ├── whisper_asr.py    # Whisper 实现 (待开发)
│   │   └── funasr.py         # FunASR 实现 (待开发)
│   ├── llm/                   # 大语言模型 (LLM)
│   │   ├── __init__.py
│   │   ├── base.py           # LLM 基类
│   │   ├── openai_llm.py     # OpenAI 实现 (待开发)
│   │   └── local_llm.py      # 本地模型实现 (待开发)
│   ├── tts/                   # 语音合成 (TTS)
│   │   ├── __init__.py
│   │   ├── base.py           # TTS 基类
│   │   ├── edge_tts.py       # Edge-TTS 实现 (待开发)
│   │   └── coqui_tts.py      # Coqui TTS 实现 (待开发)
│   ├── vad/                   # 语音活动检测 (VAD)
│   │   ├── __init__.py
│   │   ├── base.py           # VAD 基类
│   │   ├── silero_vad.py     # Silero VAD 实现 (待开发)
│   │   └── webrtc_vad.py     # WebRTC VAD 实现 (待开发)
│   └── websocket/             # WebSocket 处理
│       └── (待开发)
│
├── api/                       # API 路由层
│   ├── routes/               # 路由定义
│   │   ├── health.py         # 健康检查 ✅
│   │   └── websocket.py      # WebSocket 路由 ✅
│   └── middleware/           # 中间件
│       └── (待开发)
│
├── core/                      # 核心功能
│   ├── config/               # 配置管理
│   │   ├── __init__.py       # ✅
│   │   └── settings.py       # 配置类 ✅
│   ├── audio/                # 音频处理
│   │   └── (待开发)
│   ├── stream/               # 流式处理
│   │   └── (待开发)
│   └── context/              # 上下文管理
│       └── (待开发)
│
├── models/                    # 数据模型
│   └── (待开发)
│
├── services/                  # 业务服务层
│   └── (待开发)
│
├── utils/                     # 工具函数
│   ├── __init__.py           # ✅
│   └── audio_utils.py        # 音频工具 ✅
│
├── tests/                     # 测试文件
│   └── (待开发)
│
├── logs/                      # 日志文件
│   └── (自动生成)
│
├── .env.example              # 环境变量示例 ✅
├── .gitignore                # Git 忽略文件 ✅
├── requirements.txt          # Python 依赖 ✅
├── main.py                   # 应用入口 ✅
├── README.md                 # 项目说明 ✅
├── ARCHITECTURE.md           # 架构设计 ✅
└── PROJECT_STRUCTURE.md      # 本文件 ✅
```

## 已完成的文件 ✅

### 1. 配置文件
- `.env.example` - 环境变量模板
- `.gitignore` - Git 忽略规则
- `requirements.txt` - Python 依赖列表

### 2. 核心文件
- `main.py` - FastAPI 应用入口
- `core/config/settings.py` - 配置管理

### 3. API 路由
- `api/routes/health.py` - 健康检查接口
- `api/routes/websocket.py` - WebSocket 接口

### 4. 基类定义
- `agent/asr/base.py` - ASR 基类
- `agent/llm/base.py` - LLM 基类
- `agent/tts/base.py` - TTS 基类
- `agent/vad/base.py` - VAD 基类

### 5. 工具函数
- `utils/audio_utils.py` - 音频处理工具

### 6. 文档
- `README.md` - 项目说明
- `ARCHITECTURE.md` - 架构设计
- `PROJECT_STRUCTURE.md` - 项目结构

## 待开发的模块 🚧

### 优先级 P0 (核心功能)
1. **ASR 实现**
   - `agent/asr/whisper_asr.py`
   - 实现 Whisper 语音识别

2. **LLM 实现**
   - `agent/llm/openai_llm.py`
   - 实现 OpenAI API 调用

3. **TTS 实现**
   - `agent/tts/edge_tts.py`
   - 实现 Edge-TTS 语音合成

4. **VAD 实现**
   - `agent/vad/silero_vad.py`
   - 实现语音活动检测

5. **WebSocket 处理**
   - 完善 `api/routes/websocket.py`
   - 实现音频流处理逻辑

### 优先级 P1 (重要功能)
6. **音频处理**
   - `core/audio/processor.py`
   - 降噪、格式转换、重采样

7. **流式处理**
   - `core/stream/manager.py`
   - 管理音频流和文本流

8. **上下文管理**
   - `core/context/manager.py`
   - 管理对话历史和会话状态

9. **业务服务**
   - `services/conversation_service.py`
   - 协调各个 AI 模块

### 优先级 P2 (优化功能)
10. **中间件**
    - 认证、日志、错误处理

11. **数据模型**
    - Pydantic 模型定义

12. **测试**
    - 单元测试和集成测试

## 开发顺序建议

### Phase 1: 基础功能 (1-2 周)
1. 实现 ASR (Whisper)
2. 实现 LLM (OpenAI)
3. 实现 TTS (Edge-TTS)
4. 完善 WebSocket 处理
5. 基础测试

### Phase 2: 核心功能 (1-2 周)
6. 实现 VAD
7. 实现音频处理
8. 实现流式处理
9. 实现上下文管理
10. 集成测试

### Phase 3: 优化完善 (1 周)
11. 性能优化
12. 错误处理
13. 日志完善
14. 文档补充

## 快速开始开发

### 1. 环境准备
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件
```

### 3. 启动服务
```bash
python main.py
```

### 4. 测试接口
```bash
# 健康检查
curl http://localhost:8000/api/health

# API 文档
open http://localhost:8000/docs
```

## 代码规范

### 命名规范
- 文件名: `snake_case.py`
- 类名: `PascalCase`
- 函数名: `snake_case`
- 常量: `UPPER_CASE`

### 文档规范
- 所有类和函数必须有文档字符串
- 使用 Google 风格的文档字符串
- 类型注解必须完整

### 示例
```python
async def process_audio(
    audio_data: bytes,
    sample_rate: int = 16000
) -> str:
    """
    处理音频数据
    
    Args:
        audio_data: 音频字节数据
        sample_rate: 采样率，默认 16000Hz
        
    Returns:
        处理后的文本
        
    Raises:
        ValueError: 当音频数据无效时
    """
    pass
```

## 贡献指南

1. 从 `main` 分支创建功能分支
2. 遵循代码规范
3. 编写单元测试
4. 提交 Pull Request
5. Code Review 通过后合并

## 联系方式

如有问题，请提交 Issue 或联系开发团队。
