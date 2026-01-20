import time
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from agent.tools import tools
from core.config import settings
from agent.asr import audio_to_text

start_time = time.time()

llm = ChatOpenAI(
    model=settings.LLM_MODEL_NAME,
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_BASE_URL,
    temperature=settings.LLM_TEMPERATURE,
    max_tokens=settings.LLM_MAX_TOKENS,
    streaming=settings.LLM_STREAMING
)

file_path = r"D:\ChatAI\audio.wav"
# user_content = audio_to_text(file_path)
user_content = "我想要了解最新的事件"

messages = [
    HumanMessage(content=user_content)
]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
    你是一个善解人意的AI语音对话助手，根据用户的问题温馨解答用户问题，适当加入一些暖心的表情。
"""
)

response = agent.stream({"messages":messages})

for chunk in response:
    print(chunk.values(),flush=True)

end_time = time.time()
print(f"花费时间{end_time-start_time}")