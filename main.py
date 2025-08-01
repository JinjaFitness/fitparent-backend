from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

app = FastAPI()

class WorkoutRequest(BaseModel):
    goal: str
    fitness_level: str
    time: int

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    prompt = (
        f"Create a {data.time}-minute home workout for a {data.fitness_level} level "
        f"parent with a goal to {data.goal}. Include warm-up, workout, and cool-down. "
        f"No equipment."
    )
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a personal trainer."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"plan": response['choices'][0]['message']['content']}
