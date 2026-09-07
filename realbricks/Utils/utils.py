import json , random , re
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


def _random_email(prefix: str = "sl") -> str:
    """Generate a unique yopmail address."""
    return f"{prefix}{random.randint(1, 200_000)}@yopmail.com"
# realbricks/Utils/utils.py

import re

def clean_value(value: str) -> float:
    if not value:
        return 0.0

    # Remove any parenthetical content, wherever it appears
    value = re.sub(r"\([^)]*\)", "", value).strip()

    cleaned = re.sub(r"[^0-9.\-]", "", value)
    cleaned = re.sub(r"-{2,}", "", cleaned)

    if not cleaned or cleaned in ["-", "."]:
        return 0.0

    return float(cleaned)

def current_date() -> str:
    """Return today's date in format: Thursday, June 26, 2026"""
    from datetime import datetime
    return datetime.now().strftime("%A, %B %d, %Y")
# Utils.py
def values_match(actual: float, expected: float, tolerance: float = 0.01) -> bool:
    return abs(actual - expected) < tolerance