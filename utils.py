import requests

url = "http://localhost:11434/api/generate"
def generate(prompt):
    response = requests.post(url , json={
        "model":"qwen2.5:7b",
        "prompt":prompt,
        "stream":False,
        "options": {
            "temperature": 0.3, # randomness controll = less temperature more acurate and strict , more temprecture creative 
            "top_p": 0.9, # probability filtering (nucleus sampling) - Instead of picking from ALL words, it picks from the smallest set of words whose total probability = 90%
            "repeat_penalty": 1.1 # panalize token that already used (anti loop control) avoide repetation
        }
    })

    return response.json().get("response")

