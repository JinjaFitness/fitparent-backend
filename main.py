from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client with your API key from the environment
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
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a fitness coach."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"workout": response.choices[0].message.content}
