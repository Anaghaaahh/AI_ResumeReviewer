from groq import Groq
from dotenv import load_dotenv
from main import ResumeReview
import json

load_dotenv()

client = Groq()

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": "Return a valid resume review using the provided schema."
        },
        {
            "role": "user",
            "content": "Give a simple resume review."
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "resume_review",
            "strict": True,
            "schema": ResumeReview.model_json_schema()
        }
    }
)

result = json.loads(response.choices[0].message.content)

review = ResumeReview.model_validate(result)

print(review)
print("\nValidation successful!")