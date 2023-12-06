from __task__ import TaskBuilder, TaskContext
from __system__ import snap_install, apt_install

module_name = "dev"


def _git_config(ctx: TaskContext):
    ctx.log.info("Configuring git")
    if ctx.exec("git config --global user.name", quiet=True).returncode:
        ctx.exec('git config --global user.name "Chris Garrett"')
    if ctx.exec("git config --global user.email", quiet=True).returncode:
        ctx.exec('git config --global user.email "chris@nesteggs.ca"')
    if ctx.exec("git config --global push.default", quiet=True).returncode:
        ctx.exec("git config --global push.default current")


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:meld", lambda ctx: apt_install(ctx, "meld", "/usr/bin/meld"))
    builder.add_task(module_name, f"{module_name}:postman", lambda ctx: snap_install(ctx, "postman"))
    builder.add_task(module_name, f"{module_name}:dbeaver", lambda ctx: snap_install(ctx, "dbeaver-ce"))
    builder.add_task(module_name, f"{module_name}:git:config", _git_config)
    builder.add_task(module_name, f"{module_name}:git:lfs", lambda ctx: apt_install(ctx, "git-lfs", "/usr/bin/git-lfs"))
