from app.utils.loader import load_json_data
from app.models.bike_config import BikeConfig

def recommend_components(config: BikeConfig):
    result = {}

    # Chain Matching
    chains = load_json_data("chains.json")
    chain_match = next(
        (c for c in chains
         if config.rear_speeds in c["speeds"]
         and config.drivetrain_brand in c["compatible_brands"]),
        None
    )
    result["chain"] = chain_match or "No match found"

    # Cassette Matching
    cassettes = load_json_data("cassettes.json")
    cassette_match = next(
        (c for c in cassettes
         if config.rear_speeds in c["speeds"]
         and config.drivetrain_brand == c["brand"]),
        None
    )
    result["cassette"] = cassette_match or "No match found"

    # Brake Pad Matching
    brake_pads = load_json_data("brake_pads.json")
    pad_match = next(
        (b for b in brake_pads
         if b["system"].lower() == config.brake_system.lower()
         and b["brake_type"].lower() == config.brake_type.lower()
         and config.brake_brand.lower() == b["brand"].lower()),
        None
    )
    result["brake_pads"] = pad_match or "No match found"

    # Tire Matching
    tires = load_json_data("tires.json")
    tire_match = next(
        (t for t in tires
         if t["marked_size"] == config.tire_size),
        None
    )
    result["tire"] = tire_match or "No match found"

    # Tube Matching
    tubes = load_json_data("tubes.json")
    tube_match = next(
        (t for t in tubes
         if config.valve_type.lower() == t["valve_type"].lower()
         and str(config.valve_length).replace("mm", "") == str(t["valve_length_mm"])),
        None
    )
    result["tube"] = tube_match or "No match found"

    return result
