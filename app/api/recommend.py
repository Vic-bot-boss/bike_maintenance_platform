from fastapi import APIRouter, HTTPException, Depends
from app.auth.auth import get_current_user
from app.services.matcher import recommend_components
from app.models.bike_config import BikeConfig
import json
from pathlib import Path

router = APIRouter()
bikes_path = Path("app/data/bikes.json")

def load_bikes():
    if not bikes_path.exists():
        return {}
    with open(bikes_path, "r") as f:
        content = f.read().strip()
        return json.loads(content) if content else {}

@router.get("/recommend/{bike_id}")
def recommend_for_bike(bike_id: str, user_email: str = Depends(get_current_user)):
    bikes = load_bikes()
    user_bikes = bikes.get(user_email, [])
    bike_data = next((b for b in user_bikes if b["id"] == bike_id), None)

    if not bike_data:
        raise HTTPException(status_code=404, detail="Bike not found")

    try:
        config = BikeConfig(**bike_data)
        result = recommend_components(config)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {e}")