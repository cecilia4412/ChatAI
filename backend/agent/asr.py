import requests
from core.config import settings

def audio_to_text(file_path):
    headers = {
        "Authorization": f"Bearer {settings.ASR_API_KEY}"
    }
    with open(file_path, "rb") as audio_file:
        files = {
            "file": ("audio.wav", audio_file,"audio/wav"),
            "model": (None, settings.ASR_MODEL_NAME)
        }
        response = requests.post(settings.ASR_BASE_URL, headers=headers, files=files)

    if response.status_code == 200:
        result = response.json()['text']
        print(f"asr结果:{result}")
        return result
    else:
        return ""