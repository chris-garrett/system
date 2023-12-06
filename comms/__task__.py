from __task__ import TaskBuilder
from __system__ import snap_install, apt_install

module_name = "comms"


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:slack", lambda ctx: snap_install(ctx, "slack"))
    builder.add_task(module_name, f"{module_name}:discord", lambda ctx: snap_install(ctx, "discord"))
    builder.add_task(module_name, f"{module_name}:mattermost", lambda ctx: snap_install(ctx, "mattermost-desktop"))
