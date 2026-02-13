import os
import requests
from typing import List, Tuple, Dict
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.tools import tool
from langchain_tavily import TavilySearch
from config import settings


class ChatService:
    
    def __init__(self):
        print("正在初始化ChatService...")
        
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL_NAME,
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            streaming=settings.LLM_STREAMING
        )
        print("✓ LLM初始化完成")
        
        self.sessions: Dict[str, ChatMessageHistory] = {}
        self.tools = self._init_tools()
        print("✓ Tools初始化完成")
        
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt="你是一个善解人意的AI语音对话助手，根据用户的问题温馨解答用户问题，适当加入一些暖心的表情。"
        )
        print("✓ Agent初始化完成")
        print("ChatService初始化完成！")
    
    def _init_tools(self):
        @tool(
            "tavily_search",
            description="""
            联网搜索工具，用于获取实时/最新资讯、动态数据、未知常识、跨领域复杂问题答案（如2026年行业趋势、热点事件、股价汇率、学术资讯等）。
            
            特别说明：
            当用户的问题涉及 **健康、营养、饮食、食品安全、疾病饮食建议、营养摄入标准、最新膳食指南** 等内容时，**必须优先调用此工具**，以获取权威、最新的健康相关信息。
            
            使用时需提取用户问题核心关键词作为唯一参数，仅当问题无法通过现有知识或其他工具解答时调用。
            """
        )
        def tavily_search(query: str) -> str:
            os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
            search = TavilySearch(max_results=5, country="China")
            result = search.invoke(query)
            return result

        @tool(
            "get_weather",
            description="""
            获取当前所在位置的实时天气，无需用户提供城市名称，调用后自动通过IP定位返回天气信息（包括气温、天气状况、风速等），适用于用户问"今天天气怎么样""今天情况如何"等相关问题
            """
        )
        def get_weather(*args, **kwargs) -> dict:
            ipinfo_url = "https://ipinfo.io/json"
            response = requests.get(ipinfo_url)
            latitude, longitude = response.json()['loc'].split(',')
            open_meteo_url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true"
            }
            response = requests.get(open_meteo_url, params=params)
            return response.json()

        return [get_weather, tavily_search]
    
    def audio_to_text(self, file_path: str) -> str:
        headers = {"Authorization": f"Bearer {settings.ASR_API_KEY}"}
        with open(file_path, "rb") as audio_file:
            files = {
                "file": ("audio.wav", audio_file, "audio/wav"),
                "model": (None, settings.ASR_MODEL_NAME)
            }
            response = requests.post(settings.ASR_BASE_URL, headers=headers, files=files)

        if response.status_code == 200:
            result = response.json()['text']
            print(f"ASR结果: {result}")
            return result
        else:
            print(f"ASR失败: {response.status_code}")
            return ""
    
    def text_to_speech(self, text: str, output_path: str = "output.wav") -> str:
        print(f"TTS: {text}")
        return output_path
    
    def detect_speech(self, audio_chunk: bytes) -> bool:
        return True
    
    def get_or_create_memory(self, session_id: str = "default") -> ChatMessageHistory:
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatMessageHistory()
        return self.sessions[session_id]
    
    def clear_memory(self, session_id: str = "default"):
        if session_id in self.sessions:
            self.sessions[session_id].clear()
    
    async def chat(self, message: str, history: List[dict] = None, session_id: str = "default") -> Tuple[str, List[dict]]:
        memory = self.get_or_create_memory(session_id)
        messages = []
        
        if history:
            for msg in history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        else:
            messages.extend(memory.messages)
        
        messages.append(HumanMessage(content=message))
        
        response = self.agent.invoke({"messages": messages})
        
        ai_response = ""
        if "messages" in response:
            last_message = response["messages"][-1]
            ai_response = last_message.content
        
        memory.add_user_message(message)
        memory.add_ai_message(ai_response)
        
        if history:
            updated_history = history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": ai_response}
            ]
        else:
            updated_history = []
            for msg in memory.messages:
                if isinstance(msg, HumanMessage):
                    updated_history.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    updated_history.append({"role": "assistant", "content": msg.content})
        
        return ai_response, updated_history
    
    async def chat_stream(self, message: str, history: List[dict] = None, session_id: str = "default"):
        memory = self.get_or_create_memory(session_id)
        messages = []
        
        if history:
            for msg in history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        else:
            messages.extend(memory.messages)
        
        messages.append(HumanMessage(content=message))
        
        response_stream = self.agent.stream({"messages": messages})
        
        full_response = ""
        for chunk in response_stream:
            if "messages" in chunk:
                content = chunk["messages"][-1].content
                full_response += content
                yield content
        
        memory.add_user_message(message)
        memory.add_ai_message(full_response)
    
    async def voice_chat(self, audio_path: str, session_id: str = "default") -> Tuple[str, str]:
        user_text = self.audio_to_text(audio_path)
        
        if not user_text:
            return "抱歉，我没有听清楚", ""
        
        ai_response, _ = await self.chat(user_text, session_id=session_id)
        audio_output = self.text_to_speech(ai_response)
        
        return ai_response, audio_output
