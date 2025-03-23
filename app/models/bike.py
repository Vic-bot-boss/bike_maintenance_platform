from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date
from pydantic import Field
from uuid import uuid4

class Component(BaseModel):
    installed_at: Optional[date] = None
    model: Optional[str] = None
    notes: Optional[str] = None

class BikeProfile(BaseModel):
    id: Optional[str] = None
    name: str
    bike_type: Optional[str]
    rear_speeds: int
    drivetrain_brand: str
    front_chainrings: str
    brake_type: str
    brake_system: str
    brake_brand: str
    tire_size: str
    valve_type: str
    valve_length: str
    weekly_km: Optional[float] = 50.0

    components: Optional[Dict[str, Component]] = {}
    service_log: Optional[list] = []

    def assign_id(self):
        if not self.id:
            self.id = str(uuid4())