from ddgs import DDGS
from datetime import datetime

def get_datetime(_=None):
    now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    return f"Current date is {current_date} and time is {current_time}"

def calculator(expression):
    try:
        print(f"🧮 Calculating: {expression}")
        allowed_names = {"__builtins__": None}
        return str(eval(expression, allowed_names, {}))
    except:
        return "Error in calculation"

def save_note(note):
    print(f"📝 Saving note: {note}")
    with open("notes.txt", "a") as f:
        f.write(f"[NOTE] {note}\n")
    return "Note saved!"

def web_search(query):
    try:
        print(f"🌐 Web search called: {query}")
        results = []

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results.append(f"{r['title']} - {r['body']}")

        return "\n".join(results)

    except Exception as e:
        return f"Search error: {str(e)}"
    
    
TOOLS = {
    "calculator": calculator,
    "web_search": web_search,
    "get_datetime": get_datetime,
    "save_note": save_note
}