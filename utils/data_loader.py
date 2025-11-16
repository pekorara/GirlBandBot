import asyncio
import json, os
from typing import List
from utils.generate_mujica import save_list_to_file

def _load_json_list(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def load_mujica_list() -> List[dict]:
    path = os.path.join("static", "data", "mujica.json")
    data = _load_json_list(path)
    if not data:
        asyncio.run(save_list_to_file("mujica"))
        data = _load_json_list(path)
    return data

def load_mygo_list() -> List[dict]:
    return _load_json_list(os.path.join("static", "data", "mygo.json"))