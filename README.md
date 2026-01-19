# ChatAI - 实时通话应用

一个前后端分离的实时通话应用，支持语音识别、LLM 对话和语音合成功能。

## 项目结构

```
ChatAI/
├── backend/          # 后端服务
│   └── agent/       # AI 代理模块
├── expo/            # 前端移动应用（React Native + Expo）
├── docs/            # 项目文档
└── README.md        # 项目说明文档
```

## 技术架构

### 前端（expo/）
- **框架**: React Native + Expo SDK 54
- **语言**: TypeScript
- **主要功能**:
  - 实时语音录音（麦克风控制）
  - 摄像头全屏共享
  - 实时性能监控（ASR、TTFT、TTS 延迟）
  - 渐变背景 UI

### 后端（backend/）
- **框架**: FastAPI + LangChain
- **语言**: Python 3.11+
- **核心技术**:
  - **LangChain**: LLM 应用开发框架
  - **ASR**: Whisper (语音识别)
  - **LLM**: OpenAI GPT / Claude / Gemini (支持多种模型)
  - **TTS**: Edge-TTS (语音合成)
  - **VAD**: Silero VAD (语音活动检测)
  - **WebSocket**: 实时双向通信
- **主要功能**:
  - 流式语音识别
  - 对话历史管理
  - 流式文本生成
  - 流式语音合成
  - 上下文管理

## 快速开始

### 前端启动

1. 进入前端目录
```bash
cd expo
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm start
```

4. 使用 Expo Go 扫描二维码或按快捷键：
   - `a` - Android 模拟器
   - `i` - iOS 模拟器
   - `w` - Web 浏览器

详细说明请查看 [expo/README.md](./expo/README.md)

### 后端启动

1. 进入后端目录
```bash
cd backend
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入 OpenAI API Key 等配置
```

5. 启动服务
```bash
python main.py
```

服务将在 `http://localhost:8000` 启动

详细说明请查看：
- [backend/README.md](./backend/README.md) - 后端项目说明
- [backend/LANGCHAIN_GUIDE.md](./backend/LANGCHAIN_GUIDE.md) - LangChain 使用指南
- [backend/ARCHITECTURE.md](./backend/ARCHITECTURE.md) - 架构设计文档

## 功能特性

### ✅ 已实现
- 🎙️ 麦克风控制（默认开启，可切换静音）
- 📹 摄像头全屏共享（支持前后摄像头切换）
- 🎨 渐变背景 UI
- 📊 实时性能监控
- 🔄 状态管理

### 🚧 开发中
- 🎤 真实语音识别（ASR）
- 🤖 LLM 对话集成
- 🔊 语音合成（TTS）
- 📱 屏幕共享功能
- 🌐 WebSocket 实时通信

## 开发环境

### 前端要求
- Node.js 14+
- npm 或 yarn
- Expo Go（手机测试）
- Android Studio / Xcode（模拟器测试）

### 后端要求
- Python 3.8+（待定）
- 其他依赖待补充

## 项目文档

- [前端开发文档](./expo/README.md)
- [设计规范](./docs/豆包式实时通话手机App：页面与交互设计规范.pdf)

## 开发计划

### Phase 1: 前端基础 ✅
- [x] 项目初始化
- [x] UI 界面实现
- [x] 摄像头功能
- [x] 基础交互

### Phase 2: 后端服务 🚧
- [ ] 搭建后端框架
- [ ] 实现 ASR 服务
- [ ] 集成 LLM
- [ ] 实现 TTS 服务

### Phase 3: 前后端联调 📋
- [ ] WebSocket 通信
- [ ] 实时数据流
- [ ] 性能优化
- [ ] 错误处理

### Phase 4: 功能完善 📋
- [ ] 屏幕共享
- [ ] 设置页面
- [ ] 用户认证
- [ ] 数据持久化

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue。
