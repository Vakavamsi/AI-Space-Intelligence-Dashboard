from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "backend/live_data.json"

# Create file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "people_count": 0,
                "status": "Not Crowded"
            },
            f
        )


class OccupancyData(BaseModel):
    people_count: int
    status: str


@app.get("/")
def home():
    return {
        "message": "AI Space Intelligence API Running"
    }


@app.get("/occupancy")
def occupancy():

    with open(DATA_FILE, "r") as f:
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


@app.post("/update-count")
def update_count(data: OccupancyData):

    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "people_count": data.people_count,
                "status": data.status
            },
            f
        )

    return {
        "message": "Count Updated Successfully",
        "people_count": data.people_count,
        "status": data.status
    }