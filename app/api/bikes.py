from fastapi import APIRouter, Depends, HTTPException, Body
from app.models.bike import BikeProfile
from app.auth.auth import get_current_user
from app.services.wear import estimate_wear, estimate_component_wear
import json
import os
import uuid
from pathlib import Path
from fastapi import Body
from datetime import date
from pydantic import BaseModel
from typing import Optional


router = APIRouter()
bikes_path = Path("app/data/bikes.json")
bikes_path.parent.mkdir(parents=True, exist_ok=True)

# Ensure the file exists
if not bikes_path.exists():
    with open(bikes_path, "w") as f:
        json.dump({}, f)

def load_bikes():
    with open(bikes_path, "r") as f:
        content = f.read().strip()
        return json.loads(content) if content else {}

def save_bikes(data):
    with open(bikes_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

@router.post("/bikes")
def add_bike(bike: BikeProfile, user_email: str = Depends(get_current_user)):
    bikes = load_bikes()
    user_bikes = bikes.get(user_email, [])
    
    bike.id = str(uuid.uuid4())
    user_bikes.append(bike.dict())
    
    bikes[user_email] = user_bikes
    save_bikes(bikes)
    
    return {"msg": "Bike added successfully", "bike_id": bike.id}

@router.get("/bikes")
def list_bikes(user_email: str = Depends(get_current_user)):
    bikes = load_bikes()
    return bikes.get(user_email, [])

@router.get("/bikes/{bike_id}")
def get_bike(bike_id: str, user_email: str = Depends(get_current_user)):
    bikes = load_bikes()
    user_bikes = bikes.get(user_email, [])
    for bike in user_bikes:
        if bike["id"] == bike_id:
            return bike
    raise HTTPException(status_code=404, detail="Bike not found")

@router.put("/bikes/{bike_id}")
def update_bike(bike_id: str, updated_bike: BikeProfile = Body(...), user_email: str = Depends(get_current_user)):
    bikes = load_bikes()
    user_bikes = bikes.get(user_email, [])
    for idx, bike in enumerate(user_bikes):
        if bike["id"] == bike_id:
            updated_bike.id = bike_id  # Preserve ID
            user_bikes[idx] = updated_bike.dict()
            bikes[user_email] = user_bikes
            save_bikes(bikes)
            return {"msg": "Bike updated successfully"}
    raise HTTPException(status_code=404, detail="Bike not found")

@router.delete("/bikes/{bike_id}")
def delete_bike(bike_id: str, user_email: str = Depends(get_current_user)):
    bikes = load_bikes()
    user_bikes = bikes.get(user_email, [])
    new_bikes = [b for b in user_bikes if b["id"] != bike_id]
    if len(new_bikes) == len(user_bikes):
        raise HTTPException(status_code=404, detail="Bike not found")
    bikes[user_email] = new_bikes
    save_bikes(bikes)
    return {"msg": "Bike deleted"}

@router.get("/bikes/{bike_id}/status")
def get_bike_status(bike_id: str, user_email: str = Depends(get_current_user)):
    bikes = load_bikes()
    user_bikes = bikes.get(user_email, [])
    bike = next((b for b in user_bikes if b["id"] == bike_id), None)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    components = bike.get("components", {})
    weekly_km = bike.get("weekly_km", 50)

    status = {
        "chain_wear": estimate_component_wear(components.get("chain", {}).get("installed_at"), weekly_km, 2000),
        "cassette_wear": estimate_component_wear(components.get("cassette", {}).get("installed_at"), weekly_km, 6000),
        "brake_pads_wear": estimate_component_wear(components.get("brake_pads", {}).get("installed_at"), weekly_km, 1500),
        "tire_wear": estimate_component_wear(components.get("tires", {}).get("installed_at"), weekly_km, 3000)
    }

    return {
        "bike": bike["name"],
        "wear_estimates": status
    }

@router.post("/bikes/confirm-llm")
def confirm_and_add_llm_bike(bike: BikeProfile, user_email: str = Depends(get_current_user)):
    bikes = load_bikes()
    user_bikes = bikes.get(user_email, [])

    bike.assign_id()
    user_bikes.append(bike.dict())

    bikes[user_email] = user_bikes
    save_bikes(bikes)
    return {"msg": "Bike saved", "bike_id": bike.id}

class ServiceEntry(BaseModel):
    date: date
    action: str
    component: Optional[str]
    notes: Optional[str]

@router.post("/bikes/{bike_id}/service-log")
def add_service_entry(bike_id: str, entry: ServiceEntry, user_email: str = Depends(get_current_user)):
    bikes = load_bikes()
    user_bikes = bikes.get(user_email, [])
    for bike in user_bikes:
        if bike["id"] == bike_id:
            if "service_log" not in bike:
                bike["service_log"] = []
            bike["service_log"].append(entry.dict())
            save_bikes(bikes)
            return {"msg": "Service log entry added"}
    raise HTTPException(status_code=404, detail="Bike not found")
