import os
from dotenv import load_dotenv
from rdflib import Graph
from rdflib_neo4j import Neo4jStoreConfig, Neo4jStore, HANDLE_VOCAB_URI_STRATEGY


def main():
    # Load environment variables for authentification
    auth_data = {'uri': os.getenv("AURA_DB_URI"),
                'database': os.getenv("AURA_DB_NAME"),
                'user': os.getenv("AURA_DB_USERNAME"),
                'pwd': os.getenv("AURA_DB_PWD")}
    
    # Define store configuration
    config = Neo4jStoreConfig(auth_data=auth_data,
                            handle_vocab_uri_strategy=HANDLE_VOCAB_URI_STRATEGY.IGNORE,
                            batching=True)

    # Create the RDF Graph
    neo4j_aura = Graph(store=Neo4jStore(config=config))

    schema_path = 'neo4j/schema.ttl'

    # Parse the Turtle file and load it into Neo4j
    neo4j_aura.parse(schema_path, format="ttl")

    neo4j_aura.close(True)

if __name__ == "__main__":
    if not load_dotenv():
        print("Error: .env file not found.")
        exit(1)

    main()