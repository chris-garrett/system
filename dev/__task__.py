from __task__ import TaskBuilder
from __system__ import snap_install, apt_install

module_name = "dev"


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:meld", lambda ctx: apt_install(ctx, "meld", "/usr/bin/meld"))
