import pytest
from app.services.matcher import ComponentMatcher
from app.models.bike_config import BikeConfiguration


# Sample test data
test_component_data = {
    "chains": [
        {
            "id": "chain-001",
            "name": "Test Chain 1",
            "type": "chain",
            "compatibility": ["11-speed", "Shimano"],
            "brand": "Test Brand"
        },
        {
            "id": "chain-002",
            "name": "Test Chain 2",
            "type": "chain",
            "compatibility": ["all"],
            "brand": "Another Brand"
        }
    ],
    "brake_pads": [
        {
            "id": "brake-001",
            "name": "Test Brake Pads",
            "type": "brake_pad",
            "compatibility": ["hydraulic disc"],
            "brand": "Test Brand"
        }
    ]
}


def test_find_compatible_components():
    # Initialize the matcher with test data
    matcher = ComponentMatcher(test_component_data)
    
    # Create a test bike configuration
    bike_config = BikeConfiguration(
        frame_size="M",
        wheel_size="29",
        brake_type="hydraulic disc",
        drivetrain_type="11-speed"
    )
    
    # Test finding chains
    chains = matcher.find_compatible_components(bike_config, "chains")
    assert len(chains) == 2
    
    # Test finding brake pads
    brake_pads = matcher.find_compatible_components(bike_config, "brake_pads")
    assert len(brake_pads) == 1
    assert brake_pads[0].id == "brake-001"
    
    # Test preferences
    preferred_chains = matcher.find_compatible_components(
        bike_config, 
        "chains", 
        preferences=["Test Brand"]
    )
    assert len(preferred_chains) > 0
    assert preferred_chains[0].brand == "Test Brand" 