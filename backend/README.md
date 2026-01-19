# ChatAI Backend - 实时语音通话后端服务

基于 Python 的实时语音通话后端服务，支持 ASR、LLM、TTS 和实时通信。

## 项目结构

```
backend/
├── agent/                  # 核心 AI 代理模块
│   ├── asr/               # 语音识别模块
│   ├── llm/               # 大语言模型模块
│   ├── tts/               # 语音合成模块
│   ├── vad/               # 语音活动检测模块
│   └── websocket/         # WebSocket 通信模块
├── api/                   # API 路由层
│   ├── routes/            # 路由定义
│   └── middleware/        # 中间件
├── core/                  # 核心功能
│   ├── config/            # 配置管理
│   ├── audio/             # 音频处理
│   ├── stream/            # 流式处理
│   └── context/           # 上下文管理
├── models/                # 数据模型
├── services/              # 业务服务层
├── utils/                 # 工具函数
├── tests/                 # 测试文件
├── logs/                  # 日志文件
├── requirements.txt       # Python 依赖
├── main.py               # 应用入口
├── config.yaml           # 配置文件
└── README.md             # 项目文档
```

## 技术栈

- **框架**: FastAPI / Flask
- **WebSocket**: python-socketio / websockets
- **ASR**: Whisper / FunASR
- **LLM**: OpenAI API / 本地模型
- **TTS**: Edge-TTS / Coqui TTS
- **音频处理**: librosa / pydub
- **VAD**: Silero VAD / WebRTC VAD

## 快速开始

### 1. 创建虚拟环境
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的 API Keys
```

### 4. 启动服务
```bash
python main.py
```

服务将在 `http://localhost:8000` 启动

## API 文档

启动服务后访问：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 模块说明

### ASR (语音识别)
- 支持流式识别
- 多语言支持
- 实时转录

### LLM (大语言模型)
- 流式生成
- 上下文管理
- 多轮对话

### TTS (语音合成)
- 流式合成
- 多音色支持
- 情感控制

### VAD (语音活动检测)
- 实时检测
- 低延迟
- 高准确率

### WebSocket
- 双向通信
- 音频流传输
- 状态同步

## 开发计划

- [ ] 搭建基础框架
- [ ] 实现 WebSocket 服务
- [ ] 集成 ASR 模块
- [ ] 集成 LLM 模块
- [ ] 集成 TTS 模块
- [ ] 实现 VAD 检测
- [ ] 添加音频处理
- [ ] 实现流式处理
- [ ] 添加打断机制
- [ ] 性能优化
- [ ] 单元测试
- [ ] 部署文档

## 环境变量

```env
# 服务配置
HOST=0.0.0.0
PORT=8000
DEBUG=True

# OpenAI (如果使用)
OPENAI_API_KEY=your_api_key_here

# 其他 API Keys
# ...
```

## 许可证

MIT License
