from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class WorkoutRequest(BaseModel):
    input: str

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    prompt = f"""
You are a certified personal trainer.

{data.input}

Requirements:
- Provide a complete workout plan for each week.
- Each week must contain 5 distinct workout days (Day 1–5).
- Each day must have: **Warm-up**, **Main Workout**, and **Cooldown**.
- Clearly label: ## Week X and ### Day Y – Title
- Format in Markdown using **bold** for section headers.
- Be progressive and suitable for {data.input.lower()}.
- If asked for 4/6/8 weeks, include all requested weeks in the plan.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fitness coach."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"workout": response.choices[0].message.content}
