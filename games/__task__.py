from __task__ import TaskContext, TaskBuilder
from __system__ import snap_install, apt_install


def _protontricks(ctx: TaskContext):
    if ctx.exec("pip --version").returncode:
        print(f"distro {ctx.system.distro}")
        if ctx.system.distro == "debian":
            ctx.exec("sudo apt install -y python3-pip")
            ctx.exec("sudo snap install --edge yad")
            ctx.exec("pip install protontricks")


def configure(builder: TaskBuilder):
    module_name = "games"
    builder.add_task(module_name, "games:steam", lambda ctx: snap_install(ctx, "steam"))
    builder.add_task(module_name, "games:lutris", lambda ctx: apt_install(ctx, "lutris", "/usr/games/lutris"))
    builder.add_task(module_name, "games:protontricks", _protontricks)
