from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Allow requests from Vercel and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "AI Space Intelligence API Running"
    }

@app.get("/occupancy")
def occupancy():

    with open("backend/live_data.json", "r") as f:
        data = json.load(f)

    people_count = data["people_count"]
    status = data["status"]

    max_capacity = 20

    utilization = round(
        (people_count / max_capacity) * 100,
        2
    )

    return {
        "people_count": people_count,
        "status": status,
        "space_utilization": f"{utilization}%"
    }