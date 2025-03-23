from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.docs import get_swagger_ui_html

from app.api import recommend
from app.auth import users
from app.api import bikes
from app.api import parse

app = FastAPI(
    title="Bike Maintenance API",
    description="Helps users configure and maintain bikes with replacement recommendations.",
    version="1.0.0"
)

# Manually define the OpenAPI schema to override the default OAuth2 UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Bike Maintenance API",
        version="1.0.0",
        description="A smart bike maintenance backend",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "Bike Maintenance API is running. Try POST /api/recommend"}

# Include route module
app.include_router(recommend.router, prefix="/api")
app.include_router(users.router, prefix="/api/auth")
app.include_router(bikes.router, prefix="/api")
app.include_router(parse.router, prefix="/api")
