import json
from pathlib import Path

# Resolve flag.Json relative to this file's own location instead of a
# hardcoded absolute path, so this works on any machine (local, CI, teammates).
_FLAG_FILE = Path(__file__).resolve().parents[1] / "Configs" / "flag.Json"

with open(_FLAG_FILE, encoding="utf-8") as f:
    FEATURE = json.load(f)


def is_enabled(feature_name):
    return FEATURE.get(feature_name, False)
