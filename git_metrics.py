from revisions_traversal import get_revisions_from_latest

def get_metrics_for_git_repos(swhid):
    """
    Fetches metrics for a git repository.

    Args:
        swhid (str): The Software Heritage identifier of the repository.

    Returns:
        Dict[str, Union[str, int]]:
        - The metrics for the repository.
    """
    # Placeholder function
    commits, error, age, devs = get_revisions_from_latest(swhid)
    if error:
        return {"error": error}
    return {"commits": commits, "age": age, "devs": devs}
    