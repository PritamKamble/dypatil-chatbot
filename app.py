from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
while True:
    response = client.responses.create(
        input=input('Enter your message:'),
        model="openai/gpt-oss-20b",
    )
    print(response.output_text)
