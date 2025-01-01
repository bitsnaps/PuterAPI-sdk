import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = 'https://api.puter.com/drivers/call'
headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': f"Bearer {os.getenv('API_TOKEN')}",
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://docs.puter.com',
    'Referer': 'https://docs.puter.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

conversation_history = []

def add_message(message):
    conversation_history.append({"content": message})
    data = {
        "interface": "puter-chat-completion",
        "driver": "openai-completion",
        "test_mode": False,
        "method": "complete",
        "args": {
            "messages": conversation_history
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("success"):
            bot_reply = response_json['result']['message']['content']
            conversation_history.append({"content": bot_reply, "role": "assistant"})
            return bot_reply
        else:
            return "Failed to get a valid response from the API."
    else:
        return f"Request failed with status code {response.status_code}"

def synthesize(user_text):
    data = {
        "interface": "puter-tts",
        "driver": "aws-polly",
        "test_mode": False,
        "method": "synthesize",
        "args": {
            "text": user_text
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.content
    print(f"Request tts failed with status code: {response.status_code}")
    return None
