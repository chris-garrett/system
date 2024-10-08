import os
import shutil
from textwrap import dedent

from __system__ import (apt_install, brew_install, download_to_tmp, brew_install,
                        get_shelld_dir, get_tmp_dir, snap_install)
from __tasklib__ import TaskBuilder, TaskContext

module_name = "dev"


def _git_config(ctx: TaskContext):
    ctx.log.info("Configuring git")
    if ctx.exec("git config --global user.name", capture=True).returncode:
        ctx.exec('git config --global user.name "Chris Garrett"')
    if ctx.exec("git config --global user.email", capture=True).returncode:
        ctx.exec('git config --global user.email "chris@nesteggs.ca"')
    if ctx.exec("git config --global push.default", capture=True).returncode:
        ctx.exec("git config --global push.default current")


def _dotnet_installer(ctx: TaskContext, version: str):
    if ctx.system.platform == "linux" or ctx.system.platform == "darwin":
        dotnet = os.path.expanduser("~/.dotnet/dotnet")
        installer_file = "/tmp/dotnet-install.sh"

        if not os.path.exists(installer_file):
            ctx.exec(
                f"curl -L -o {installer_file} https://dot.net/v1/dotnet-install.sh")

        if os.path.exists(dotnet):
            ret = ctx.exec(f"{dotnet} --list-sdks", capture=True)
            if ret.returncode != 0:
                raise Exception(f"Failed to list dotnet sdks: {ret.stderr}")

            found = len([x for x in ret.stdout.splitlines()
                        if x.startswith(version)])
        else:
            found = False

        # recreate shell init:
        dotnet_shelld = os.path.join(get_shelld_dir(ctx), "dotnet")
        with open(dotnet_shelld, "w") as f:
            f.write(
                dedent(
                    """
                export DOTNET_CLI_TELEMETRY_OPTOUT=1
                export DOTNET_ROOT=~/.dotnet
                export PATH=$DOTNET_ROOT:$PATH
            """
                )
            )

        if not found:
            ctx.exec(f"/bin/bash {installer_file} -c {version}")
        else:
            ctx.log.info(f"dotnet {version} already installed")
    else:
        raise NotImplementedError(
            f"dotnet {version} not implemented on platform: {
                ctx.system.platform}:{ctx.system.distro}"
        )


def _toolbox(ctx: TaskContext):
    if "debian" in ctx.system.distro:
        toolbox = os.path.expanduser(
            "~/.local/share/JetBrains/Toolbox/bin/jetbrains-toolbox")
        if not os.path.exists(toolbox):
            ctx.exec("sudo apt-get install -y fuse libfuse2")
            ctx.exec("mkdir -p /tmp/jtoolbox")
            ctx.exec(
                "curl -o /tmp/jtoolbox.tar.gz -L 'https://data.services.jetbrains.com/products/download?platform=linux&code=TBA'"
            )
            ctx.exec("tar xvf /tmp/jtoolbox.tar.gz -C /tmp/jtoolbox")
            ret = ctx.exec(
                "find /tmp/jtoolbox -name jetbrains-toolbox", capture=True)
            if ret.returncode != 0:
                raise Exception(
                    f"Failed to find jetbrains toolbox: {ret.stderr}")

            ctx.exec(ret.stdout.strip())
    else:
        raise NotImplementedError(
            f"toolbox not implemented on platform: {
                ctx.system.platform}:{ctx.system.distro}"
        )


def _build_essential(ctx: TaskContext):
    tool = "build-essential"

    if "debian" in ctx.system.distro:
        if not os.path.exists("/usr/bin/gcc"):
            ctx.exec(f"sudo apt-get install -y {tool}")
        else:
            ctx.log.info(f"{tool} already installed")
    else:
        raise NotImplementedError(
            f"{tool} not implemented on platform: {
                ctx.system.platform}:{ctx.system.distro}"
        )


def _node(ctx: TaskContext):
    tool = "node"
    tool_version = "20"
    node_dir = os.path.expanduser("~/.nvm")

    if ctx.system.platform in ("linux", "darwin"):
        if not os.path.exists(node_dir):
            ctx.exec(
                "curl -o /tmp/nvm.sh -L -C - https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh")
            ctx.exec("bash /tmp/nvm.sh")
            # TODO: fix this
            # ctx.exec(f"zsh -l 'nvm install 20'")
        else:
            ctx.log.info(f"{tool} {tool_version} already installed")

        with open(os.path.expanduser("~/.shell.d/nvm"), "w") as f:
            f.write(
                dedent(
                    """
            export NVM_DIR="$HOME/.nvm"
            [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
            [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
            """
                )
            )

    else:
        raise NotImplementedError(
            f"{tool} not implemented on platform: {
                ctx.system.platform}:{ctx.system.distro}"
        )


def _lazygit(ctx: TaskContext):
    tool = "lazygit"
    if "debian" in ctx.system.distro:
        bin_dir = os.path.expanduser("~/bin")
        lazygit = os.path.join(bin_dir, tool)
        if not os.path.exists(lazygit):
            ctx.log.info(f"installing {tool}")

            release_url = system.get_github_download_url(
                ctx, "jesseduffield", "lazygit", r"Linux_x86_64.tar.gz$")
            ctx.exec(f"curl -o /tmp/lazygit.tar.gz -L -C - '{release_url}'")
            ctx.exec(f"tar xvf /tmp/lazygit.tar.gz -C {bin_dir} lazygit")
            ctx.exec(f"chmod +x {lazygit}")
            shutil.rmtree("/tmp/lazygit.tar.gz", ignore_errors=True)
        else:
            ctx.log.info(f"{tool} already installed")
    elif "darwin" in ctx.system.platform:
        brew_install(ctx, "lazygit")
    else:
        raise NotImplementedError(
            f"lazygit not implemented on platform: {
                ctx.system.platform}:{ctx.system.distro}"
        )


def _conda(ctx: TaskContext):
    tool = "conda"
    if "debian" in ctx.system.distro:
        bin_dir = os.path.expanduser("~/miniconda3")
        if os.path.exists(bin_dir):
            ctx.log.info(f"installing {tool}")

            release_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
            ctx.exec(f"curl -o /tmp/conda.sh -L -C - '{release_url}'")
            ctx.exec(f"bash /tmp/conda.sh -b -u -p {bin_dir}")
            ctx.exec(
                f"{os.path.expanduser(
                    '~/miniconda3/bin/conda create -n py312 python=3.12 -y')}"
            )
            shutil.rmtree("/tmp/conda.sh", ignore_errors=True)

            shell_file = os.path.expanduser("~/.shell.d/conda")
            with open(shell_file, "w") as f:
                f.write(
                    dedent(
                        """
                    # >>> conda initialize >>>
                    # !! Contents within this block are managed by 'conda init' !!
                    __conda_setup="$('/home/chris/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
                    if [ $? -eq 0 ]; then
                        eval "$__conda_setup"
                    else
                        if [ -f "/home/chris/miniconda3/etc/profile.d/conda.sh" ]; then
                            . "/home/chris/miniconda3/etc/profile.d/conda.sh"
                        else
                            export PATH="/home/chris/miniconda3/bin:$PATH"
                        fi
                    fi
                    unset __conda_setup
                    # <<< conda initialize <<<

                    conda activate py312
                """
                    )
                )

        else:
            ctx.log.info(f"{tool} already installed")
    else:
        raise NotImplementedError(
            f"lazygit not implemented on platform: {
                ctx.system.platform}:{ctx.system.distro}"
        )


def _deno(ctx: TaskContext):
    tool = "deno"
    if "debian" in ctx.system.distro:
        bin_dir = os.path.expanduser("~/bin")
        deno = os.path.join(bin_dir, tool)
        if not os.path.exists(deno):
            ctx.log.info(f"installing {tool}")

            release_url = system.get_github_download_url(
                ctx, "denoland", "deno", r"x86_64-unknown-linux-gnu.zip$")
            ctx.exec(f"curl -o /tmp/deno.zip -L -C - '{release_url}'")
            ctx.exec(f"unzip /tmp/deno.zip deno -d {bin_dir}")
            ctx.exec(f"chmod +x {deno}")
            shutil.rmtree("/tmp/deno.zip", ignore_errors=True)
        else:
            ctx.log.info(f"{tool} already installed")
    else:
        raise NotImplementedError(
            f"{tool} not implemented on platform: {
                ctx.system.platform}:{ctx.system.distro}"
        )


def _git_lfs(ctx: TaskContext):
    tool = "git-lfs"
    if "debian" in ctx.system.distro:
        apt_install(ctx, "git-lfs", "/usr/bin/git-lfs")
    elif "darwin" in ctx.system.platform:
        brew_install(ctx, "git-lfs")
    else:
        raise NotImplementedError(
            f"{tool} not implemented on platform: {
                ctx.system.platform}:{ctx.system.distro}"
        )


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:meld", lambda ctx: apt_install(
        ctx, "meld", "/usr/bin/meld"))
    builder.add_task(
        module_name,
        f"{module_name}:postman",
        lambda ctx: snap_install(ctx, "postman"),
    )
    builder.add_task(
        module_name,
        f"{module_name}:dbeaver",
        lambda ctx: snap_install(ctx, "dbeaver-ce"),
    )
    builder.add_task(module_name, f"{module_name}:git:config", _git_config)
    builder.add_task(module_name, f"{module_name}:git:lfs", _git_lfs)
    builder.add_task(module_name, f"{module_name}:gitkraken", lambda ctx: snap_install(
        ctx, "gitkraken", classic=True))
    builder.add_task(module_name, f"{module_name}:lazygit", _lazygit)
    builder.add_task(
        module_name,
        f"{module_name}:dotnet:all",
        lambda ctx: None,
        deps=[
            f"{module_name}:dotnet:6",
            f"{module_name}:dotnet:7",
            f"{module_name}:dotnet:8",
        ],
    )
    builder.add_task(
        module_name, f"{module_name}:dotnet:6", lambda ctx: _dotnet_installer(ctx, "6.0"), deps=["utils:curl"]
    )
    builder.add_task(
        module_name, f"{module_name}:dotnet:7", lambda ctx: _dotnet_installer(ctx, "7.0"), deps=["utils:curl"]
    )
    builder.add_task(
        module_name, f"{module_name}:dotnet:8", lambda ctx: _dotnet_installer(ctx, "8.0"), deps=["utils:curl"]
    )
    builder.add_task(module_name, f"{module_name}:toolbox", _toolbox)
    builder.add_task(
        module_name, f"{module_name}:build-essential", _build_essential)
    builder.add_task(
        module_name, f"{module_name}:node", _node, deps=["utils:xz"])
    builder.add_task(module_name, f"{module_name}:conda", _conda)
    builder.add_task(module_name, f"{module_name}:deno", _deno)
