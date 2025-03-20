from controllers import get_node, traverse
from typing import Optional, Tuple, List, Set, Dict
from datetime import datetime

def get_main_or_master_revision(successors):
    """
    Filters the successors to get the revision of the main or master branch.

    Args:
        successors (List[Successor]): The list of successor nodes.

    Returns:
        Optional[str]: The swhid of the main or master revision if found, None otherwise.
    """
    for successor in successors:
        for label in successor.label:
            label_name = label.name.decode('utf-8')
            if label_name == "refs/heads/master" or label_name == "refs/heads/main":
                return successor.swhid
    return None

def collect_revisions_timestamps_and_devs_and_size(revision_ids: List[str]) -> Tuple[Set[str], List[int], int, Set[str], int, Dict[str, int], Optional[str]]:
    """ 
    Collects distinct 'rev' nodes, their timestamps, and counts the number of distinct developers by 
    traversing from the given revision IDs, and calculates the size of the repository.

    Args:
        revision_ids (List[str]): The list of revision IDs to traverse from.

    Returns:
        Tuple[Set[str], List[int], int, Set[str], int, Dict[str, int], Optional[str]]:
        - A set of distinct 'rev' nodes.
        - A list of commit timestamps.
        - The number of distinct developers.
        - The size of the repository in bytes.
        - A dictionary with the number of commits per developer.
        - An error message if an error occurs, None otherwise.
    """
    distinct_revs: Set[str] = set()
    timestamps: List[int] = []
    devs: Set[str] = set()
    total_size: int = 0
    visited_files: Dict[str, int] = {}
    commits_per_developer: Dict[str, int] = {}

    def traverse_dir(dir_id: str):
        nonlocal total_size
        cnt_nodes, error_msg = traverse([dir_id], "cnt")
        if error_msg:
            total_size = None  # Mark size calculation as failed
            return
        for cnt_node in cnt_nodes:
            if total_size is not None and cnt_node.swhid not in visited_files:
                visited_files[cnt_node.swhid] = cnt_node.cnt.length
                total_size += cnt_node.cnt.length

    for rev_id in revision_ids:
        rev_nodes, error_msg = traverse([rev_id], "rev")
        if error_msg:
            return set(), [], 0, set(), 0, {}, error_msg
        if rev_nodes:
            for node in rev_nodes:
                if node.swhid.startswith("swh:1:rev"):
                    distinct_revs.add(node.swhid)
                    if node.HasField("rev"):
                        timestamps.append(node.rev.author_date)
                        devs.add(node.rev.author)  # Add the author to the set of developers
                        if node.rev.author in commits_per_developer:
                            commits_per_developer[node.rev.author] += 1
                        else:
                            commits_per_developer[node.rev.author] = 1
    revnode, error_msg = get_node(revision_ids[0])
    if error_msg:
        return None, None, None, None, None, None, error_msg
    if revnode and revnode.successor:
        for successor in revnode.successor:
            if successor.swhid.startswith("swh:1:dir"):
                traverse_dir(successor.swhid)
            if successor.swhid.startswith("swh:1:cnt"):
                if total_size is not None and successor.swhid not in visited_files:
                    visited_files[successor.swhid] = successor.cnt.length
                    total_size += successor.cnt.length

    return len(distinct_revs), timestamps, len(devs), devs, total_size, commits_per_developer, None

def gini_index(commits_per_developer: Dict[str, int]) -> float:
    """
    Calculates the Gini index based on the number of commits per developer.

    Args:
        commits_per_developer (Dict[str, int]): A dictionary with the number of commits per developer.

    Returns:
        float: The Gini index (0 = perfect equality, 1 = maximal inequality).
    """
    n = len(commits_per_developer)
    
    if n == 0:
        return 0  # Avoid division by zero
    
    # Sort commit counts
    commits = sorted(commits_per_developer.values())
    
    # Total number of commits
    total_commits = sum(commits)
    
    if total_commits == 0:
        return 0  # Avoid division by zero
    
    # Compute Gini index using proper formula
    cumulative_sum = sum((i + 1) * commit for i, commit in enumerate(commits))
    
    gini = (2 * cumulative_sum) / (n * total_commits) - (n + 1) / n
    return gini

def get_revisions_from_latest(swhid: str) -> Tuple[Optional[int], Optional[str], Optional[int], Optional[int], Optional[int]]:
    """ 
    Fetches the latest revisions from the repository, counts the number of distinct 'rev' nodes, 
    calculates the age of the repository (difference between latest and oldest commit), 
    the number of developers, and the repository size.
    
    Args:
        swhid (str): The identifier of the repository to fetch revisions from.

    Returns:
        Tuple[Optional[int], Optional[str], Optional[int], Optional[int], Optional[int]]:
        - The count of distinct 'rev' nodes if successful, None otherwise.
        - An error message if an error occurs, None otherwise.
        - The age of the repository in seconds (latest commit timestamp - oldest commit timestamp), 
          or None if it cannot be calculated.
        - The number of distinct developers.
        - The size of the repository in bytes.
    """
    if not swhid:
        return None, None, None, None, None, None, None, None, "No swhid provided"
    if not swhid.startswith("swh:1:ori:"):
        return None, None, None, None, None, None, None, None, "Invalid swhid format"

    # Step 1: Get the origin node
    url = None
    origin_node, error_msg = get_node(swhid)
    url = origin_node.ori.url
    if error_msg:
        return None, None, None, None, None, None, None, None, error_msg
    if not origin_node:
        return None, None, None, None, None, None, None, None, "No origin node found"

    # Step 2: Get the latest snapshot node
    if not origin_node.successor:
        return None, None, None, None, None, None, None, None, "No successors found"

    snapshot_node = None
    for successor in origin_node.successor:
        if successor.swhid.startswith("swh:1:snp"):
            snapshot_id = successor.swhid
            snapshot_node, error_msg = get_node(snapshot_id)
            if error_msg:
                return None, None, None, None, None, None, None, None, error_msg
            if snapshot_node and snapshot_node.successor:
                break

    if not snapshot_node:
        return None, None, None, None, None, None, None, None, "No snapshot found"

    # Step 3: Extract the main or master revision from the snapshot
    revision_ids = []
    if origin_node.ori.url.startswith("https://github.com"):
        main_or_master_revision_id = get_main_or_master_revision(snapshot_node.successor)
        if main_or_master_revision_id:
            print(f"Main or master revision found: {main_or_master_revision_id}")
            revision_ids = [main_or_master_revision_id]
    else:
        revision_ids = [successor.swhid for successor in snapshot_node.successor if successor.swhid.startswith("swh:1:rev")]

    # Step 4: Collect distinct 'rev' nodes, timestamps, devs, and calculate repo size
    distinct_revs, timestamps, num_devs, devs, repo_size, commits_per_developer, error_msg = collect_revisions_timestamps_and_devs_and_size(revision_ids)
    if error_msg:
        return None, None, None, None, None, None, None, None, error_msg

    # Calculate the age of the repository
    if timestamps:
        latest_commit = max(timestamps)
        age = max(timestamps) - min(timestamps)
    else:
        latest_commit = None
        age = None
    
    if commits_per_developer:
        gini = gini_index(commits_per_developer)
    else:
        gini = None

    return url, distinct_revs, latest_commit, age, num_devs, devs, gini, repo_size, None


# Example usage
if __name__ == "__main__":
    # count, error, age = get_revisions_from_latest("swh:1:ori:0259ab09d7832d244383f26fab074d04bfba11cd")
    # count, error, age, devs = get_revisions_from_latest("swh:1:ori:006762b49f6052c9648a93fabcddeb68c90d2382")     # voila dashboards
    url, count, maxtime, age, devs, devset, gini, size, error = get_revisions_from_latest("swh:1:ori:018438a0237516842ca1d683f6566e66dabe0722")       # crashing repo
    if error:
        print(f"Error: {error}")
    else:
      if url is not None:
          print(f"Repository URL: {url}")
      if count is not None:
          print(f"Total number commits found: {count}")
      if maxtime is not None:
          print(f"Latest commit timestamp: {datetime.utcfromtimestamp(maxtime)}")
      if age is not None:
          print(f"Repository age: {age} seconds (≈ {age // 86400} days)")
      if devs is not None:
          print(f"Number of distinct developers: {devs}")
      if devset is not None:
          print(f"List of distinct developers: {devset}")
      if gini is not None:
          print(f"Developer Contribution Index: {gini}")
      if size is not None:
          print(f"Repository size: {size} bytes")