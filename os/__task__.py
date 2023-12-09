from __task__ import TaskBuilder


def configure(builder: TaskBuilder):
    module_name = "os"
    builder.add_task(module_name, "os:update", lambda ctx: ctx.exec("sudo apt update"))
    builder.add_task(module_name, "os:upgrade", lambda ctx: ctx.exec("sudo apt upgrade -y"), deps=["os:update"])
