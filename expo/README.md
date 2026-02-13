# ChatAI Expo 前端

## 项目架构

```
expo/
├── src/
│   ├── api/              # API调用层
│   │   └── chatApi.ts    # 聊天API接口
│   ├── config/           # 配置文件
│   │   └── api.ts        # API配置
│   ├── hooks/            # 自定义Hooks
│   │   └── useChat.ts    # 聊天Hook
│   └── screens/          # 页面组件
│       └── VoiceChatScreen.tsx  # 语音聊天主页面
├── App.tsx               # 应用入口
├── index.js              # 注册入口
└── package.json
```

## 架构说明

### 1. API层 (`src/api/`)
- 封装所有后端API调用
- 统一错误处理
- 类型定义

### 2. 配置层 (`src/config/`)
- API地址配置
- 环境变量管理

### 3. Hooks层 (`src/hooks/`)
- 封装业务逻辑
- 状态管理
- 可复用的逻辑

### 4. 页面层 (`src/screens/`)
- UI组件
- 页面布局
- 用户交互

## 优势

1. **关注点分离** - API、业务逻辑、UI分离
2. **易于测试** - 每层可独立测试
3. **可维护性** - 代码结构清晰
4. **可扩展性** - 易于添加新功能
5. **类型安全** - TypeScript类型定义

## 使用示例

### 调用API
```typescript
import { chatApi } from './src/api/chatApi';

const response = await chatApi.sendMessage({
  message: '你好',
  session_id: 'user_123'
});
```

### 使用Hook
```typescript
import { useChat } from './src/hooks/useChat';

const { sendMessage, clearHistory, isLoading } = useChat();

await sendMessage('你好');
await clearHistory();
```

## 启动项目

```bash
npm start
```
