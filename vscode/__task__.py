import os
from __task__ import TaskContext, TaskBuilder


def _setup(ctx: TaskContext):
    if ctx.system.distro == "debian":
        if not os.path.exists("/usr/bin/code"):
            ctx.log.info("installing")
            ctx.exec("sudo apt update")
            ctx.exec("sudo apt install software-properties-common apt-transport-https wget")
            ctx.exec("wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -")
            ctx.exec(
                'sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"'
            )
            ctx.exec("sudo apt install -y code")
        else:
            ctx.log.info("already installed")
    else:
        raise NotImplementedError(f"Not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def configure(builder: TaskBuilder):
    module_name = "vscode"
    builder.add_task(module_name, "vscode", _setup)
