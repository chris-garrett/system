from __task__ import TaskBuilder
from __system__ import snap_install, deb_install

module_name = "browsers"


def configure(builder: TaskBuilder):
    builder.add_task(
        module_name,
        f"{module_name}:all",
        lambda ctx: None,
        deps=[f"{module_name}:brave", f"{module_name}:chrome", f"{module_name}:edge"],
    )
    builder.add_task(module_name, f"{module_name}:brave", lambda ctx: snap_install(ctx, "brave"))
    builder.add_task(module_name, f"{module_name}:chrome", lambda ctx: snap_install(ctx, "chromium"))
    builder.add_task(
        module_name,
        f"{module_name}:edge",
        lambda ctx: deb_install(
            ctx, "edge", "/usr/bin/microsoft-edge-stable", "https://go.microsoft.com/fwlink?linkid=2149051&brand=M102"
        ),
        deps=["utils:curl"],
    )
