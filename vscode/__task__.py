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


def _install_codium(ctx: TaskContext):
    # TODO: add alias code -> codium
    if ctx.system.arch == "x86_64" and ctx.system.distro == "debian":
        deb_url = get_github_download_url("VSCodium", "vscodium", r"amd64.deb$")
        deb_install(ctx, "codium", "/usr/bin/codium", deb_url)
    else:
        raise NotImplementedError(
            f"Not implemented on platform: {ctx.system.platform}:{ctx.system.distro}:{ctx.system.arch}"
        )


def configure(builder: TaskBuilder):
    module_name = "vscode"
    builder.add_task(module_name, "vscode:code", _install_codium)
    builder.add_task(module_name, "vscode:python", _python)
    builder.add_task(module_name, "vscode:aiml", _aiml)
    builder.add_task(module_name, "vscode:dotnet", _dotnet)
