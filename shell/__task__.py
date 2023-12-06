import os
import re
from __task__ import TaskContext, TaskBuilder

rx_alias = re.compile(r"^alias\s+(\w+)\s*=\s*(.*)$")


def _configure_bashrc(ctx: TaskContext):
    if ctx.system.platform == "linux":
        bashrc = os.path.expanduser("~/.bashrc")

        add_shell_aliases = False
        add_shell_exports = False
        if os.path.exists(bashrc):
            with open(bashrc) as f:
                contents = f.read()
                if "shell_aliases" not in contents:
                    add_shell_aliases = True
                if "shell_exports" not in contents:
                    add_shell_exports = True

        if add_shell_aliases:
            with open(bashrc, "a") as f:
                f.write("\nsource ~/.shell_aliases\n")

        if add_shell_exports:
            with open(bashrc, "a") as f:
                f.write("\nsource ~/.shell_exports\n")

    else:
        raise NotImplementedError(f"shell_aliases implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _configure_shell_aliases(ctx: TaskContext):
    if ctx.system.platform == "linux":
        shell_aliases = os.path.expanduser("~/.shell_aliases")

        aliases = {"l": "alias l='ls -laFHh'"}
        missing_aliases = {}

        if os.path.exists(shell_aliases):
            with open(shell_aliases, "r") as f:
                aliases_contents = f.read()

        # for alias in aliases_contents:

    else:
        raise NotImplementedError(f"shell_aliases implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _setup(ctx: TaskContext):
    _configure_bashrc(ctx)
    _configure_shell_aliases(ctx)


def configure(builder: TaskBuilder):
    module_name = "shell"
    builder.add_task(module_name, "shell", _setup)
