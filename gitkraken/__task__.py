from __task__ import TaskContext, TaskBuilder


def _update(ctx: TaskContext):
    ctx.log.info("Updating OS")
    if ctx.system.distro == "debian":
        ctx.exec("sudo apt update")
    else:
        raise NotImplementedError(f"Not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _upgrade(ctx: TaskContext):
    ctx.log.info("Grading OS")
    if ctx.system.distro == "debian":
        ctx.exec("sudo apt upgrade -y")
        ctx.exec("sudo snap refresh")
    else:
        raise NotImplementedError(f"Not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def configure(builder: TaskBuilder):
    module_name = "os"
    builder.add_task(module_name, "os:update", _update)
    builder.add_task(module_name, "os:upgrade", _upgrade, deps=["os:update"])
