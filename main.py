from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a fitness coach."},
        {"role": "user", "content": "Make a 15-minute beginner workout to lose weight."}
    ]
)
print(response.choices[0].message.content)
