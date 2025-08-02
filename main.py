# backend/main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow local frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class WorkoutRequest(BaseModel):
    input: str

@app.post("/generate-workout")
async def generate_workout(request: WorkoutRequest):
    input_text = request.input

    # Simulate AI workout generation
    # Replace this with real GPT call or your logic
    fake_output = f"## Week 1\n### Day 1 – Full Body Strength\n**Warm-up:**\n- Jog x 1 min\n- Arm Circles x 1 min\n\n**Main Workout:**\n1. Squats 3x10\n2. Push-ups 3x10\n\n**Cooldown:**\n- Hamstring Stretch 30 sec each leg\n\n### Day 2 – Cardio\n..."

    return {"workout": fake_output}
