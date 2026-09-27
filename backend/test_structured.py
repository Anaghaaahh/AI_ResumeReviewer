from groq import Groq
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()


class TestResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
    score: int


response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": "Return a simple structured response."
        },
        {
            "role": "user",
            "content": "Say hello and give a score of 10."
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "test_response",
            "strict": True,
            "schema": TestResponse.model_json_schema()
        }
    }
)

result = json.loads(response.choices[0].message.content)

validated = TestResponse.model_validate(result)

print(validated)
print(validated.model_dump())
