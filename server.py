from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from pydantic import BaseModel
import requests
from io import BytesIO
from puter import add_message, synthesize


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
def index():
    return FileResponse("public/index.html")

class ChatMessage(BaseModel):
    message: str

class TTSRequest(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: ChatMessage):
    if not message.message:
        raise HTTPException(status_code=400, detail="No message provided")
    
    bot_response = add_message(message.message)
    return JSONResponse(content={'response': bot_response})

@app.post("/tts")
async def tts(request: TTSRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    responseContent = synthesize(request.text)
    audio_data = BytesIO(responseContent)
    if not audio_data:
        raise HTTPException(status_code=500, detail="Failed to generate TTS")
    
    return StreamingResponse(
        audio_data,
        media_type="audio/mp3"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)