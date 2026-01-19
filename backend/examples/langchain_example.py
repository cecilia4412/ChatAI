"""
LangChain 使用示例
演示如何使用 LangChain 构建对话系统
"""

import asyncio
from loguru import logger

# 设置环境变量（实际使用时应该从 .env 读取）
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

from agent.chains.conversation_chain import ConversationChain
from agent.llm.langchain_llm import LangChainLLM


async def example_basic_llm():
    """示例1: 基础 LLM 使用"""
    logger.info("=== 示例1: 基础 LLM 使用 ===")
    
    # 初始化 LLM
    llm = LangChainLLM(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=False
    )
    await llm.initialize()
    
    # 生成回复
    response = await llm.generate("你好，请介绍一下自己")
    logger.info(f"回复: {response}")


async def example_streaming_llm():
    """示例2: 流式 LLM"""
    logger.info("=== 示例2: 流式 LLM ===")
    
    # 初始化 LLM
    llm = LangChainLLM(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=True
    )
    await llm.initialize()
    
    # 流式生成
    print("回复: ", end="", flush=True)
    async for chunk in llm.generate_stream("讲一个简短的笑话"):
        print(chunk, end="", flush=True)
    print()


async def example_conversation_chain():
    """示例3: 对话链"""
    logger.info("=== 示例3: 对话链 ===")
    
    # 初始化对话链
    chain = ConversationChain(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=False
    )
    
    # 多轮对话
    questions = [
        "你好，我叫小明",
        "我喜欢编程",
        "你还记得我的名字吗？",
        "我喜欢什么？"
    ]
    
    for question in questions:
        logger.info(f"用户: {question}")
        response = await chain.generate(question)
        logger.info(f"AI: {response}")
        print()


async def example_streaming_conversation():
    """示例4: 流式对话链"""
    logger.info("=== 示例4: 流式对话链 ===")
    
    # 初始化对话链
    chain = ConversationChain(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        streaming=True
    )
    
    # 流式对话
    user_input = "给我讲一个关于程序员的故事"
    logger.info(f"用户: {user_input}")
    
    print("AI: ", end="", flush=True)
    async for chunk in chain.generate_stream(user_input):
        print(chunk, end="", flush=True)
    print("\n")


async def example_with_context():
    """示例5: 带上下文的对话"""
    logger.info("=== 示例5: 带上下文的对话 ===")
    
    llm = LangChainLLM(
        model_name="gpt-3.5-turbo",
        temperature=0.7
    )
    await llm.initialize()
    
    # 构建上下文
    context = [
        {"role": "human", "content": "我叫张三"},
        {"role": "ai", "content": "你好张三，很高兴认识你！"},
        {"role": "human", "content": "我是一名软件工程师"},
        {"role": "ai", "content": "太好了！软件工程是一个很有前景的领域。"}
    ]
    
    # 带上下文生成
    response = await llm.generate(
        "你还记得我的职业吗？",
        context=context
    )
    logger.info(f"回复: {response}")


async def main():
    """主函数"""
    try:
        # 运行示例
        await example_basic_llm()
        print("\n" + "="*50 + "\n")
        
        await example_streaming_llm()
        print("\n" + "="*50 + "\n")
        
        await example_conversation_chain()
        print("\n" + "="*50 + "\n")
        
        await example_streaming_conversation()
        print("\n" + "="*50 + "\n")
        
        await example_with_context()
        
    except Exception as e:
        logger.error(f"示例运行失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())
