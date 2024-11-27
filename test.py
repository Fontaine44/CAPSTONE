import requests

OLLAMA_URL = "http://localhost:11434"  # Ollama URL from docker-compose

def send_request_to_ollama(prompt):
    """
    Sends a prompt to the Ollama API and returns the response.
    """
    url = f"{OLLAMA_URL}/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3.2",
        "prompt": prompt
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response  # Ollama likely responds with JSON
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return None

# Example usage
if __name__ == "__main__":
    prompt = "Tell me a joke!"
    response = send_request_to_ollama(prompt)
    text = f"[{response.text}]"
    if response:
        print("Response from Ollama:", response)
