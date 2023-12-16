import os
import re
import requests
from __task__ import TaskContext


def snap_install(ctx: TaskContext, app: str, classic=False, edge=False):
    """
    Function to install an application using snap package manager.

    Args:
        ctx (TaskContext): Context object that provides system details and logging.
        app (str): The name of the application to be installed.
        classic (bool, optional): Install using --classic flag. Defaults to False.
        edge (bool, optional): Install using --edge flag. Defaults to False.

    Raises:
        NotImplementedError: If the system distro is not debian.
    """

    extra_repo = ""
    if classic:
        extra_repo = "--classic"
    if edge:
        extra_repo = "--edge"

    if ctx.system.platform == "linux":
        if not os.path.exists(f"/snap/bin/{app}"):
            ctx.log.info(f"installing {app}")
            ctx.exec(f"sudo snap install {extra_repo}{app}")
        else:
            ctx.log.info(f"{app} already installed")
    else:
        raise NotImplementedError(f"{app} not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def apt_install(ctx: TaskContext, app: str, file_test: str):
    """
    Function to install an application using apt package manager.

    Args:
        ctx (TaskContext): Context object that provides system details and logging.
        app (str): The name of the application to be installed.
        file_test (str): The path to check if the application is already installed.

    Raises:
        NotImplementedError: If the system distro is not debian.
    """

    if ctx.system.distro == "debian":
        if not os.path.exists(file_test):
            ctx.log.info(f"installing {app}")
            ctx.exec(f"sudo apt install -y {app}")
        else:
            ctx.log.info(f"{app} already installed")
    else:
        raise NotImplementedError(f"{app} not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def deb_install(ctx: TaskContext, app: str, file_test: str, deb_url: str):
    """
    Function to install an application via a .deb file.

    Args:
        ctx (TaskContext): Context object that provides system details and logging.
        app (str): The name of the application to be installed.
        file_test (str): The path to check if the application is already installed.
        deb_url (str): The url to download the .deb file from.

    Raises:
        NotImplementedError: If the system distro is not debian.
    """

    if ctx.system.distro == "debian":
        if not os.path.exists(file_test):
            ctx.exec(f"curl -o /tmp/{app}.deb -L -C - '{deb_url}'")
            ctx.exec(f"sudo dpkg -i /tmp/{app}.deb")
            ctx.exec("sudo apt install -f")
        else:
            ctx.log.info(f"{app} already installed")
    else:
        raise NotImplementedError(f"{app} not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def get_github_download_url(org: str, repo: str, regex: str):
    """
    Function to get the download URL of the latest release of a GitHub repository.

    Args:
        org (str): The name of the organization that owns the repository.
        repo (str): The name of the repository.
        regex (str): The regular expression pattern to match the asset name.

    Returns:
        str: The download URL of the matched asset. If no asset matches the regex pattern, returns an empty string.

    Examples:
        >>> get_github_download_url("VSCodium", "vscodium", r"amd64.deb$")
    """
    ret = requests.get(
        f"https://api.github.com/repos/{org}/{repo}/releases/latest",
        headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"},
    )
    release_json = ret.json()

    for asset in release_json["assets"]:
        if re.search(regex, asset["name"]):
            return asset["browser_download_url"]

    return ""
