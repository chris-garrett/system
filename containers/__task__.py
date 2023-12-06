from __task__ import TaskBuilder, TaskContext
from __system__ import snap_install


module_name = "containers"


def _setup_docker(ctx: TaskContext):
    raise NotImplementedError("dropbox not implemented")


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:docker", _setup_docker)
