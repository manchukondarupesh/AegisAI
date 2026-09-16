from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "agents"
    )
)

from multi_agents import supervisor

from drone_db_agent import (
    get_drones,
    get_low_battery_drones,
    get_high_temperature_drones,
    get_high_alerts,
    get_missions,
    get_telemetry
)

app = FastAPI(
    title="AegisAI",
    description="Multi-Agent Drone Intelligence Platform",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AegisAI Drone Intelligence API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "system": "AegisAI"
    }


@app.post("/chat")
def chat(request: UserRequest):

    result = supervisor(request.question)

    return {
        "question": request.question,
        "agent": result.get("agent", "Supervisor"),
        "answer": result.get("answer", "No answer available")
    }

@app.get("/dashboard")
def dashboard():

    drones = get_drones()
    low_battery = get_low_battery_drones()
    high_temperature = get_high_temperature_drones()
    high_alerts = get_high_alerts()

    return {
        "total_drones": len(drones),
        "low_battery": low_battery,
        "high_temperature": high_temperature,
        "high_alerts": high_alerts
    }
@app.get("/drones")
def drones():

    drone_list = get_drones()

    return {
        "drones": drone_list
    }
@app.get("/missions")
def missions():

    mission_list = get_missions()

    return {
        "missions": mission_list
    }
@app.get("/telemetry")
def telemetry():
    telemetry_data = get_telemetry()

    return {
        "telemetry": telemetry_data
    }