import os
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


def _dotnet_installer(ctx: TaskContext, version: str):
    if ctx.system.platform == "linux":
        dotnet = os.path.expanduser("~/.dotnet/dotnet")
        installer_file = "/tmp/dotnet-install.sh"

        if not os.path.exists(installer_file):
            ctx.exec(f"curl -L -o {installer_file} https://dot.net/v1/dotnet-install.sh")

        ret = ctx.exec(f"{dotnet} --list-sdks", quiet=True)
        if ret.returncode != 0:
            raise Exception(f"Failed to list dotnet sdks: {ret.stderr}")

        found = len([x for x in ret.stdout.splitlines() if x.startswith(version)])
        if not found:
            ctx.exec(f"/bin/bash {installer_file} -c {version}")
        else:
            ctx.log.info(f"dotnet {version} already installed")
    else:
        raise NotImplementedError(
            f"dotnet {version} not implemented on platform: {ctx.system.platform}:{ctx.system.distro}"
        )


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:meld", lambda ctx: apt_install(ctx, "meld", "/usr/bin/meld"))
    builder.add_task(module_name, f"{module_name}:postman", lambda ctx: snap_install(ctx, "postman"))
    builder.add_task(module_name, f"{module_name}:dbeaver", lambda ctx: snap_install(ctx, "dbeaver-ce"))
    builder.add_task(module_name, f"{module_name}:git:config", _git_config)
    builder.add_task(module_name, f"{module_name}:git:lfs", lambda ctx: apt_install(ctx, "git-lfs", "/usr/bin/git-lfs"))
    builder.add_task(module_name, f"{module_name}:gitkraken", lambda ctx: snap_install(ctx, "gitkraken", classic=True))
    builder.add_task(
        module_name,
        f"{module_name}:dotnet:all",
        lambda ctx: None,
        deps=[f"{module_name}:dotnet:6", f"{module_name}:dotnet:7", f"{module_name}:dotnet:8"],
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
