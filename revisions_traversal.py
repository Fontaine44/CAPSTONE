from controllers import get_node, traverse
from typing import Optional, Tuple

def get_revisions_from_latest(swhid: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Fetches the latest revisions from the repository and counts the number of 'rev' nodes 
    by traversing from each one.

    Args:
        swhid (str): The identifier of the repository to fetch revisions from.

    Returns:
        Tuple[Optional[int], Optional[str]]:
        - The count of 'rev' nodes if successful, None otherwise.
        - An error message if an error occurs, None otherwise.
    """
    if not swhid:
        return None, "No swhid provided"
    if not swhid.startswith("swh:1:ori:"):
        return None, "Invalid swhid format"
    
    # Step 1: Get the latest snapshot of the origin
    node, error_msg = get_node(swhid)
    print(node)
    if error_msg:
        return None, error_msg
    if not node:
        return None, "Origin not found"
    
    if not node.successor:
        return None, "No successors found"
    
    if not node.successor[0].swhid.startswith("swh:1:snp"):
        return None, "No snapshot as successor"
    
    # Step 2: Get the latest snapshot
    snapshot, error_msg = get_node(node.successor[0].swhid)
    print(snapshot)
    if error_msg:
        return None, error_msg
    if not snapshot:
        return None, "Snapshot not found"

    # Step 3: Find all revisions from the snapshot
    revision_ids = [commit.swhid for commit in snapshot.successor if commit.swhid.startswith("swh:1:rev")]

    if not revision_ids:
        return None, "No revisions found in snapshot"

    # Step 4: Traverse from each revision and count 'rev' nodes
    total_revs = 0
    for rev_id in revision_ids:
        rev_nodes, error_msg = traverse(rev_id, "rev")
        if error_msg:
            return None, error_msg
        total_revs += len(rev_nodes) if rev_nodes else 0

    return total_revs, None  # Return the total count of 'rev' nodes

# Example usage
if __name__ == "__main__":
    count, error = get_revisions_from_latest("swh:1:ori:1e3b21ea9ff1194752f71077cf8ba94b2af46556")
    if error:
        print(f"Error: {error}")
    else:
        print(f"Total number of 'rev' nodes found: {count}")
