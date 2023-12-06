import os
from __task__ import TaskContext, TaskBuilder


def _setup(ctx: TaskContext):
    if ctx.system.distro == "debian":
        if not os.path.exists("/snap/bin/gitkraken"):
            ctx.log.info("installing")
            ctx.exec("sudo snap install --classic gitkraken")
        else:
            ctx.log.info("already installed")
    else:
        raise NotImplementedError(f"Not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def configure(builder: TaskBuilder):
    module_name = "gitkraken"
    builder.add_task(module_name, "gitkraken", _setup)
