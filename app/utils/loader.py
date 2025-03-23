import json
import os

def load_json_data(filename: str):
    path = os.path.join("app", "data", filename)
    with open(path, "r") as f:
        return json.load(f)
