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

def collect_revisions_timestamps_and_devs(revision_ids: List[str]) -> Tuple[Set[str], List[int], int, Optional[str]]:
    """
    Collects distinct 'rev' nodes, their timestamps, and counts the number of distinct developers by traversing from the given revision IDs.

    Args:
        revision_ids (List[str]): The list of revision IDs to traverse from.

    Returns:
        Tuple[Set[str], List[int], int, Optional[str]]:
        - A set of distinct 'rev' nodes.
        - A list of commit timestamps.
        - The number of distinct developers.
        - An error message if an error occurs, None otherwise.
    """
    distinct_revs: Set[str] = set()
    timestamps: List[int] = []
    devs: Set[str] = set()

    for rev_id in revision_ids:
        rev_nodes, error_msg = traverse([rev_id], "rev")
        if error_msg:
            return set(), [], 0, error_msg
        if rev_nodes:
            for node in rev_nodes:
                if node.swhid.startswith("swh:1:rev"):
                    distinct_revs.add(node.swhid)
                    if node.HasField("rev"):
                        timestamps.append(node.rev.author_date)
                        devs.add(node.rev.author)  # Add the author to the set of developers

    return distinct_revs, timestamps, len(devs), None

# def get_num_of_devs(revisions):
#     """
#     Count the number of distinct developers from the revisions.

#     Args:
#         revisions (Set[str]): The set of distinct 'rev' nodes.

#     Returns:
#         Tuple[int, Optional[str]]:
#         - The number of distinct developers.
#         - An error message if an error occurs, None otherwise.
#     """
#     devs = set()
#     for rev in revisions:
#         node, error_msg = get_node(rev)
#         if error_msg:
#             return set(), error_msg
#         if node.HasField("rev"):
#             devs.add(node.rev.author) # We can change this to committer if needed
#     return len(devs), None

def get_revisions_from_latest(swhid: str) -> Tuple[Optional[int], Optional[str], Optional[int]]:
    """
    Fetches the latest revisions from the repository, counts the number of distinct 'rev' nodes, 
    calculates the age of the repository (difference between latest and oldest commit), and
    the number of developers.

    Args:
        swhid (str): The identifier of the repository to fetch revisions from.

    Returns:
        Tuple[Optional[int], Optional[str], Optional[int]]:
        - The count of distinct 'rev' nodes if successful, None otherwise.
        - An error message if an error occurs, None otherwise.
        - The age of the repository in seconds (latest commit timestamp - oldest commit timestamp),
          or None if it cannot be calculated.
        - The number of distinct developers.
    """
    if not swhid:
        return None, "No swhid provided", None
    if not swhid.startswith("swh:1:ori:"):
        return None, "Invalid swhid format. Expected 'swh:1:ori:...'", None, None
    
    # Step 1: Get the origin node
    origin_node, error_msg = get_node(swhid)
    if error_msg:
        return None, error_msg, None, None
    if not origin_node:
        return None, "Origin not found", None, None

    # Step 2: Get the latest snapshot node
    if not origin_node.successor:
        return None, "No successors found for the origin", None, None
    
    # find first snapshot
    snapshot_node = None
    for successor in origin_node.successor:
        if successor.swhid.startswith("swh:1:snp"):
            snapshot_id = successor.swhid
            snapshot_node, error_msg = get_node(snapshot_id)
            if error_msg:
                return None, error_msg, None, None
            if snapshot_node:
                break

    if not snapshot_node:
        return None, "No snapshot found as successor", None, None
    
    # print(snapshot_node)
    if error_msg:
        return None, error_msg, None
    if not snapshot_node:
        return None, "Snapshot not found", None, None

    # Step 3: Extract the main or master revision from the snapshot
    main_or_master_revision_id = get_main_or_master_revision(snapshot_node.successor)
    if main_or_master_revision_id:
        revision_ids = [main_or_master_revision_id]
    else:
        print("No main or master branch found") 
        # If no main or master branch, use all revision successors
        revision_ids = [successor.swhid for successor in snapshot_node.successor if successor.swhid.startswith("swh:1:rev")]

    # Step 4: Collect distinct 'rev' nodes and their timestamps
    distinct_revs, timestamps, num_devs, error_msg = collect_revisions_timestamps_and_devs(revision_ids)
    if error_msg:
        return None, error_msg, None, None

    if not distinct_revs:
        return None, "No distinct revisions found", None, None

    # Calculate the age of the repository
    if timestamps:
        age = max(timestamps) - min(timestamps)
    else:
        age = None

    if error_msg:
        return None, error_msg, None, None
    return len(distinct_revs), None, age, num_devs

# Example usage
if __name__ == "__main__":
    # count, error, age = get_revisions_from_latest("swh:1:ori:0259ab09d7832d244383f26fab074d04bfba11cd")
    # count, error, age, devs = get_revisions_from_latest("swh:1:ori:006762b49f6052c9648a93fabcddeb68c90d2382")     # voila dashboards
    count, error, age, devs = get_revisions_from_latest("swh:1:ori:00a082063e1572f77e21b9dedef30635e60a99e8")       # crashing repo
    if error:
        print(f"Error: {error}")
    else:
        print(f"Total number of distinct 'rev' nodes found: {count}")
        if age is not None:
            print(f"Repository age: {age} seconds (≈ {age // 86400} days)")
        if devs is not None:
            print(f"Number of distinct developers: {devs}")