from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class WorkoutRequest(BaseModel):
    input: str

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    prompt = (
        f"{data.input}\n\n"
        "Provide the workout plan in this exact structure:\n"
        "## Week 1\n"
        "### Day 1 – [Name of Focus]\n"
        "**Warm-up:**\n"
        "- Example warm-up 1\n"
        "- Example warm-up 2\n"
        "**Main Workout:**\n"
        "1. Exercise 1\n"
        "2. Exercise 2\n"
        "**Cooldown:**\n"
        "- Stretch 1\n"
        "- Stretch 2\n"
        "\nRepeat this format for EVERY day in EVERY week requested. Do not skip weeks. Do not summarize. The full plan must be structured and explicit for all weeks and days."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional fitness coach. Provide full workout plans with warm-up, main, and cooldown sections per day."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"workout": response.choices[0].message.content}
