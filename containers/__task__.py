import os
import re
from __task__ import TaskBuilder, TaskContext
from __system__ import (
    get_github_release,
    usr_binary_install,
    usr_binary_install_github,
)

module_name = "containers"


def _setup_docker(ctx: TaskContext):
    if "debian" in ctx.system.distro:
        if not os.path.exists("/usr/local/bin/docker"):
            ctx.exec("sudo apt update")
            ctx.exec("sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release")
            ctx.exec("sudo install -m 0755 -d /etc/apt/keyrings")

            gpg = ctx.exec("curl -fsSL https://download.docker.com/linux/ubuntu/gpg", capture=True).stdout
            ctx.exec("sudo gpg --batch --yes --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg", input=gpg)

            arch = ctx.exec("dpkg --print-architecture", capture=True).stdout.strip()
            lsb = ctx.exec("lsb_release -cs", capture=True).stdout.strip()
            source_entry = f"deb [arch={arch} signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu {lsb} stable"
            with open("/tmp/docker.list", "w") as f:
                f.write(source_entry)
            ctx.exec("sudo mv /tmp/docker.list /etc/apt/sources.list.d/docker.list")

            ctx.exec("sudo apt update")
            ctx.exec(
                "sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
            )
            who = ctx.exec("whoami", capture=True).stdout.strip()
            ctx.exec(f"sudo usermod -aG docker {who}")
        else:
            ctx.log.info("docker already installed")

    else:
        raise NotImplementedError("docker not implemented")


def _kubectl(ctx: TaskContext):
    if "debian" in ctx.system.distro:
        if not os.path.exists("/usr/local/bin/kubectl"):
            version = ctx.exec("curl -L -s https://dl.k8s.io/release/stable.txt", capture=True).stdout
            usr_binary_install(ctx, "kubectl", f"https://dl.k8s.io/release/{version}/bin/linux/amd64/kubectl")
        else:
            ctx.log.info("kubectl already installed")

    else:
        raise NotImplementedError("kubectl not implemented")


def _helm(ctx: TaskContext):
    """
    Helm doesnt use assets in GH releases for binaries. Links are buried in the description of the release.
    """
    if "debian" in ctx.system.distro:
        if not os.path.exists("/usr/local/bin/helm"):
            release = get_github_release(ctx, "helm", "helm")
            matches = re.search(r"\[Linux amd64\]\((.*.gz)\)", release["body"])
            print(f"Matches: {matches.groups()[0]}")

            ctx.exec("mkdir -p /tmp/helm")
            ctx.exec(f"curl -o /tmp/helm/helm.tar.gz -L -C - '{matches.groups()[0]}'")
            ctx.exec("tar xvf /tmp/helm/helm.tar.gz -C /tmp/helm linux-amd64/helm")
            ctx.exec("chmod +x /tmp/helm/linux-amd64/helm")
            ctx.exec("sudo mv /tmp/helm/linux-amd64/helm /usr/local/bin/helm")
        else:
            ctx.log.info("kubectl already installed")


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:docker", _setup_docker)
    builder.add_task(module_name, f"{module_name}:kubectl", _kubectl)
    builder.add_task(
        module_name,
        f"{module_name}:k0s",
        lambda ctx: usr_binary_install_github(ctx, "k0s", "k0sproject", "k0s", r"k0s-v.*amd64"),
    )
    builder.add_task(module_name, f"{module_name}:helm", _helm)
