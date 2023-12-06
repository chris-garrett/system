from __task__ import TaskBuilder, TaskContext
from __system__ import snap_install


def _setup(ctx: TaskContext):
    raise NotImplementedError("dropbox not implemented")


def configure(builder: TaskBuilder):
    module_name = "dropbox"
    builder.add_task(module_name, "dropbox", _setup)
