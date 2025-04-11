def get_source(url: str) -> str:
    """
    Finds the source of a software repository based on the URL.

    Args:
        url: The URL of the repository.

    Returns:
        The source of the repository (e.g., "GitHub", "PyPI"), or "Unknown" if not found.
    """

    url_lower = url.lower()  # Make the URL lowercase for case-insensitive matching

    if 'github' in url_lower:
        return 'GitHub'
    elif 'gitlab' in url_lower:
        return 'GitLab'
    elif 'bitbucket' in url_lower:
        return 'Bitbucket'
    elif 'pypi' in url_lower:
        return 'PyPI'
    elif 'debian' in url_lower:
        return 'Debian'
    elif 'ubuntu' in url_lower:
        return 'Ubuntu'
    elif 'fedora' in url_lower:
        return 'Fedora'
    elif 'maven.org' in url_lower:
        return 'Maven Central'
    elif 'nuget.org' in url_lower:
        return 'NuGet'
    elif 'crates.io' in url_lower:
        return 'crates.io'
    elif 'npmjs.com' in url_lower:
        return 'npm'
    elif 'docker.com' in url_lower or 'dockerhub' in url_lower:
        return 'Docker Hub'
    elif 'ecr.' in url_lower and 'amazonaws.com' in url_lower:
        return 'Amazon ECR'
    elif 'gcr.io' in url_lower:
        return 'Google Container Registry'
    else:
        return 'Unknown'