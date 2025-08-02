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
    prompt = (
        f"Design a workout for a {data.input}. The total duration should match their available time.\n\n"
        "Respond using this format:\n"
        "### Warm-up (5–10 minutes)\n"
        "- Include mobility and light cardio\n\n"
        "### Main Workout (20–40 minutes)\n"
        "- Use 3–5 exercises\n"
        "- Include sets/reps or durations\n"
        "- Add rest times\n"
        "- Optional: include a circuit format or EMOM/AMRAP\n\n"
        "### Cooldown (5–10 minutes)\n"
        "- Focus on breathing and stretching major muscle groups\n\n"
        "Make the workout realistic, safe, and goal-appropriate. Use headings and bullet points."
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
