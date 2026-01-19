# LangChain 集成指南

## 为什么使用 LangChain？

LangChain 是一个强大的 LLM 应用开发框架，提供了：

1. **统一接口**: 支持多种 LLM 提供商（OpenAI、Anthropic、Google 等）
2. **记忆管理**: 内置对话历史管理
3. **链式调用**: 灵活组合多个组件
4. **流式输出**: 原生支持流式生成
5. **工具集成**: 轻松集成外部工具和 API
6. **RAG 支持**: 内置向量数据库和检索增强生成
7. **监控调试**: LangSmith 提供完整的可观测性

## 项目结构

```
backend/
├── agent/
│   ├── chains/              # LangChain 链定义
│   │   ├── conversation_chain.py  # 对话链
│   │   └── rag_chain.py          # RAG 链（待开发）
│   ├── memory/              # 记忆管理
│   │   └── conversation_memory.py # 对话记忆
│   ├── prompts/             # 提示词模板
│   │   └── system_prompts.py     # 系统提示词
│   ├── tools/               # LangChain 工具（待开发）
│   └── llm/                 # LLM 实现
│       ├── base.py          # 基类
│       └── langchain_llm.py # LangChain 实现
└── examples/
    └── langchain_example.py # 使用示例
```

## 核心组件

### 1. ConversationChain (对话链)

对话链是核心组件，负责管理完整的对话流程。

**特点：**
- 自动管理对话历史
- 支持流式和非流式输出
- 可自定义系统提示词
- 内置时间上下文

**使用示例：**
```python
from agent.chains.conversation_chain import ConversationChain

# 初始化
chain = ConversationChain(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    streaming=True
)

# 生成回复
response = await chain.generate("你好")

# 流式生成
async for chunk in chain.generate_stream("讲个故事"):
    print(chunk, end="")
```

### 2. ConversationMemory (对话记忆)

管理对话历史，自动限制消息数量。

**特点：**
- 基于 LangChain 的 BaseChatMessageHistory
- 自动管理消息数量
- 支持多种消息类型（Human、AI、System）
- 可序列化为字典

**使用示例：**
```python
from agent.memory.conversation_memory import ConversationMemory

# 初始化
memory = ConversationMemory(max_messages=20)

# 添加消息
memory.add_message("human", "你好")
memory.add_message("ai", "你好！有什么可以帮你的吗？")

# 获取历史
messages = memory.get_messages()

# 清空
memory.clear()
```

### 3. LangChainLLM (LLM 实现)

基于 LangChain 的 LLM 封装，支持多种模型。

**特点：**
- 统一的接口
- 支持流式输出
- 自动处理上下文
- 可配置参数

**使用示例：**
```python
from agent.llm.langchain_llm import LangChainLLM

# 初始化
llm = LangChainLLM(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    streaming=True
)
await llm.initialize()

# 生成
response = await llm.generate("你好")

# 流式生成
async for chunk in llm.generate_stream("讲个笑话"):
    print(chunk, end="")
```

### 4. 提示词模板

预定义的系统提示词，适用于不同场景。

**可用模板：**
- `VOICE_ASSISTANT_PROMPT`: 语音助手（简洁、口语化）
- `CASUAL_CHAT_PROMPT`: 休闲聊天（轻松、幽默）
- `PROFESSIONAL_ASSISTANT_PROMPT`: 专业助手（正式、高效）

**使用示例：**
```python
from agent.prompts import VOICE_ASSISTANT_PROMPT

# 在链中使用
prompt = ChatPromptTemplate.from_messages([
    ("system", VOICE_ASSISTANT_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
```

## 实时语音通话流程

```
用户说话
  ↓
ASR (Whisper) → 转录文本
  ↓
ConversationChain
  ├─ ConversationMemory (获取历史)
  ├─ Prompt Template (构建提示)
  ├─ LangChainLLM (生成回复)
  └─ ConversationMemory (保存历史)
  ↓
流式文本输出
  ↓
TTS (Edge-TTS) → 合成语音
  ↓
播放给用户
```

## 高级功能

### 1. RAG (检索增强生成)

```python
# 待实现
from agent.chains.rag_chain import RAGChain

chain = RAGChain(
    vector_store="chroma",
    embeddings="openai"
)

# 添加文档
await chain.add_documents(documents)

# 检索并生成
response = await chain.generate("查询问题")
```

### 2. 工具调用

```python
# 待实现
from agent.tools import WeatherTool, SearchTool

tools = [WeatherTool(), SearchTool()]

chain = ConversationChain(tools=tools)
response = await chain.generate("今天天气怎么样？")
```

### 3. 多模态支持

```python
# 待实现
from agent.chains.multimodal_chain import MultimodalChain

chain = MultimodalChain()

# 处理图像 + 文本
response = await chain.generate(
    text="这是什么？",
    image=image_data
)
```

## 配置说明

### 环境变量

```env
# OpenAI
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-3.5-turbo

# LangSmith (可选，用于监控)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-xxx
LANGCHAIN_PROJECT=chatai

# 其他 LLM 提供商
# ANTHROPIC_API_KEY=xxx
# GOOGLE_API_KEY=xxx
```

### 模型选择

**OpenAI 模型：**
- `gpt-3.5-turbo`: 快速、便宜，适合日常对话
- `gpt-4-turbo-preview`: 更强大，适合复杂任务
- `gpt-4`: 最强大，但较慢较贵

**其他提供商：**
- Anthropic Claude: 长上下文，安全性好
- Google Gemini: 多模态支持
- 本地模型: Llama、Mistral 等

## 性能优化

### 1. 流式输出

```python
# 使用流式输出降低首字延迟
chain = ConversationChain(streaming=True)

async for chunk in chain.generate_stream(user_input):
    # 立即发送给 TTS
    await tts.synthesize_stream(chunk)
```

### 2. 缓存

```python
# LangChain 内置缓存
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

set_llm_cache(InMemoryCache())
```

### 3. 批处理

```python
# 批量处理多个请求
responses = await llm.batch([
    "问题1",
    "问题2",
    "问题3"
])
```

## 监控与调试

### LangSmith

LangSmith 是 LangChain 官方的监控平台。

**功能：**
- 追踪每次调用
- 查看中间步骤
- 性能分析
- 错误调试

**启用方法：**
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "chatai"
```

### 日志

```python
from loguru import logger

# 在链中添加日志
logger.info(f"用户输入: {user_input}")
logger.info(f"生成回复: {response}")
logger.debug(f"历史消息数: {len(memory)}")
```

## 测试

### 单元测试

```python
import pytest
from agent.chains.conversation_chain import ConversationChain

@pytest.mark.asyncio
async def test_conversation_chain():
    chain = ConversationChain()
    response = await chain.generate("你好")
    assert len(response) > 0
```

### 集成测试

```python
@pytest.mark.asyncio
async def test_full_pipeline():
    # ASR
    transcript = await asr.transcribe(audio_data)
    
    # LLM
    chain = ConversationChain()
    response = await chain.generate(transcript)
    
    # TTS
    audio = await tts.synthesize(response)
    
    assert audio is not None
```

## 最佳实践

1. **使用流式输出**: 降低延迟，提升体验
2. **限制历史长度**: 避免上下文过长
3. **错误处理**: 捕获异常，提供降级方案
4. **监控性能**: 使用 LangSmith 追踪
5. **提示词优化**: 针对语音场景优化提示词
6. **缓存常见回复**: 提高响应速度

## 参考资源

- [LangChain 官方文档](https://python.langchain.com/)
- [LangSmith 文档](https://docs.smith.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [示例代码](./examples/langchain_example.py)

## 常见问题

### Q: 如何切换到其他 LLM 提供商？

A: 只需更换 LLM 类：
```python
# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Anthropic
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-opus")

# Google
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro")
```

### Q: 如何实现打断功能？

A: 在检测到新的用户输入时，取消当前的生成任务：
```python
import asyncio

task = asyncio.create_task(chain.generate_stream(input))

# 检测到打断
if user_interrupted:
    task.cancel()
```

### Q: 如何优化延迟？

A: 
1. 使用流式输出
2. 选择更快的模型（如 gpt-3.5-turbo）
3. 减少上下文长度
4. 使用缓存
5. 并行处理（ASR、LLM、TTS 流水线）

## 下一步

1. 实现 RAG 链（知识库检索）
2. 添加工具调用（天气、搜索等）
3. 实现多模态支持（图像理解）
4. 优化提示词
5. 添加更多测试
