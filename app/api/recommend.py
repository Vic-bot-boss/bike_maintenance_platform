from fastapi import APIRouter
from app.models.bike_config import BikeConfig
from app.services.matcher import recommend_components

router = APIRouter()

@router.post("/recommend")
async def get_recommendation(config: BikeConfig):
    return recommend_components(config)
