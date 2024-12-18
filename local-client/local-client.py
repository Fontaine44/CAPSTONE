# make requests to localhost 3000 with the graph.nodes.csv file (which contains a list of ids)
# and print the results

import requests
import random
import os
import base64

ID_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'server', 'files', 'data', 'graph.nodes.csv'))

def get_ids():
    with open(ID_FILE, 'r') as file:
        ids = file.readlines()
    return ids

def get_node(id):
    return requests.get(f'http://localhost:3000/node/{id}')

def get_stats():
    return requests.get('http://localhost:3000/stats')

if __name__ == '__main__':
    # ids = get_ids()
    # id = random.choice(ids).strip()
    id = 'swh:1:cnt:ae0cdaa30908f360449bc5dc261dda2040e6f3ba'
    response = get_node(id)
    print(response.json())
    if 'data' in response.json():
        b_str = response.json()['data']
        # decode b_str
        b_str = base64.b64decode(b_str)
        print(b_str)
    