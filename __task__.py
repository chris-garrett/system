from __tasklib__ import TaskBuilder, TaskContext
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
        ret = ctx.exec(f"sudo du -cha --max-depth=1 {location} ", capture=True)
        for line in ret.stdout.splitlines():
            if "M" in line or "G" in line:
                print(line)

    _print_disk_free("/")
    _print_disk_free(expanduser("~"))


def configure(builder: TaskBuilder):
    module_name = "root"
    builder.add_task(module_name, "guest:all",
                     lambda ctx: True, deps=[
                        "os:upgrade",
                        "os:shell",
                        # util things
                        "util:curl",
                        "util:xz",
                        "util:bottom",
                        "util:flameshot",
                        "util:watchexec",
                        # vim things
                        "vi:all",
                        # dev things
                        "dev:git:config",
                        "dev:git:lfs"
                        "dev:build-essential",
                        "dev:dotnet:8",
                        "dev:gitkraken",
                        "dev:meld",
                        "dev:node",
                        "dev:dbeaver",
                        "dev:lazygit",
                        "dev:toolbox",
                        "vscode:all"
                        # browsers
                        "browsers:all",
                        # comms tools
                        "comms:all",
                     ])
