from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from io import BytesIO
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
API_URL = 'https://api.puter.com/drivers/call'
HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': f"Bearer {os.getenv('API_TOKEN')}",
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://docs.puter.com',
    'Referer': 'https://docs.puter.com/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

# Models
class Message(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class TTSRequest(BaseModel):
    text: str

# Store conversation history
conversation_history: List[dict] = []

async def chat_completion(message: str) -> str:
    conversation_history.append({"content": message})
    
    data = {
        "interface": "puter-chat-completion",
        "driver": "openai-completion",
        "method": "complete",
        "args": {
            "messages": conversation_history
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        
        response_json = response.json()
        if response_json.get("success"):
            bot_reply = response_json['result']['message']['content']
            conversation_history.append({"content": bot_reply, "role": "assistant"})
            return bot_reply
        raise HTTPException(status_code=500, detail="Failed to get a valid response from the API")
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

async def text_to_speech(text: str) -> Optional[BytesIO]:
    data = {
        "interface": "puter-tts",
        "driver": "aws-polly",
        "method": "synthesize",
        "args": {
            "text": text
        }
    }

    try:
        response = requests.post(API_URL, json=data, headers=HEADERS)
        response.raise_for_status()
        return BytesIO(response.content)
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: Message):
    if not message.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    response = await chat_completion(message.message)
    return ChatResponse(response=response)

@app.post("/tts")
async def tts_endpoint(request: TTSRequest):
    if not request.text.strip():
