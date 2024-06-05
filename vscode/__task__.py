import os
from __task__ import TaskContext, TaskBuilder
from __system__ import get_github_download_url, deb_install


def _python(ctx: TaskContext):
    ctx.exec("codium --install-extension ms-python.python")
    ctx.exec("codium --install-extension ms-toolsai.jupyter")
    ctx.exec("codium --install-extension ms-python.black-formatter")
    ctx.exec("codium --install-extension ms-python.flake8")


def _aiml(ctx: TaskContext):
    ctx.exec("codium --install-extension Continue.continue")
    ctx.exec("codium --install-extension GitHub.copilot")
    ctx.exec("codium --install-extension GitHub.copilot-chat")
    ctx.exec("codium --install-extension ms-semantic-kernel.semantic-kernel")


def _dotnet(ctx: TaskContext):
    ctx.exec("codium --install-extension ms-dotnettools.csdevkit")


def _containers(ctx: TaskContext):
    ctx.exec("codium --install-extension ms-azuretools.vscode-docker")
    ctx.exec("codium --install-extension ms-kubernetes-tools.vscode-kubernetes-tools")
    ctx.exec("codium --install-extension signageos.signageos-vscode-sops")


def _install_code(ctx: TaskContext):
    tool = "codium"
    if ctx.system.arch == "x86_64" and "debian" in ctx.system.distro:
        if not os.path.exists("/usr/bin/codium"):
            ctx.log.info(f"installing {tool}")
            deb_url = get_github_download_url(
                ctx, "VSCodium", "vscodium", r"amd64.deb$")
            deb_install(ctx, "codium", "/usr/bin/codium", deb_url)
        else:
            ctx.log.info(f"{tool} already installed")
    else:
        raise NotImplementedError(
            f"Not implemented on platform: {ctx.system.platform}:{
                ctx.system.distro}:{ctx.system.arch}"
        )


def _install_ms_code(ctx: TaskContext):
    if ctx.system.arch == "x86_64" and "debian" in ctx.system.distro:
        if not os.path.exists("/usr/bin/code"):
            ctx.log.info("installing")
            ctx.exec("sudo apt update")
            ctx.exec(
                "sudo apt install software-properties-common apt-transport-https wget")
            ctx.exec(
                "wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -")
            ctx.exec(
                'sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"'
            )
            ctx.exec("sudo apt install -y code")
        else:
            ctx.log.info("already installed")
    else:
        raise NotImplementedError(f"Not implemented on platform: {
                                  ctx.system.platform}:{ctx.system.distro}")


def noop(ctx: TaskContext):
    pass


def configure(builder: TaskBuilder):
    module_name = "vscode"
    builder.add_task(module_name, "vscode:all", noop, deps=[
        "vscode:install", "vscode:python", "vscode:aiml", "vscode:dotnet", "vscode:containers"])
    builder.add_task(module_name, "vscode:install", _install_code)
    builder.add_task(module_name, "vscode:python", _python)
    builder.add_task(module_name, "vscode:aiml", _aiml)
    builder.add_task(module_name, "vscode:dotnet", _dotnet)
    builder.add_task(module_name, "vscode:containers", _containers)
