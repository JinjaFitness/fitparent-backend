from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class WorkoutRequest(BaseModel):
    goal: str
    fitness_level: str
    time: int

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    prompt = (
        f"Create a {data.time}-minute home workout for a {data.fitness_level} "
        f"parent with a goal to {data.goal}. Include warm-up, workout, and cooldown."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fitness coach."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"workout": response.choices[0].message.content}
