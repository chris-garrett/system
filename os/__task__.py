from __task__ import TaskBuilder, TaskContext
from os.path import expanduser


def _print_info(ctx: TaskContext):
    print(f"Platform: {ctx.system.platform}")
    print(f"Distro:   {ctx.system.distro}")
    print(f"Arch:     {ctx.system.arch}")


def _upgrade(ctx: TaskContext):
    ctx.exec("sudo apt upgrade -y")
    ctx.exec("sudo snap refresh")


def _disk_free(ctx: TaskContext):
    def _print_disk_free(location):
        ret = ctx.exec(f"sudo du -cha --max-depth=1 {location} ", quiet=True)
        for line in ret.stdout.splitlines():
            if "M" in line or "G" in line:
                print(line)

    _print_disk_free("/")
    _print_disk_free(expanduser("~"))


def configure(builder: TaskBuilder):
    module_name = "os"
    builder.add_task(module_name, "os:update", lambda ctx: ctx.exec("sudo apt update"))
    builder.add_task(module_name, "os:upgrade", _upgrade, deps=["os:update"])
    builder.add_task(module_name, "os:info", _print_info)
    builder.add_task(module_name, "os:free", _disk_free)
