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
    "Format the workout like this:\n"
    "### Warm-up (5 minutes)\n"
    "- Light cardio: 2 minutes (e.g., jumping jacks, high knees)\n"
    "- Dynamic stretches: 3 minutes (e.g., arm circles, lunges)\n\n"
    "### Workout (25 minutes)\n"
    "- 3 exercises repeated in a circuit (e.g., squats, push-ups, planks)\n"
    "- Provide set/reps for each\n"
    "- Include rest time\n\n"
    "### Cooldown (5 minutes)\n"
    "- Static stretches for major muscle groups\n"
    "- Focus on breathing and recovery\n\n"
    "Ensure the workout matches the user's goal, fitness level, and total time.\n"
    "Format clearly using headings and bullet points."
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
