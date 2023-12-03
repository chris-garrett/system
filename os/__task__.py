import os
from __task__ import TaskContext, TaskBuilder


def _setup(ctx: TaskContext):
    ctx.log.info("Configuring git")
    if ctx.exec("git config --global user.name", quiet=True).returncode:
        ctx.exec('git config --global user.name "Chris Garrett"')
    if ctx.exec("git config --global user.email", quiet=True).returncode:
        ctx.exec('git config --global user.email "chris@nesteggs.ca"')
    if ctx.exec("git config --global push.default", quiet=True).returncode:
        ctx.exec("git config --global push.default current")

    if ctx.system.distro == "debian":
        if not os.path.exists("/usr/bin/git-lfs"):
            ctx.exec("sudo apt install -y git-lfs")
    else:
        raise NotImplementedError(f"Not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def configure(builder: TaskBuilder):
    module_name = "git"
    builder.add_task(module_name, "git", _setup)
