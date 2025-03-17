from get_metrics import get_metrics_for_git_repos, get_metrics_for_pypi_repos, get_general_metrics
import csv
import time
import logging

INPUT_FILE = "data/full_origins.csv"
OUTPUT_FILE = "data/metrics.csv"
LOG_FILE = "data/output_log.txt"
AGE_FACTOR = 86400

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
                git_metrics = get_metrics_for_git_repos(origin_swhid)
                if 'error' in git_metrics:
                    logging.error(f"Error: {git_metrics['error']} with repo: {origin_swhid}")
                    continue
                metrics[origin_swhid] = git_metrics
            elif 'pypi' in url:
                logging.info(f"Processing PyPI repository: {origin_swhid}")
                pypi_metrics = get_metrics_for_pypi_repos(origin_swhid)
                if 'error' in pypi_metrics:
                    logging.error(f"Error: {pypi_metrics['error']} with repo: {origin_swhid}")
                    continue
                metrics[origin_swhid] = pypi_metrics
            else:
                logging.info(f"Processing general repository: {origin_swhid}")
                metrics[origin_swhid] = general_metrics

            # time.sleep(0.1)

    # Write metrics to output file
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["swhid", "url", "commits", "latest_commit", "age", "devCount", "devs", "c-index", "size"])
        for swhid, metric in metrics.items():
            writer.writerow([
                swhid,
                metric["url"],
                metric["commits"],
                metric["latest_commit"],
                metric["age"] // AGE_FACTOR,
                metric["devCount"],
                ";".join(metric["devs"]),
                metric.get["c-index"],  # Include C-index if available
                metric["size"]
            ])       

if __name__ == "__main__":
    start_time = time.time()
    get_metrics(INPUT_FILE, OUTPUT_FILE)
    logging.info(f"Time taken: {time.time() - start_time} seconds")