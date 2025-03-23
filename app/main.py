from fastapi import FastAPI
from app.api import recommend

app = FastAPI(
    title="Bike Maintenance Platform",
    description="Suggests compatible components based on user bike configuration",
    version="0.1"
)

# Include route module
app.include_router(recommend.router, prefix="/api")
