from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client (uses API key from environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define input structure
class WorkoutRequest(BaseModel):
    goal: str
    fitness_level: str
    time: int        # in minutes
    length: int      # in weeks

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    # Clean prompt with clear format instruction
    prompt = (
        f"You're a professional personal trainer. Create a detailed {data.length}-week home workout plan "
        f"for a {data.fitness_level} user who wants to achieve {data.goal}. "
        f"Each week should contain 5 workout days with full detail. "
        f"Each workout should last about {data.time} minutes and include:\n"
        f"- Warm-up\n"
        f"- Main workout\n"
        f"- Cooldown\n\n"
        f"Format it clearly like this:\n"
        f"## Week 1\n"
        f"### Day 1 – [Workout focus]\n"
        f"**Warm-up:**\n- ...\n**Main Workout:**\n- ...\n**Cooldown:**\n- ...\n\n"
        f"... Repeat this format for each day and each week. No summaries. Just full content."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or 'gpt-3.5-turbo' if you're using the free tier
            messages=[
                {"role": "system", "content": "You are a professional fitness coach."},
                {"role": "user", "content": prompt}
            ]
        )

        workout_text = response.choices[0].message.content.strip()

        return {"workout": workout_text}

    except Exception as e:
        return {"error": str(e)}
