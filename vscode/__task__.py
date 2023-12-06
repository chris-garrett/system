import os
from __task__ import TaskContext, TaskBuilder


def _setup(ctx: TaskContext):
    if ctx.system.distro == "debian":
        if not os.path.exists("/snap/bin/code"):
            ctx.log.info("installing")
            ctx.exec("sudo snap install --classic code")
        else:
            ctx.log.info("already installed")
    else:
        raise NotImplementedError(f"Not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _python(ctx: TaskContext):
    ctx.exec("code --install-extension ms-python.python")
    ctx.exec("code --install-extension ms-toolsai.jupyter")
    ctx.exec("code --install-extension ms-python.black-formatter")
    ctx.exec("code --install-extension ms-python.flake8")


def _aiml(ctx: TaskContext):
    ctx.exec("code --install-extension Continue.continue")
    ctx.exec("code --install-extension GitHub.copilot")
    ctx.exec("code --install-extension GitHub.copilot-chat")
    ctx.exec("code --install-extension ms-semantic-kernel.semantic-kernel")


def _dotnet(ctx: TaskContext):
    ctx.exec("code --install-extension ms-dotnettools.csdevkit")


def configure(builder: TaskBuilder):
    module_name = "vscode"
    builder.add_task(module_name, "vscode:code", _setup)
    builder.add_task(module_name, "vscode:python", _python)
    builder.add_task(module_name, "vscode:aiml", _aiml)
    builder.add_task(module_name, "vscode:dotnet", _dotnet)
