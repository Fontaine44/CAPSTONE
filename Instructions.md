### Pre-requisites
1. Naviagte into the root directory through the terminal.
2. Create venv with this command: `python3 -m venv .venv` # for MacOS/Linux or `python -m venv .venv` # for Windows.
3. Activate venv with this command: `source .venv/bin/activate` # for MacOS/Linux or `.venv\Scripts\activate` # for Windows.
4. Install requirements with this command: `pip install -r /requirements.txt`.

### Server
1. In the Dockerfile in the server directory, make sure to use the right dataset you want, set the ENV variable `DATASET` to the name of the dataset you want to use. The default is `2021-03-23-popular-3k-python`.
2. Navigate into the root directory through the terminal.
3. Activate the venv like above.
4. Run `python -m server.server` to build and run the server container.

### Client
1. Navigate into the root directory through the terminal.
2. Activate the venv like above.
3. Run `python -m client.client` to build and run the client container.
4. Create the file `.env` in the neo4j directory fill it up with your information (see the example file `.env.example`). You have access to vim in the container.
#### Once the server container is up and running
5. In the data directory, either manually or through docker commands, copy the `graph.nodes.csv` file data into the `origins.csv` file.
All the following python commands are run in the client container inside the CAPSTONE/client directory, normally you should already be here but double check.
6. Run `python main.py` to start the data ingestion.
#### Once the data ingestion is done, you can run the following commands to create the graph database in Neo4j
7. Run `python schema.py`.
8. Run `python load_csv.py`.
