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

    # ✅ Strong, clear prompt to force full multi-week response
    prompt = (
        f"Create a {num_weeks}-week home workout program for a {input_text}. "
        "The user will train 5 days per week (Monday to Friday). "
        "You must list **every day** of **every week** clearly.\n\n"
        "Each day must include:\n"
        "- Warm-up (5–10 minutes)\n"
        "- Main workout (20–30 minutes)\n"
        "- Cooldown (5–10 minutes)\n\n"
        f"You must include exactly {num_weeks} weeks and 5 days per week.\n"
        "Do not skip any days.\n"
        "Do not summarize.\n"
        "Use this format exactly:\n\n"
    )

    for week in range(1, num_weeks + 1):
        prompt += f"## Week {week}\n"
        for day in range(1, 6):
            prompt += (
                f"### Day {day} – [Workout Focus]\n"
                "**Warm-up:**\n- ...\n"
                "**Main Workout:**\n- ...\n"
                "**Cooldown:**\n- ...\n\n"
            )

    prompt += (
        "Respond only with the full workout program in markdown-style format. "
        "Do not explain or add summaries before or after."
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
                    "- Follow structure: Warm-up, Main Workout, Cooldown"
                )
            },
            {"role": "user", "content": prompt}
        ]
    )

    workout_text = response.choices[0].message.content
    return JSONResponse(content={"workout": workout_text})
