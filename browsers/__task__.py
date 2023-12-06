import os
from __task__ import TaskContext, TaskBuilder
from __system__ import snap_install, apt_install

module_name = "browsers"


def _edge(ctx: TaskContext):
    if ctx.system.distro == "debian":
        if not os.path.exists("/usr/bin/microsoft-edge-stable"):
            ctx.exec("curl -o /tmp/msedge.deb -L -C - 'https://go.microsoft.com/fwlink?linkid=2149051&brand=M102'")
            ctx.exec("sudo dpkg -i /tmp/msedge.deb")
            ctx.exec("sudo apt install -f")
        else:
            ctx.log.info("edge already installed")
    else:
        raise NotImplementedError(f"edge not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def configure(builder: TaskBuilder):
    builder.add_task(
        module_name,
        f"{module_name}:all",
        lambda ctx: None,
        deps=[f"{module_name}:brave", f"{module_name}:chrome", f"{module_name}:edge"],
    )
    builder.add_task(module_name, f"{module_name}:brave", lambda ctx: snap_install(ctx, "brave"))
    builder.add_task(module_name, f"{module_name}:chrome", lambda ctx: snap_install(ctx, "chromium"))
    builder.add_task(module_name, f"{module_name}:edge", _edge)
