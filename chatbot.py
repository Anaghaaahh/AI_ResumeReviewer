from dotenv import load_dotenv
from groq import Groq

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


def get_ai_response(messages):
 try:
   stream = client.chat.completions.create(
   model="openai/gpt-oss-20b",
   messages=messages,
   stream=True
   )
 except Exception as e:
   print("AI Service error",e)
   return None

 ai_response=""
 for chunk in stream:
   text=chunk.choices[0].delta.content
   if text:
    print(text,end="")
    ai_response += text
 print()
 return ai_response


def handle_command(user_input):
 if user_input.lower()=="/help":
   print("""Available commands:
 /help  - Show available commands
 /clear - Clear conversation history
 /quit  - Exit chatbot""")
   return "handled"
 if user_input.lower()=="/clear":
   print("Conversation cleared")
   return "clear"
 if user_input.lower()=="/quit":
   return "quit"
 return None


def main():


    messages = create_message()

    while True:
        user_input = input("You: ")
        command = handle_command(user_input)

        if command == "quit":
            break

        if command == "clear":
            messages = create_message()
            continue

        if command == "handled":
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        ai_response = get_ai_response(messages)

        if ai_response is None:
            continue

        messages.append({
            "role": "assistant",
            "content": ai_response
        })


if __name__ == "__main__":
    main()