import json
import requests
from src import log

logger = log.setup_logger(__name__)

def reset_chat():
    conversation_history = []


url = "https://api.simsimi.vn/v1/simtalk"


async def response(message) -> str:
    payload = {
        "text": message,
        "lc": 'vn'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = json.loads(response.text)
        message = data.get("message")
    #   print(message)
        logger.info(f"Prompt response: {message}")
        return message
    else:
        print("Không thể lấy dữ liệu từ API")
        return "Không thể lấy dữ liệu từ API"
