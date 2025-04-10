from helpers.get_metrics import get_metrics_for_git_repos, get_metrics_for_pypi_repos, get_general_metrics
from helpers.controllers import get_node
from datetime import datetime
import csv
import time
import logging

INPUT_FILE = "data/full_origins.csv"
INPUT_FILE_TEST = "data/origins.csv"
OUTPUT_FILE = "data/metrics.csv"
OUTPUT_FILE_TEST = "data/partial_metrics.csv"
LOG_FILE = "data/output_log.txt"
AGE_FACTOR = 86400

with open(LOG_FILE, "w") as f:
    f.write("")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(LOG_FILE),
    logging.StreamHandler()
])

def get_metrics(input_file, output_file):
    metrics = {}
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            origin_swhid = row[0]

            if not origin_swhid.startswith("swh:1:ori:"):
                logging.error(f"Invalid swhid format: {origin_swhid}")
                continue

            node, err = get_node(origin_swhid)
            if err:
                logging.error(f"Error: {err} with repo: {origin_swhid}")
                continue

            url = node.ori.url

            if 'github' in url or 'gitlab' in url or 'bitbucket' in url:
                logging.info(f"Processing Git repository: {origin_swhid}")
                try:
                    git_metrics = get_metrics_for_git_repos(origin_swhid)
                except Exception as e:
                    logging.error(f"Error: {e} with repo: {origin_swhid}")
                    continue
                finally:
                    if 'error' in git_metrics:
                        logging.error(f"Error: {git_metrics['error']} with repo: {origin_swhid}")
                        continue
                    metrics[origin_swhid] = git_metrics
            elif 'pypi' in url:
                logging.info(f"Processing PyPI repository: {origin_swhid}")
                try:
                    pypi_metrics = get_metrics_for_pypi_repos(origin_swhid)
                except Exception as e:
                    logging.error(f"Error: {e} with repo: {origin_swhid}")
                    continue
                finally:
                    if 'error' in pypi_metrics:
                        logging.error(f"Error: {pypi_metrics['error']} with repo: {origin_swhid}")
                        continue
                    metrics[origin_swhid] = pypi_metrics
            else:
                logging.info(f"Processing general repository: {origin_swhid}")
                try:
                    other_metrics = get_general_metrics(origin_swhid)
                except Exception as e:
                    logging.error(f"Error: {e} with repo: {origin_swhid}")
                    continue
                finally:
                    if 'error' in other_metrics:
                        logging.error(f"Error: {other_metrics['error']} with repo: {origin_swhid}")
                        continue
                    metrics[origin_swhid] = other_metrics

            # time.sleep(0.1)

    # Write metrics to output file
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["swhid", "url", "commits", "latest_commit", "age", "devCount", "devs", "c-index", "size", "source"])
        for swhid, metric in metrics.items():
            writer.writerow([
                swhid,
                metric["url"],
                metric["commits"],
                datetime.utcfromtimestamp(metric["latest_commit"]).strftime('%Y-%m-%d %H:%M:%S'),
                metric["age"] // AGE_FACTOR,
                metric["devCount"],
                ";".join(metric["devs"]),
                metric["c-index"] if "c-index" in metric else "",  # Include C-index if available
                metric["size"],
                metric["source"]
            ])       

if __name__ == "__main__":
    start_time = time.time()
    get_metrics(INPUT_FILE, OUTPUT_FILE)
    # get_metrics(INPUT_FILE_TEST, OUTPUT_FILE_TEST)
    logging.info(f"Time taken: {time.time() - start_time} seconds")