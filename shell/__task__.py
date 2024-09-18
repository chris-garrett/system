import os
import re
from textwrap import dedent

from __tasklib__ import TaskBuilder, TaskContext

rx_alias = re.compile(r"^alias\s+(\w+)\s*=\s*(.*)$")


def _configure_bashrc(ctx: TaskContext):
    if ctx.system.platform == "linux" or ctx.system.platform == "darwin":
        rc_name = ".bashrc" if ctx.system.platform == "linux" else ".zshrc"
        bashrc = os.path.expanduser(f"~/{rc_name}")
        shelld = os.path.expanduser("~/.shell.d")
        ctx.log.info(f"updating {bashrc} with shell.d")

        add_shelld = False
        if os.path.exists(bashrc):
            with open(bashrc) as f:
                contents = f.read()
                if "shell.d" not in contents:
                    add_shelld = True

        if add_shelld:
            ctx.log.info(f"shell.d: updating {rc_name}")

            with open(bashrc, "a") as f:
                f.write(
                    """
# Source all scripts in ~/.shell.d
if [ -d "$HOME/.shell.d" ]; then
  for file in "$HOME/.shell.d/"*; do
    if [ -f "$file" ]; then
      source "$file"
    fi
  done
fi
"""
                )
        else:
            ctx.log.info(f"shell.d: {rc_name} already updated")

        if not os.path.exists(shelld):
            ctx.log.info("shell.d: creating directory")
            os.makedirs(shelld, exist_ok=True)

    else:
        raise NotImplementedError(f".bashrc not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _configure_shell_aliases(ctx: TaskContext):
    if ctx.system.platform == "linux" or ctx.system.platform == "darwin":
        shell_aliases = os.path.expanduser("~/.shell.d/aliases")

        aliases = {
            "l": "alias l='ls -laFHh'",
            "d": "alias d='docker'",
            "dc": "alias dc='docker-compose'",
            "dclean": "alias dclean='docker rm -v $(docker ps -a -q -f status=exited) ; docker rmi $(docker images -f \"dangling=true\" -q)'",
            "dps": "alias dps='docker ps --format \"table {{.ID}}    {{.Names}}      {{.Status}}     {{.Image}}\"'",
            "k": "alias k='kubectl'",
            "code": "alias code='codium'",
            "ca": "alias ca='conda activate py312'",
            "vi": "alias vi='nvim'",
        }

        aliases_contents = ""
        if os.path.exists(shell_aliases):
            with open(shell_aliases, "r") as f:
                aliases_contents = f.read()

        rx_alias = re.compile(r"alias\s+(\w+)\s*=\s*['\"]?(.*?)['\"]?\s*$")
        for alias in aliases_contents.splitlines():
            match = rx_alias.match(alias.strip())
            if match:
                name, value = match.groups()
                if name.strip() in aliases:
                    del aliases[name.strip()]

        with open(shell_aliases, "a") as f:
            for name, value in aliases.items():
                f.write(f"{value}\n")

    else:
        raise NotImplementedError(f"shell_aliases implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _configure_bin(ctx: TaskContext):
    if ctx.system.platform == "linux" or ctx.system.platform == "darwin":
        shell_dir = os.path.expanduser("~/bin")
        shell_file = os.path.expanduser("~/.shell.d/bin")

        os.makedirs(shell_dir, exist_ok=True)
        with open(shell_file, "w") as f:
            f.write("export PATH=~/bin:$PATH\n")

        if ctx.system.platform == "darwin":
            shell_file = os.path.expanduser("~/.shell.d/brew")
            os.makedirs(shell_dir, exist_ok=True)
            with open(shell_file, "w") as f:
                f.write("export PATH=/opt/homebrew/bin:/opt/homebrew/opt/coreutils/libexec/gnubin:$PATH\n")

    else:
        raise NotImplementedError( f"shell bin not implemented on platform: { ctx.system.platform}:{ctx.system.distro}")


def _configure_ssh(ctx: TaskContext):
    if ctx.system.platform == "linux" or ctx.system.platform == "darwin":
        ssh_path = os.path.expanduser("~/.ssh")
        shell_file = os.path.expanduser("~/.shell.d/ssh")
        with open(shell_file, "w") as f:
            f.write(
                dedent(
                    f"""
                eval "$(ssh-agent -s)"
                ssh-add {ssh_path}/id_ed25519
            """
                )
            )
    else:
        raise NotImplementedError( f"shell bin not implemented on platform: { ctx.system.platform}:{ctx.system.distro}")


def _setup(ctx: TaskContext):
    _configure_bashrc(ctx)
    _configure_shell_aliases(ctx)
    _configure_bin(ctx)
    _configure_ssh(ctx)


def configure(builder: TaskBuilder):
    module_name = "shell"
    builder.add_task(module_name, "os:shell", _setup)
