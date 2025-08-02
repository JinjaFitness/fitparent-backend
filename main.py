from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# Create OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define expected input
class WorkoutRequest(BaseModel):
    input: str

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    # Create a clean and consistent prompt
    prompt = (
        data.input + "\n\n"
        "Please format the workout into three clearly marked sections:\n"
        "**Warm-up**\n"
        "**Workout**\n"
        "**Cooldown**\n"
        "Use line breaks and bullet points."
    )

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful and professional fitness coach."},
            {"role": "user", "content": prompt}
        ]
    )

    workout_text = response.choices[0].message.content

    # Ensure valid JSON response
    return JSONResponse(content={"workout": workout_text})
