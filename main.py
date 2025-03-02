from get_metrics import get_metrics_for_git_repos, get_metrics_for_pypi_repos, get_general_metrics
from controllers import get_node
import csv 
import time

INPUT_FILE = "data/full_origins.csv"
OUTPUT_FILE = "data/metrics.csv"
AGE_FACTOR = 86400

def get_metrics(input_file, output_file):
    metrics = {}
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            origin_swhid = row[0]

            if not origin_swhid.startswith("swh:1:ori:"):
                print("Invalid swhid format")
                continue

            node, err = get_node(origin_swhid)
            if err:
                print(f"Error: {err} with repo: {origin_swhid}")
                continue

            if 'github' in node.ori.url or 'gitlab' in node.ori.url or 'bitbucket' in node.ori.url:
                print(origin_swhid, ":", node.ori.url)
                git_metrics = get_metrics_for_git_repos(origin_swhid)
                if 'error' in git_metrics:
                    print(f"Error: {git_metrics['error']} with repo: {origin_swhid}")
                    continue
                git_metrics["url"] = node.ori.url
                metrics[origin_swhid] = git_metrics
            elif 'pypi' in node.ori.url:
                print(origin_swhid, ":", node.ori.url)
                pypi_metrics = get_metrics_for_pypi_repos(origin_swhid)
                if 'error' in pypi_metrics:
                    print(f"Error: {pypi_metrics['error']} with repo: {origin_swhid}")
                    continue
                pypi_metrics["url"] = node.ori.url
                metrics[origin_swhid] = pypi_metrics
            else:
                print(origin_swhid, ":", node.ori.url)
                general_metrics = get_general_metrics(origin_swhid)
                if 'error' in general_metrics:
                    print(f"Error: {general_metrics['error']} with repo: {origin_swhid}")
                    continue
                general_metrics["url"] = node.ori.url
                metrics[origin_swhid] = general_metrics

            # time.sleep(0.1)

    # Write metrics to output file
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["swhid", "url", "commits", "age", "devs"])
        for swhid, metric in metrics.items():
            writer.writerow([swhid, metric["url"], metric["commits"], metric["age"] // AGE_FACTOR, metric["devs"]])       
    

if __name__ == "__main__":
    start_time = time.time()
    get_metrics(INPUT_FILE, OUTPUT_FILE)
    print(f"Time taken: {time.time() - start_time} seconds")