from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class WorkoutRequest(BaseModel):
    goal: str
    fitness_level: str
    time: int  # in minutes
    weeks: int  # number of weeks

@app.post("/generate-workout")
async def generate_workout(data: WorkoutRequest):
    prompt = (
        f"Generate a {data.weeks}-week home workout plan for an {data.fitness_level} individual with a goal of {data.goal}. "
        f"Each workout should last around {data.time} minutes. Include a warm-up, main workout, and cooldown for each day.\n"
        f"Use the following format:\n"
        f"## Week 1\n### Day 1 – [Workout Focus or Name]\n**Warm-up:**\n- Exercise 1\n- Exercise 2\n\n"
        f"**Main Workout:**\n1. Exercise 1\n2. Exercise 2\n\n**Cooldown:**\n- Stretch 1\n- Stretch 2\n\n"
        f"Repeat the same format for each day and week. There should be 5 workout days per week. "
        f"DO NOT skip or summarize any weeks. DO NOT write 'continue this structure'. "
        f"Only include the workouts, nothing else."
    )

    print(f"🔍 Sending input: {prompt}")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    result = response.choices[0].message.content.strip()

    return {"workout": result}
