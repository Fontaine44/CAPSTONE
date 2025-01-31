from controllers import get_node
from collections import deque

from typing import Optional, Tuple

import swh.graph.grpc.swhgraph_pb2 as swhgraph
import swh.graph.grpc.swhgraph_pb2_grpc as swhgraph_grpc

def get_commits(swhid: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Fetches the commits of a repository

    Args:
        swhid (str): The identifier of the repository to fetch commits from

    Returns:
        Tuple[Optional[swhgraph.GetCommitsResponse], Optional[str]]:
        - The commits response if successful, None otherwise.
        - An error message if an error occurs, None otherwise.
    """
    if not swhid:
        return None, "No swhid provided"
    if not swhid.startswith("swh:1:ori:"):
        return None, "Invalid swhid format"
    
    node, error_msg = get_node(swhid)
    if error_msg:
        return None, error_msg
    if not node:
        return None, "Origin not found"
        
    # Valid node so get successors
    if not node.successor:
        return None, "No successors found"
    
    if len(node.successor) != 1 or (not node.successor[0].swhid.startswith("swh:1:snp")):
        return None, "No snapshot as successor"
    
    successor, error_msg = get_node(node.successor[0].swhid)
    if error_msg:
        return None, error_msg
    if not successor:
        return None, "Snapshot not found"
    
    queue = deque()
    for commit in successor.successor:
        if commit.swhid.startswith("swh:1:rev"):
            queue.append(commit.swhid)
    
    print(queue)

    commits = set()
    first = None
    last = None

    while queue:
        commit_id = queue.popleft()
        commit, error_msg = get_node(commit_id)

        if error_msg:
            return None, error_msg
        if not commit:
            return None, f"Commit {commit_id} not found"
        
        if not commit.successor:
            continue
        
        for successor in commit.successor:
            if successor.swhid not in commits and successor.swhid.startswith("swh:1:rev"):
                queue.append(successor.swhid)
        
        if not first:
            first = commit
        last = commit
        commits.add(commit_id)
    
    first_commit, err_one = get_node(first.swhid)
    last_commit, err_two = get_node(last.swhid)

    if err_one:
        return None, err_one
    if err_two:
        return None, err_two
    
    # Print first and last commits with date
    print(f"First commit: {first_commit.swhid} on {first_commit.rev.author_date}")
    print(f"Last commit: {last_commit.swhid} on {last_commit.rev.author_date}")
    print(f"Number of commits: {len(commits)}")

if __name__ == "__main__":
    get_commits("swh:1:ori:006762b49f6052c9648a93fabcddeb68c90d2382")