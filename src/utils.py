# src/utils.py
import os
import json
from datetime import datetime

def save_chat_history(history, path="history"):
    os.makedirs(path, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = os.path.join(path, f"chat_{ts}.json")
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    return fname

def export_history_as_json(history):
    return {
        "metadata": {"exported_at": datetime.now().isoformat()},
        "chat": history
    }

def validate_env_keys(keys):
    missing = []
    for k in keys:
        if os.getenv(k) is None:
            missing.append(k)
    return missing
