from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import JSONResponse
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class WorkoutRequest(BaseModel):
    input: str

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    # Better structured prompt for a 2-week program
    prompt = (
        f"Create a 2-week home workout program for a {data.input}. "
        "The user should train 5 days per week (Monday to Friday). "
        "Each day must include:\n"
        "- Warm-up (5–10 minutes)\n"
        "- Main workout (20–40 minutes)\n"
        "- Cooldown (5–10 minutes)\n\n"
        "Use this format:\n\n"
        "## Week 1\n"
        "### Day 1 – [Workout Title or Goal]\n"
        "**Warm-up:**\n"
        "- ...\n"
        "**Main Workout:**\n"
        "- ...\n"
        "**Cooldown:**\n"
        "- ...\n\n"
        "Repeat for Day 2 through Day 5.\n\n"
        "## Week 2\n"
        "(Same format for Days 1–5)\n\n"
        "Ensure variety, goal-appropriate exercises, clear formatting, and professional tone."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an elite certified personal trainer. You design training plans "
                    "tailored to individual goals and experience levels. Each workout must be:\n"
                    "- Well-balanced (push/pull, upper/lower body)\n"
                    "- Goal-specific (fat loss, endurance, strength, etc.)\n"
                    "- Scaled for fitness level (beginner, intermediate, advanced)\n"
                    "- Structured with a warm-up, main workout, and cooldown\n"
                    "- Professionally formatted and clear"
                )
            },
            {"role": "user", "content": prompt}
        ]
    )

    workout_text = response.choices[0].message.content
    return JSONResponse(content={"workout": workout_text})
