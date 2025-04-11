## For the Server (On your machine machine)

### For macOS and Linux
1. Navigate into the root directory through the terminal
2. Create venv with this command: `python3 -m venv .venv`
3. Activate venv with this command: `source venv/bin/activate`
4. Install requirements with this command: `pip install -r /requirements.txt`
5. Run the program with this command: `python3 main.py`

### For Windows
1. Navigate into the server directory through the terminal
2. Create venv with this command: `python -m venv .venv`
3. Activate venv with this command: `.\.venv\Scripts\activate`
4. Install requirements with this command: `pip install -r files\requirements.txt`
5. Run the program with this command: `python main.py`

## For the Client

1. Navigate into the client directory through the terminal
2. Run the command `docker build -t swh-graph-client .` to build the client container
3. `docker run -it --name swh-graph-client swh-graph-client`


## To run the contianers

### Pre-requisites
1. Naviagte into the root directory through the terminal
2. Create venv with this command: `python3 -m venv .venv`
3. Activate venv with this command: `source venv/bin/activate`
4. Install requirements with this command: `pip install -r /requirements.txt`

### Server
1. Navigate into the root directory through the terminal
2. Activate the venv like above
3. Run `python -m server.server` to build and run the server container

### Client
1. Navigate into the root directory through the terminal
2. Activate the venv like above
3. Run `python -m client.client` to build and run the client containert
4. Get access to the client container (either through docker exec or attaching the contianer to vscode)
5. Create the file `.env` in the neo4j directory fill it up with your information (see the example file `.env.example`)
#### Once the server container is up and running
6. In the data directory, either manually or through docker commands, copy the graph.nodes.csv file data into the origins.csv file
All the following python commands are run in the client container inside the CAPSTONE/client directory
7. Run `python main.py` to start the data ingestion
#### Once the data ingestion is done, you can run the following commands to create the graph database in Neo4j
8. Run `python schema.py`
9. Run `python load_csv.py`
