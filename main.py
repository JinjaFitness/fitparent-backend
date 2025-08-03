from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the request structure
class WorkoutRequest(BaseModel):
    goal: str
    level: str
    duration: int
    weeks: int

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    prompt = (
        f"Create a {data.weeks}-week workout plan for a {data.level} user "
        f"with a goal of {data.goal}. Each workout should be about {data.duration} minutes "
        f"and include a warm-up, main workout, and cooldown. Provide daily variations for each week."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional fitness coach."},
                {"role": "user", "content": prompt}
            ]
        )

        workout_plan = response.choices[0].message.content
        return {"workout": workout_plan}

    except Exception as e:
        return {"error": str(e)}
