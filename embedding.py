import requests 

url = "http://localhost:11434/api/embeddings"

def embedding_model(text):
    response = requests.post(url , json={
        "model": "nomic-embed-text:latest",
        "prompt" : text
    })

    return response.json()["embedding"]



