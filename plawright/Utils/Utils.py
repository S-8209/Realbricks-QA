import json
from pathlib import Path
import pytest 
from typing import List, Dict, Any

def load_users(key) -> List[Dict[str, Any]]:
    file_path = Path(__file__).parents[1] / "Data" / "Cred.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    user = data.get(key)
    if not user:
        raise ValueError(f"user {key} not available")
    return user