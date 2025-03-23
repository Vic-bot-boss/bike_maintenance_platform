from fastapi import FastAPI
from app.api import recommend

app = FastAPI(
    title="Bike Maintenance Platform",
    description="Suggests compatible components based on user bike configuration",
    version="0.1"
)

@app.get("/")
def read_root():
    return {"message": "Bike Maintenance API is running. Try POST /api/recommend"}

# Include route module
app.include_router(recommend.router, prefix="/api")
