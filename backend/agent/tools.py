import os
import requests
from langchain_core.tools import Tool
from langchain_tavily import TavilySearch
from core.config import settings

def tavily_search(query):
    os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
    search = TavilySearch(
        max_results=2,
        country="China"
    )
    result = search.invoke(query)
    return result

def get_weather(*args, **kwargs):
    ipinfo_url = "https://ipinfo.io/json"
    response = requests.get(ipinfo_url)
    latitude,longitude = response.json()['loc'].split(',')
    open_meteo_url = f"https://api.open-meteo.com/v1/forecast"
    params  = {
        "latitude":latitude,
        "longitude":longitude,
        "current_weather":"true"
    }
    response = requests.get(open_meteo_url,params=params)
    return response.json()

tools = [
    Tool(
        name="get_weather",
        func=get_weather,
        description="获取当前所在位置的实时天气，无需用户提供城市名称，调用后自动通过IP定位返回天气信息（包括气温、天气状况、风速等），适用于用户问“今天天气怎么样”“今天情况如何”等相关问题"
    ),
    Tool(
        name="web_search",
        func=web_search,
        description="联网搜索工具，用于获取实时/最新资讯、动态数据、未知常识、跨领域复杂问题答案（如2026年行业趋势、热点事件、股价汇率、学术资讯等）。使用时需提取用户问题核心关键词作为唯一参数，仅当问题无法通过现有知识或其他工具解答时调用"
    )
]