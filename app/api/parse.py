from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.bike_config import BikeConfig
from app.config import OPENAI_API_KEY
import openai

router = APIRouter()

class DescriptionInput(BaseModel):
    description: str

openai.api_key = OPENAI_API_KEY

@router.post("/parse-config")
def parse_bike_description(data: DescriptionInput):
    prompt = f"""
Extract the bike configuration from the following user description as a JSON that matches this schema:
{BikeConfig.schema_json(indent=2)}

User description: "{data.description}"
Only include fields with enough information to infer.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a smart assistant that converts bike descriptions into structured configuration."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        content = response.choices[0].message.content  # ✅ fixed access
        return {"parsed_config": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")
