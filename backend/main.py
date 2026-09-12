from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

load_dotenv()

client = Groq()


def create_message():
    return [
        {
            "role": "system",
            "content": """
You are an AI learning assistant for a beginner learning Python and Generative AI.

Your job is to teach, not just give answers.

Rules:
- Explain concepts in simple language.
- Break difficult concepts into small steps.
- Use simple examples when useful.
- If the user asks a coding question, explain the logic before giving the code.
- If the user seems confused, explain the concept differently.
- Do not assume advanced knowledge.
"""
        }
    ]


messages = create_message()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "fastapi backend is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    messages.append({
        "role": "user",
        "content": request.message
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    ai_response = response.choices[0].message.content

    messages.append({
        "role": "assistant",
        "content": ai_response
    })

    return {
        "response": ai_response
    }


@app.post("/clear")
def clear_chat():

    global messages

    messages = create_message()

    return {
        "message": "Conversation cleared"
    }