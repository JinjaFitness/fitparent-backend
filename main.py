from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import JSONResponse
import os
import re

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class WorkoutRequest(BaseModel):
    input: str

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    input_text = data.input
    match = re.search(r"(\d+)\s*week", input_text.lower())
    num_weeks = int(match.group(1)) if match else 2

    # ✅ Structured prompt with progression and variation
    prompt = (
        f"Create a {num_weeks}-week home workout program for a {input_text}. "
        "The user should train 5 days per week (Monday to Friday). Each week must:\n"
        "- Progress in difficulty (slightly more reps, time, or complexity)\n"
        "- Use varied exercises across days and weeks\n"
        "- Remain safe and appropriate for a beginner\n"
        "- Be time-efficient (total session ~30 minutes)\n"
        "- Match the user’s goal (e.g. fat loss, strength)\n\n"
        "Each day must include:\n"
        "- Warm-up (5–10 minutes)\n"
        "- Main workout (20–40 minutes)\n"
        "- Cooldown (5–10 minutes)\n\n"
        "Use this format:\n\n"
    )

    for week in range(1, num_weeks + 1):
        prompt += f"## Week {week}\n"
        for day in range(1, 6):
            prompt += (
                f"### Day {day} – [Theme or Focus]\n"
                "**Warm-up:**\n- ...\n"
                "**Main Workout:**\n- ...\n"
                "**Cooldown:**\n- ...\n\n"
            )

    prompt += (
        "Ensure clear headings, bullet points, and a professional tone. "
        "Avoid repetition of exercises across days. Increase challenge subtly each week."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an elite certified personal trainer who specializes in working with beginners. "
                    "You design safe, progressive, and goal-based fitness programs. All workouts must:\n"
                    "- Be low-impact and beginner-friendly\n"
                    "- Use bodyweight or minimal equipment\n"
                    "- Increase slightly in intensity each week (progressive overload)\n"
                    "- Include exercise variation to prevent boredom\n"
                    "- Be realistic and engaging for parents with limited time\n"
                    "- Follow structure: Warm-up, Main, Cooldown"
                )
            },
            {"role": "user", "content": prompt}
        ]
    )

    workout_text = response.choices[0].message.content
    return JSONResponse(content={"workout": workout_text})
