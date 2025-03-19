from revisions_traversal import get_revisions_from_latest

def get_metrics_for_git_repos(swhid: str):
    """
    Fetches metrics for a git repository.

    Args:
        swhid (str): The Software Heritage identifier of the repository.

    Returns:
        Dict[str, Union[str, int]]:
        - The metrics for the repository.
    """
    url, commits, latest_commit, age, devCount, devs, gini, size, error = get_revisions_from_latest(swhid)
    if error:
        return {"error": error}
    return {
        "url": url,
        "commits": commits,
        "latest_commit": latest_commit,
        "age": age,
        "devCount": devCount,
        "devs": [str(x) for x in devs],  # Convert set to list
        "c-index": gini,
        "size": size
    }


def get_metrics_for_pypi_repos(swhid: str):
    """
    Fetches metrics for a PyPI repository.

    Args:
        swhid (str): The Software Heritage identifier of the repository.

    Returns:
        Dict[str, Union[str, int]]:
        - The metrics for the repository.
    """
    url, commits, latest_commit, age, devCount, devs, gini, size, error = get_revisions_from_latest(swhid)
    if error:
        return {"error": error}
    return {
        "url": url,
        "commits": commits,
        "latest_commit": latest_commit,
        "age": age,
        "devCount": devCount,
        "devs": [str(x) for x in devs],  # Convert set to list
        "c-index": gini,
        "size": size
    }

def get_general_metrics(swhid: str):
    """
    Fetches metrics for a repository.

    Args:
        swhid (str): The Software Heritage identifier of the repository.

    Returns:
        Dict[str, Union[str, int]]:
        - The metrics for the repository.
    """
    url, commits, latest_commit, age, devCount, devs, gini, size, error = get_revisions_from_latest(swhid)
    if error:
        return {"error": error}
    return {
        "url": url,
        "commits": commits,
        "latest_commit": latest_commit,
        "age": age,
        "devCount": devCount,
        "devs": [str(x) for x in devs],  # Convert set to list
        "c-index": gini,
        "size": size
    }