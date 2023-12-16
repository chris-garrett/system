import os
from __task__ import TaskBuilder, TaskContext
from __system__ import snap_install, apt_install, deb_install, get_github_download_url


def _dropbox(ctx: TaskContext):
    if ctx.system.distro == "debian":
        if not os.path.exists("/usr/bin/dropbox-xl"):
            user_home = os.path.expanduser("~")
            ctx.exec(
                f"curl -o /tmp/dropbox.tar.gz -L -C - 'https://www.dropbox.com/download?plat=lnx.{ctx.system.arch}'"
            )
            ctx.exec(f"tar xvf /tmp/dropbox.tar.gz -C {user_home}")
        else:
            ctx.log.info("dropbox already installed")
    else:
        raise NotImplementedError(f"dropbox not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def configure(builder: TaskBuilder):
    module_name = "utils"
    builder.add_task(module_name, f"{module_name}:htop", lambda ctx: snap_install(ctx, "htop"))
    builder.add_task(
        module_name, f"{module_name}:flameshot", lambda ctx: apt_install(ctx, "flameshot", "/usr/bin/flameshot")
    )
    builder.add_task(module_name, f"{module_name}:curl", lambda ctx: apt_install(ctx, "curl", "/usr/bin/curl"))
    builder.add_task(
        module_name, f"{module_name}:liquidctl", lambda ctx: apt_install(ctx, "liquidctl", "/usr/bin/liquidctl")
    )
    builder.add_task(
        module_name,
        f"{module_name}:bottom",
        lambda ctx: deb_install(
            ctx, "bottom", "/usr/bin/btm", get_github_download_url("ClementTsang", "bottom", r"amd64.deb$")
        ),
    )
    builder.add_task(
        module_name, f"{module_name}:filezilla", lambda ctx: apt_install(ctx, "filezilla", "/usr/bin/filezilla")
    )
    builder.add_task(module_name, f"{module_name}:dropbox", _dropbox, deps=["utils:curl"])
