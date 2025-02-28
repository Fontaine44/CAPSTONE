from git_metrics import get_metrics_for_git_repos
from controllers import get_node
import csv 
import time

INPUT_FILE = "data/origins.csv"
OUTPUT_FILE = "data/metrics.csv"

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

            # if 'github' in node.ori.url or 'gitlab' in node.ori.url or 'bitbucket' in node.ori.url:
            #     print(origin_swhid, ":", node.ori.url)
            #     git_metrics = get_metrics_for_git_repos(origin_swhid)
            #     if 'error' in git_metrics:
            #         print(f"Error: {git_metrics['error']} with repo: {origin_swhid}")
            #         continue
            #     metrics[origin_swhid] = git_metrics
            
            print(origin_swhid, ":", node.ori.url)
            git_metrics = get_metrics_for_git_repos(origin_swhid)
            if 'error' in git_metrics:
                print(f"Error: {git_metrics['error']} with repo: {origin_swhid}")
                continue
            metrics[origin_swhid] = git_metrics

            time.sleep(0.5)

    # Write metrics to output file
    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["swhid", "commits", "age", "devs"])
        for swhid, metric in metrics.items():
            writer.writerow([swhid, metric["commits"], metric["age"], metric["devs"]])       
    

if __name__ == "__main__":
    get_metrics(INPUT_FILE, OUTPUT_FILE)