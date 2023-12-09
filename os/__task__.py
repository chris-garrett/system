from __task__ import TaskBuilder, TaskContext


def _print_info(ctx: TaskContext):
    print(f"Platform: {ctx.system.platform}")
    print(f"Distro:   {ctx.system.distro}")
    print(f"Arch:     {ctx.system.arch}")


def configure(builder: TaskBuilder):
    module_name = "os"
    builder.add_task(module_name, "os:update", lambda ctx: ctx.exec("sudo apt update"))
    builder.add_task(module_name, "os:upgrade", lambda ctx: ctx.exec("sudo apt upgrade -y"), deps=["os:update"])
    builder.add_task(module_name, "os:info", _print_info)
