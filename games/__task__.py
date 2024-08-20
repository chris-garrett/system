from __system__ import apt_install, deb_install
from __tasklib__ import TaskBuilder, TaskContext


def _protontricks(ctx: TaskContext):
    if ctx.exec("pip --version").returncode:
        print(f"distro {ctx.system.distro}")
        if "debian" in ctx.system.distro:
            ctx.exec("sudo apt install -y python3-pip")
            ctx.exec("sudo snap install --edge yad")
            ctx.exec("pip install protontricks")


def _protonup(ctx: TaskContext):
    pass
    # pip3 install protonup
    # protonup -d "~/.steam/root/compatibilitytools.d/"
    # protonup -t GE-Proton9-4


def configure(builder: TaskBuilder):
    module_name = "games"
    builder.add_task(
        module_name,
        "games:steam",
        lambda ctx: deb_install(
            ctx, "steam", "/usr/bin/steam", "https://cdn.cloudflare.steamstatic.com/client/installer/steam.deb"
        ),
    )
    builder.add_task(module_name, "games:lutris", lambda ctx: apt_install(ctx, "lutris", "/usr/games/lutris"))
    builder.add_task(
        module_name, "games:winetricks", lambda ctx: apt_install(ctx, "winetricks", "/usr/games/winetricks")
    )
    builder.add_task(module_name, "games:lutris", lambda ctx: apt_install(ctx, "lutris", "/usr/games/lutris"))
    builder.add_task(module_name, "games:protontricks", _protontricks)
