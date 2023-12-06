from __task__ import TaskBuilder
from __system__ import snap_install, apt_install


def configure(builder: TaskBuilder):
    module_name = "utils"
    builder.add_task(module_name, f"{module_name}:htop", lambda ctx: snap_install(ctx, "htop"))
    builder.add_task(
        module_name, f"{module_name}:flameshot", lambda ctx: apt_install(ctx, "flameshot", "/usr/bin/flameshot")
    )
    builder.add_task(module_name, f"{module_name}:curl", lambda ctx: apt_install(ctx, "curl", "/usr/bin/curl"))
    builder.add_task(
        module_name, f"{module_name}:filezilla", lambda ctx: apt_install(ctx, "filezilla", "/usr/bin/filezilla")
    )
