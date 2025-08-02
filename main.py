from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Expecting a single "input" field from frontend
class WorkoutRequest(BaseModel):
    input: str

@app.post("/generate-workout")
def generate_workout(data: WorkoutRequest):
    prompt = data.input

    # Call OpenAI with the user-defined prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fitness coach."},
            {"role": "user", "content": prompt}
        ]
    )

    # Return workout text
    return {"workout": response.choices[0].message.content}
