
memory = []

def add_memory(user ,agent):
    memory.append({
        "user":user,
        "Agent":agent
    })

def get_memory(limit=3):
    mem = memory[-limit:]
    mem_context = "\n".join([
    f"user: {m['user']}\nagent: {m['Agent']}"
    for m in mem
    ])
    return mem_context

