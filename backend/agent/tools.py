import requests
from langchain_core.tools import Tool,StructuredTool

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
    )
]