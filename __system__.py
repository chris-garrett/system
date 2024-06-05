import json
import os
import re
import uuid

from __task__ import TaskContext


def _ensure_curl(ctx: TaskContext):
    if not os.path.exists("/usr/bin/curl"):
        ctx.exec("sudo apt install -y curl", capture=True)


def get_shelld_dir(ctx: TaskContext):
    return os.path.abspath(os.path.expanduser("~/.shell.d"))


def get_tmp_dir(ctx: TaskContext):
    return os.path.abspath(os.path.join(ctx.root_dir, "tmp"))


def install_msi(ctx: TaskContext, file_path):
    return ctx.exec(f"msiexec /i '{file_path}'")
    # TODO: figure out how to do this unattended.
    return ctx.exec(f"msiexec /i '{file_path}' /quiet /passive /qn /norestart")


def download_to_tmp(ctx: TaskContext, url, name, force_redownload=False):
    _ensure_curl(ctx)

    tmp_dir = get_tmp_dir(ctx)

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir, exist_ok=True)

    fname = name if name else uuid.uuid4()
    fname_path = os.path.join(tmp_dir, fname)

    # dont download if it already exists
    if os.path.exists(fname_path) and not force_redownload:
        ctx.log.info(f"{name} already downloaded")
        return fname_path

    ctx.log.info(f"downloading {name}")
    ctx.exec(f"curl -o '{fname_path}' -L -C - '{url}'")

    return fname_path


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
            ctx.exec(f"sudo snap install {extra_repo} {app}")
        else:
            ctx.log.info(f"{app} already installed")
    else:
        raise NotImplementedError(
            f"{app} not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


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

    if "debian" in ctx.system.distro:
        if not os.path.exists(file_test):
            ctx.log.info(f"installing {app}")
            ctx.exec(f"sudo apt install -y {app}")
        else:
            ctx.log.info(f"{app} already installed")
    else:
        raise NotImplementedError(
            f"{app} not implemented on platform: {ctx.system.platform}:{ctx.system.distro}"
        )


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
    _ensure_curl(ctx)

    if "debian" in ctx.system.distro:
        if not os.path.exists(file_test):
            ctx.exec(f"curl -o /tmp/{app}.deb -L -C - '{deb_url}'")
            ctx.exec(f"sudo dpkg -i /tmp/{app}.deb")
            ctx.exec("sudo apt install -f")
        else:
            ctx.log.info(f"{app} already installed")
    else:
        raise NotImplementedError(
            f"{app} not implemented on platform: {ctx.system.platform}:{ctx.system.distro}"
        )


def get_github_release(ctx: TaskContext, org: str, repo: str) -> dict:
    """
    Retrieve the latest release data from a GitHub repository.

    This function fetches the latest release information of the specified GitHub repository
    by making an HTTP GET request to the GitHub API. It returns the JSON response as a dictionary.

    Args:
        ctx (TaskContext): The context of the task, providing system details and logging.
        org (str): The organization or user name that owns the repository.
        repo (str): The repository name.

    Returns:
        dict: A dictionary containing the latest release information.

    Examples:
        >>> ctx = TaskContext(...)
        >>> release_data = get_github_release(ctx, 'octocat', 'Hello-World')
        >>> print(release_data['tag_name'])
        'v1.0.0'

    Note:
        The GitHub API version and other headers are set in the curl command to ensure compatibility
        and proper response format.
    """
    _ensure_curl(ctx)

    url = f"https://api.github.com/repos/{org}/{repo}/releases/latest"
    ret = ctx.exec(
        f"curl --header 'Accept: application/vnd.github+json' --header 'X-GitHub-Api-Version: 2022-11-28' -L -C - '{url}'",  # noqa
        capture=True,
    )
    return json.loads(ret.stdout)


def get_github_download_url(ctx: TaskContext, org: str, repo: str, regex: str):
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

    release_json = get_github_release(ctx, org, repo)
    for asset in release_json["assets"]:
        if re.search(regex, asset["name"]):
            return asset["browser_download_url"]

    return ""


def deb_install_github(ctx: TaskContext, app: str, file_test: str, org: str, repo: str, regex: str):
    """
    Install a Debian package directly from a GitHub repository's latest release.

    This function uses the `deb_install` function to install a Debian package. It retrieves
    the download URL for the package from the latest release of the specified GitHub repository
    by matching the provided regex pattern. It then proceeds to install the package if it is
    not already installed on the system.

    Args:
        ctx (TaskContext): The task context that provides system details and logging.
        app (str): The name of the application to be installed.
        file_test (str): The path to check if the application is already installed.
        org (str): The GitHub organization or user that owns the repository.
        repo (str): The name of the repository on GitHub.
        regex (str): The regex pattern to match the name of the Debian package asset.

    Raises:
        NotImplementedError: If the system distro is not Debian.
    """
    # Retrieve the download URL for the Debian package from the GitHub repository's latest release
    deb_url = get_github_download_url(ctx, org, repo, regex)
    # Install the Debian package using the retrieved URL
    deb_install(ctx, app, file_test, deb_url)


def usr_binary_install(ctx: TaskContext, app: str, app_url: str):
    """
    Function to install a binary application.

    This function downloads a binary file from a URL and moves it to the '/usr/local/bin' directory,
    making it executable. It checks if the application is already installed before proceeding.

    Args:
        ctx (TaskContext): Context object that provides system details and logging.
        app (str): The name of the binary application to be installed.
        app_url (str): The URL from where to download the binary application.

    Raises:
        NotImplementedError: If the system platform is not Linux.
    """
    _ensure_curl(ctx)

    if ctx.system.platform == "linux":
        # Check if the binary is already installed
        if not os.path.exists(f"/usr/local/bin/{app}"):
            # Download the binary to a temporary location
            ctx.exec(f"curl -o /tmp/{app} -L -C - '{app_url}'")
            # Make the binary executable
            ctx.exec(f"chmod +x /tmp/{app}")
            # Move the binary to the '/usr/local/bin' directory
            ctx.exec(f"sudo mv /tmp/{app} /usr/local/bin/{app}")
        else:
            # Log the information that the application is already installed
            ctx.log.info(f"{app} already installed")
    else:
        # Raise an error if the platform is not Linux
        raise NotImplementedError(
            f"{app} not implemented on platform: {ctx.system.platform}:{ctx.system.distro}"
        )


def usr_binary_install_github(ctx: TaskContext, app: str, org: str, repo: str, regex: str):
    """
    Install a binary application directly from a GitHub repository's latest release.

    This function retrieves the download URL for the binary from the latest release of the
    specified GitHub repository by matching the provided regex pattern. It then proceeds to
    install the binary if it is not already installed on the system.

    Args:
        ctx (TaskContext): The task context that provides system details and logging.
        app (str): The name of the binary application to be installed.
        org (str): The GitHub organization or user that owns the repository.
        repo (str): The name of the repository on GitHub.
        regex (str): The regex pattern to match the name of the binary asset.

    Raises:
        NotImplementedError: If the system platform is not Linux.
    """
    # Retrieve the download URL for the binary from the GitHub repository's latest release
    app_url = get_github_download_url(ctx, org, repo, regex)
    # Install the binary application using the retrieved URL
    usr_binary_install(ctx, app, app_url)
