from pydantic import BaseModel
from typing import Optional

class BikeConfig(BaseModel):
    bike_type: Optional[str]
    rear_speeds: int
    drivetrain_brand: str
    front_chainrings: str  # "1x", "2x", "3x"
    brake_type: str        # "Rim", "Disc"
    brake_system: str      # "Hydraulic", "Mechanical", etc.
    brake_brand: str
    tire_size: str         # e.g. "700x28c"
    valve_type: str        # "Presta", "Schrader", etc.
    valve_length: str      # "32mm", "48mm", etc.
