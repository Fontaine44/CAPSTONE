from controllers import get_node, traverse
from typing import Optional, Tuple, List, Set
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

def collect_revisions_and_timestamps(revision_ids: List[str]) -> Tuple[Set[str], List[int], Optional[str]]:
    """
    Collects distinct 'rev' nodes and their timestamps by traversing from the given revision IDs.

    Args:
        revision_ids (List[str]): The list of revision IDs to traverse from.

    Returns:
        Tuple[Set[str], List[int], Optional[str]]:
        - A set of distinct 'rev' nodes.
        - A list of commit timestamps.
        - An error message if an error occurs, None otherwise.
    """
    distinct_revs: Set[str] = set()
    timestamps: List[int] = []

    for rev_id in revision_ids:
        print(rev_id)
        rev_nodes, error_msg = traverse([rev_id], "rev")
        if error_msg:
            return set(), [], error_msg
        if rev_nodes:
            for node in rev_nodes:
                if node.swhid.startswith("swh:1:rev"):
                    distinct_revs.add(node.swhid)
                    if node.HasField("rev"):
                        timestamps.append(node.rev.author_date)

    return distinct_revs, timestamps, None

def get_revisions_from_latest(swhid: str) -> Tuple[Optional[int], Optional[str], Optional[int]]:
    """
    Fetches the latest revisions from the repository, counts the number of distinct 'rev' nodes,
    and calculates the age of the repository (difference between latest and oldest commit).

    Args:
        swhid (str): The identifier of the repository to fetch revisions from.

    Returns:
        Tuple[Optional[int], Optional[str], Optional[int]]:
        - The count of distinct 'rev' nodes if successful, None otherwise.
        - An error message if an error occurs, None otherwise.
        - The age of the repository in seconds (latest commit timestamp - oldest commit timestamp),
          or None if it cannot be calculated.
    """
    if not swhid:
        return None, "No swhid provided", None
    if not swhid.startswith("swh:1:ori:"):
        return None, "Invalid swhid format. Expected 'swh:1:ori:...'", None
    
    # Step 1: Get the origin node
    origin_node, error_msg = get_node(swhid)
    if error_msg:
        return None, error_msg, None
    if not origin_node:
        return None, "Origin not found", None

    # Step 2: Get the latest snapshot node
    if not origin_node.successor:
        return None, "No successors found for the origin", None
    
    snapshot_node = None
    for successor in reversed(origin_node.successor):
        if successor.swhid.startswith("swh:1:snp"):
            snapshot_id = successor.swhid
            snapshot_node, error_msg = get_node(snapshot_id)
            if error_msg:
                return None, error_msg, None
            if snapshot_node:
                break

    if not snapshot_node:
        return None, "No snapshot found as successor", None
    
    print(snapshot_node)
    if error_msg:
        return None, error_msg, None
    if not snapshot_node:
        return None, "Snapshot not found", None

       # Step 3: Extract the main or master revision from the snapshot
    main_or_master_revision_id = get_main_or_master_revision(snapshot_node.successor)
    if main_or_master_revision_id:
        revision_ids = [main_or_master_revision_id]
    else:
        print("No main or master branch found") 
        # If no main or master branch, use all revision successors
        revision_ids = [successor.swhid for successor in snapshot_node.successor if successor.swhid.startswith("swh:1:rev")]

    # Step 4: Collect distinct 'rev' nodes and their timestamps
    distinct_revs, timestamps, error_msg = collect_revisions_and_timestamps(revision_ids)
    if error_msg:
        return None, error_msg, None

    if not distinct_revs:
        return None, "No distinct revisions found", None

    # Calculate the age of the repository
    if timestamps:
        age = max(timestamps) - min(timestamps)
    else:
        age = None

    return len(distinct_revs), None, age

# Example usage
if __name__ == "__main__":
    count, error, age = get_revisions_from_latest("swh:1:ori:0259ab09d7832d244383f26fab074d04bfba11cd")
    if error:
        print(f"Error: {error}")
    else:
        print(f"Total number of distinct 'rev' nodes found: {count}")
        if age is not None:
            print(f"Repository age: {age} seconds (≈ {age // 86400} days)")