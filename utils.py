import requests

url = "http://localhost:11434/api/generate"
def generate(prompt):
    response = requests.post(url , json={
        "model":"gemma4:e2b",
        "prompt":prompt,
        "stream":False,
        "options": {
            "temperature": 0.3
        }
    })

    return response.json().get("response")


