from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import anthropic
from groq import Groq
import os
import json
from dotenv import load_dotenv
from typing import List

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not ANTHROPIC_KEY and not GROQ_KEY:
    raise ValueError("Tidak ada API key! Set ANTHROPIC_API_KEY atau GROQ_API_KEY di .env")

SYSTEM_PROMPT = """Kamu adalah Agent, asisten AI yang santai, pintar, dan selalu helpful.
Kamu berbicara dalam bahasa Indonesia dengan gaya casual dan bersahabat seperti teman dekat.
Kamu siap membantu dengan berbagai hal - dari pertanyaan sehari-hari, membantu pekerjaan,
memberikan saran, analisis, menulis, coding, sampai ngobrol santai.
Kamu cerdas tapi tidak sombong. Jawaban kamu selalu jelas, bermanfaat, dan to the point.
Gunakan emoji sesekali untuk membuat percakapan lebih hidup."""

anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_KEY) if ANTHROPIC_KEY else None
groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

def to_messages(messages):
    return [{"role": m.role, "content": m.content} for m in messages]

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    def generate():
        # Coba Claude dulu
        if anthropic_client:
            try:
                with anthropic_client.messages.stream(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=2048,
                    system=SYSTEM_PROMPT,
                    messages=to_messages(request.messages)
                ) as stream:
                    for text in stream.text_stream:
                        yield f"data: {json.dumps({'text': text})}\n\n"
                yield "data: [DONE]\n\n"
                return
            except Exception as e:
                print(f"[Claude gagal] {e} → beralih ke Groq...")

        # Fallback ke Groq
        if groq_client:
            try:
                msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + to_messages(request.messages)
                stream = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=msgs,
                    max_tokens=2048,
                    stream=True
                )
                for chunk in stream:
                    text = chunk.choices[0].delta.content
                    if text:
                        yield f"data: {json.dumps({'text': text})}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                print(f"[Groq gagal] {e}")
                yield f"data: {json.dumps({'text': 'Maaf, semua AI sedang bermasalah. Coba lagi nanti! 😅'})}\n\n"
                yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Coba Claude dulu
    if anthropic_client:
        try:
            response = anthropic_client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                messages=to_messages(request.messages)
            )
            return {"reply": response.content[0].text, "source": "claude"}
        except Exception as e:
            print(f"[Claude gagal] {e} → beralih ke Groq...")

    # Fallback ke Groq
    if groq_client:
        try:
            msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + to_messages(request.messages)
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=msgs,
                max_tokens=2048
            )
            return {"reply": response.choices[0].message.content, "source": "groq"}
        except Exception as e:
            print(f"[Groq gagal] {e}")

    return {"reply": "Maaf, semua AI sedang bermasalah. Coba lagi nanti! 😅", "source": "none"}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
