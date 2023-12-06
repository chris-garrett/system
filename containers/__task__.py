import os
from __task__ import TaskBuilder, TaskContext


module_name = "containers"


def _setup_docker(ctx: TaskContext):
    if ctx.system.distro == "debian":
        if not os.path.exists("/snap/bin/docker"):
            ctx.exec("sudo addgroup --system docker")
            ctx.exec(f"sudo adduser {os.getlogin()} docker")
            ctx.exec("sudo snap install docker")
        else:
            ctx.log.info("docker already installed")

    else:
        raise NotImplementedError("docker not implemented")


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:docker", _setup_docker)
