from controllers import get_node, traverse
from typing import Optional, Tuple, List, Set
from datetime import datetime

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
    
    # Step 2: Get the latest snapshot from the origin
    if not origin_node.successor:
        return None, "No successors found for the origin", None
    
    # Check if the first successor is a snapshot
    if not origin_node.successor[0].swhid.startswith("swh:1:snp"):
        return None, "No snapshot as successor", None
    
    snapshot_id = origin_node.successor[0].swhid
    snapshot_node, error_msg = get_node(snapshot_id)
    if error_msg:
        return None, error_msg, None
    if not snapshot_node:
        return None, "Snapshot not found", None

    # Step 3: Extract all revisions from the snapshot
    revision_ids = [commit.swhid for commit in snapshot_node.successor if commit.swhid.startswith("swh:1:rev")]
    if not revision_ids:
        return None, "No revisions found in snapshot", None

    # Step 4: Traverse from each revision and collect distinct 'rev' nodes and their timestamps
    distinct_revs: Set[str] = set()  # Use a set to store distinct 'rev' nodes
    timestamps: List[int] = []  # List to store commit timestamps

    for rev_id in revision_ids:
        rev_nodes, error_msg = traverse([rev_id], "rev")
        if error_msg:
            return None, error_msg, None
        if rev_nodes:
            for node in rev_nodes:
                if node.swhid.startswith("swh:1:rev"):
                    distinct_revs.add(node.swhid)  # Add distinct 'rev' nodes to the set
                    # Get the author_date timestamp for the revision
                    if node.HasField("rev"):
                        timestamps.append(node.rev.author_date)

    # Step 5: Calculate the age of the repository
    if not timestamps:
        return len(distinct_revs), None, None  # No timestamps available

    # Find the latest and oldest commit timestamps
    latest_timestamp = max(timestamps)
    oldest_timestamp = min(timestamps)
    repo_age_seconds = latest_timestamp - oldest_timestamp

    # Step 6: Return the count of distinct 'rev' nodes and the repository age
    return len(distinct_revs), None, repo_age_seconds

# Example usage
if __name__ == "__main__":
    count, error, age = get_revisions_from_latest("swh:1:ori:006762b49f6052c9648a93fabcddeb68c90d2382")
    if error:
        print(f"Error: {error}")
    else:
        print(f"Total number of distinct 'rev' nodes found: {count}")
        if age is not None:
            print(f"Repository age: {age} seconds (≈ {age // 86400} days)")