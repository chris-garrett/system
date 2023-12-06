import os
from __task__ import TaskContext, TaskBuilder


def _dotnet_installer(ctx: TaskContext, version: str):
    if ctx.system.platform == "linux":
        print("dist 1")
        dotnet = os.path.expanduser("~/.dotnet/dotnet")
        installer_file = "/tmp/dotnet-install.sh"

        if not os.path.exists(installer_file):
            print("dist 2")
            ctx.exec(f"curl -L -o {installer_file} https://dot.net/v1/dotnet-install.sh")

        ret = ctx.exec(f"{dotnet} --list-sdks", quiet=True)
        if ret.returncode != 0:
            raise Exception(f"Failed to list dotnet sdks: {ret.stderr}")

        found = len([x for x in ret.stdout.splitlines() if x.startswith(version)])
        if not found:
            ctx.exec(f"/bin/bash {installer_file} -c {version}")


def _noop(ctx: TaskContext):
    ctx.log.info("installing all .net versions")


def configure(builder: TaskBuilder):
    module_name = "dotnet"
    builder.add_task(module_name, "dotnet:all", _noop, deps=["dotnet:6", "dotnet:7", "dotnet:8"])
    builder.add_task(module_name, "dotnet:6", lambda ctx: _dotnet_installer(ctx, "6.0"), deps=["utils:curl"])
    builder.add_task(module_name, "dotnet:7", lambda ctx: _dotnet_installer(ctx, "7.0"), deps=["utils:curl"])
    builder.add_task(module_name, "dotnet:8", lambda ctx: _dotnet_installer(ctx, "8.0"), deps=["utils:curl"])
