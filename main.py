from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected request body structure
class WorkoutRequest(BaseModel):
    goal: str
    level: str
    duration: int
    time: str

# API route to handle workout generation
@app.post("/generate-workout")
async def generate_workout(request: WorkoutRequest):
    # Simulate workout generation
    sample_workout = f"""
## Week 1
### Day 1 – {request.goal.capitalize()} Training
**Warm-up:**\n- Light jog (5 min)\n- Dynamic stretches
**Main Workout:**\n- Push-ups, Squats, Planks ({request.duration} mins total)
**Cooldown:**\n- Light stretching

...repeat similar structure for more days and weeks...
"""
    return {"workout": sample_workout.strip()}
