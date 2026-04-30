import os
import json
import datetime 
from embedding import embedding_model


MEMORY_FILE = "memory.json"
MAX_MEMORY = 100


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def add_memory(user, agent):
    memory = load_memory()

    memory.append({
        "user": user,
        "agent": agent,
        "time": str(datetime.datetime.now())
    })

    memory = memory[-MAX_MEMORY:]

    save_memory(memory)


def get_memory(limit=5):
    memory = load_memory()
    mem = memory[-limit:]

    mem_context = "\n".join([
        f"User: {m['user']}\nAssistant: {m['agent']}"
        for m in mem
    ])

    return mem_context