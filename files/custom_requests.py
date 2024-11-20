import requests
import os
import csv
import random

CWD = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(CWD, "data", "graph.nodes.csv")
URL = "http://localhost:5009"

def make_request(url, headers):
    try:
        print(f"Making request to {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request was successful (status code 200)
        return response.json()  # Return response as JSON
    except Exception as e:
        return {"error": str(e)}

def stats_requests():
    url = f"{URL}/graph/stats"
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"Making request to {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request was successful (status code 200)
        
        try:
            return response.json()  # Attempt to return JSON data
        except ValueError:
            # If the response is not JSON, handle accordingly
            return {"error": "Response is not in JSON format."}

    except requests.exceptions.RequestException as e:
        # Handle general HTTP errors (including connection errors, timeouts, etc.)
        return {"Request failed": str(e)}
    except Exception as e:
        # Handle any other unexpected exceptions
        return {"Error": str(e)}

def get_neighbours(id):
    url = f"{URL}/graph/neighbors/{id}"
    headers = {
        "Content-Type": "text/plain",
        "Transfer-Encoding": "chunked"
    }

    content = bytearray()  # Default value if request fails

    try:
        print(f"Making request to {url}...")
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # Check if request was successful (status code 200)
        for chunk in response.iter_content(chunk_size=128):
            content.extend(chunk)  # If successful, store the response text

    except requests.exceptions.RequestException as e:
        # Handle general HTTP errors (including connection errors, timeouts, etc.)
        print(f"Error during request: {e}")
        content = bytearray(b"Request failed")  # Return a message indicating failure

    try:
        with open(os.path.join(CWD, "data", "bytes.txt"), 'wb') as f:
            f.write(content)  # Write the bytes data to the file
        print(f"Data successfully written to file")
    except Exception as e:
        print(f"Error writing data to file: {e}")

    return content  # Return the content (or failure message)

def extract_random_id():
    with open(PATH, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        selected_row = None
        for i, row in enumerate(reader):
            # Select a row with probability 1/(i+1)
            if random.randint(0, i) == 0:
                selected_row = row[0]
        return selected_row 


if __name__ == '__main__':
    # response = stats_requests()
    # print(response)
    # print(extract_ids()[:100])
    # print(extract_random_id())
    print("hi")