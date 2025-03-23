from datetime import datetime
from typing import Dict, Optional

def estimate_wear(installed_at: str, weekly_km: float) -> Dict[str, float]:
    if not installed_at or not weekly_km:
        return {}

    try:
        start_date = datetime.strptime(installed_at, "%Y-%m-%d")
        today = datetime.today()
        weeks = (today - start_date).days / 7
        total_km = weeks * weekly_km
    except Exception:
        return {}

    return {
        "chain_wear": min((total_km / 2000) * 100, 100),
        "cassette_wear": min((total_km / 6000) * 100, 100),
        "brake_pad_wear": min((total_km / 1500) * 100, 100),
        "tire_wear": min((total_km / 3000) * 100, 100),
        "estimated_km": round(total_km, 1)
    }

def estimate_component_wear(install_date: Optional[str], weekly_km: float, lifespan_km: float) -> float:
    if not install_date:
        return 0
    try:
        installed = datetime.strptime(install_date, "%Y-%m-%d")
        weeks = (datetime.today() - installed).days / 7
        total_km = weeks * weekly_km
        wear = (total_km / lifespan_km) * 100
        return min(round(wear, 1), 100)
    except Exception:
        return 0
