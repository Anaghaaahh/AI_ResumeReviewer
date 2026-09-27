from groq import Groq
from dotenv import load_dotenv
from main import ResumeReview, create_message
import json

load_dotenv()

client = Groq()

messages = create_message()

messages.append({
    "role": "user",
    "content": """
Please review the following resume.

Resume:
John Doe
B.Tech Computer Science
CGPA: 8.5

Technical Skills:
Python, JavaScript, React

Projects:
- Built a student management website using JavaScript.
- Created a simple Python chatbot.

Job description:
Software Engineering Intern
Requirements:
- Python
- JavaScript
- React
- Git
- SQL

User instructions:
Focus on whether the technical skills are demonstrated through the projects.
Do not assume a listed skill is demonstrated without evidence.
"""
})

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    max_completion_tokens=4096,
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "resume_review",
            "strict": True,
            "schema": ResumeReview.model_json_schema()
        }
    }
)

ai_response = response.choices[0].message.content
result = json.loads(ai_response)
review = ResumeReview.model_validate(result)

print(review)
print("\nValidation successful!")
