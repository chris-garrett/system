import os

from __system__ import (apt_install, deb_install, get_github_download_url,
                        snap_install, brew_install)
from __tasklib__ import TaskBuilder, TaskContext


def _sudoers(ctx: TaskContext):
    pass
    # "%sudo   ALL=(ALL:ALL) ALL"


def _dropbox(ctx: TaskContext):
    if "debian" in ctx.system.distro:
        if not os.path.exists("/usr/bin/dropbox-xl"):
            user_home = os.path.expanduser("~")
            ctx.exec(
                f"curl -o /tmp/dropbox.tar.gz -L -C - 'https://www.dropbox.com/download?plat=lnx.{
                    ctx.system.arch}'"
            )
            ctx.exec(f"tar xvf /tmp/dropbox.tar.gz -C {user_home}")
        else:
            ctx.log.info("dropbox already installed")
    else:
        raise NotImplementedError(
            f"dropbox not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _curl(ctx: TaskContext):
    if "debian" in ctx.system.distro:
        apt_install(ctx, "curl", "/usr/bin/curl")
    elif ctx.system.platform == "darwin":
        pass
    else:
        raise NotImplementedError(
            f"dropbox not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _install_xz(ctx: TaskContext):
    if "debian" in ctx.system.distro:
        apt_install(ctx, "xz", "/usr/bin/xz")
    elif "darwin" in ctx.system.platform:
        brew_install(ctx, "xz")
    else:
        raise NotImplementedError(
            f"xz not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def configure(builder: TaskBuilder):
    module_name = "utils"
    builder.add_task(
        module_name, f"{module_name}:htop", lambda ctx: snap_install(ctx, "htop"))
    builder.add_task(
        module_name, f"{module_name}:flameshot", lambda ctx: apt_install(
            ctx, "flameshot", "/usr/bin/flameshot")
    )
    builder.add_task(module_name, f"{module_name}:curl", _curl)
    builder.add_task(
        module_name, f"{module_name}:liquidctl", lambda ctx: apt_install(
            ctx, "liquidctl", "/usr/bin/liquidctl")
    )
    builder.add_task(
        module_name,
        f"{module_name}:bottom",
        lambda ctx: deb_install(
            ctx, "bottom", "/usr/bin/btm", get_github_download_url(
                ctx, "ClementTsang", "bottom", r"amd64.deb$")
        ),
    )
    builder.add_task(
        module_name, f"{module_name}:filezilla", lambda ctx: apt_install(
            ctx, "filezilla", "/usr/bin/filezilla")
    )
    builder.add_task(module_name, f"{module_name}:xz", _install_xz)
    builder.add_task(
        module_name, f"{module_name}:dropbox", _dropbox, deps=["utils:curl"])
    builder.add_task(
        module_name,
        f"{module_name}:watchexec",
        lambda ctx: deb_install(
            ctx,
            "watchexec",
            "/usr/bin/watchexec",
            get_github_download_url(
                ctx, "watchexec", "watchexec", r"x86_64-unknown-linux-gnu.deb$"),
        ),
    )
