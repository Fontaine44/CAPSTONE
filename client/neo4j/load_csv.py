import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from rdflib import RDF, RDFS, XSD, Graph, Literal, Namespace, URIRef
from rdflib_neo4j import HANDLE_VOCAB_URI_STRATEGY, Neo4jStore, Neo4jStoreConfig


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

    # Define namespace
    EX = Namespace("http://example.org/schema#")

    # Read the CSV file and create RDF triples
    csv_file_path = "data/metrics.csv"
    with open(csv_file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Create a unique URI for the repository and source
            repo_uri = URIRef(EX[row["swhid"]])
            source_uri = URIRef(EX[row["source"]])
            
            # Add the repository
            neo4j_aura.add((repo_uri, RDF.type, EX.Repository))

            # Add the source
            neo4j_aura.add((source_uri, RDF.type, EX.Source))
            neo4j_aura.add((source_uri, RDFS.label, Literal(row["source"], datatype=XSD.string)))

            # Add repository properties
            neo4j_aura.add((repo_uri, EX.swhid, Literal(row["swhid"], datatype=XSD.string)))
            neo4j_aura.add((repo_uri, EX.url, Literal(row["url"], datatype=XSD.string)))
            neo4j_aura.add((repo_uri, EX.commits, Literal(row["commits"], datatype=XSD.integer)))
            neo4j_aura.add((repo_uri, EX.age, Literal(row["age"], datatype=XSD.integer)))
            neo4j_aura.add((repo_uri, EX.developers, Literal(row["devCount"], datatype=XSD.integer)))
            neo4j_aura.add((repo_uri, EX.size, Literal(row["size"], datatype=XSD.integer)))
            neo4j_aura.add((repo_uri, EX.cIndex, Literal(f"{float(row['c-index']):.4f}", datatype=XSD.float)))

            last_updated_date = datetime.strptime(row["latest_commit"], "%Y-%m-%d %H:%M:%S").date()
            neo4j_aura.add((repo_uri, EX.lastUpdated, Literal(last_updated_date.isoformat(), datatype=XSD.date)))

            # Link repository to its source
            neo4j_aura.add((repo_uri, EX.hostedOn, source_uri))

            # Process developers
            devs = row["devs"].split(";")
            for dev_hash in devs:
                # Create a unique URI for the developer
                dev_uri = URIRef(EX[dev_hash])

                # Add developer as an instance of ex:Dev
                neo4j_aura.add((dev_uri, RDF.type, EX.Dev))

                # Add developer hash property
                neo4j_aura.add((dev_uri, EX.hash, Literal(dev_hash, datatype=XSD.string)))

                # Link developer to repository
                neo4j_aura.add((dev_uri, EX.contributedTo, repo_uri))
                neo4j_aura.add((repo_uri, EX.hasContributor, dev_uri))

                # Link developer to source
                neo4j_aura.add((dev_uri, EX.contributesToSource, source_uri))

    neo4j_aura.close(True)

if __name__ == "__main__":
    if not load_dotenv():
        print("Error: .env file not found.")
        exit(1)

    main()