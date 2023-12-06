import os
from __task__ import TaskContext, TaskBuilder


def _install(ctx: TaskContext, app):
    if ctx.system.platform == "linux":
        if not os.path.exists(f"/snap/bin/{app}"):
            ctx.log.info(f"installing {app}")
            ctx.exec(f"sudo snap install {app}")
        else:
            ctx.log.info(f"{app} already installed")
    else:
        raise NotImplementedError(f"{app} not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _brave(ctx: TaskContext):
    _install(ctx, "brave")


def _all(ctx: TaskContext):
    _brave(ctx)


def configure(builder: TaskBuilder):
    module_name = "browsers"
    builder.add_task(module_name, "browsers", _all)
    builder.add_task(module_name, "browsers:brave", _brave)
