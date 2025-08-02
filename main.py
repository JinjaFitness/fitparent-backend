from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Create OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define input format expected from frontend
class WorkoutRequest(BaseModel):
    input: str

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    # Build detailed and structured prompt
    prompt = (
        data.input + "\n\n"
        "Please format the workout clearly into these three sections:\n"
        "**Warm-up**\n"
        "**Workout**\n"
        "**Cooldown**\n"
        "Use line breaks and bullet points for each section."
    )

    # Send request to OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful and professional fitness coach."},
            {"role": "user", "content": prompt}
        ]
    )

    # Return workout text
    return {"workout": response.choices[0].message.content}
