from __task__ import TaskBuilder
from __system__ import snap_install, apt_install

module_name = "comms"


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:htop", lambda ctx: snap_install(ctx, "htop"))
    builder.add_task(
        module_name, f"{module_name}:flameshot", lambda ctx: apt_install(ctx, "flameshot", "/usr/bin/flameshot")
    )
