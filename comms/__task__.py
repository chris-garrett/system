from __system__ import snap_install
from __tasklib__ import TaskBuilder, TaskContext

module_name = "comms"


def _install_slack(ctx: TaskContext):
    snap_install(ctx, "slack")


# add functions for install discord and mattermost
def _install_discord(ctx: TaskContext):
    snap_install(ctx, "discord")


def _install_mattermost(ctx: TaskContext):
    snap_install(ctx, "mattermost-desktop")


def _install_all(ctx: TaskContext):
    _install_slack(ctx)
    _install_discord(ctx)
    _install_mattermost(ctx)


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:all", _install_all)
    builder.add_task(module_name, f"{module_name}:slack", _install_slack)
    builder.add_task(module_name, f"{module_name}:discord", _install_discord)
    builder.add_task(
        module_name, f"{module_name}:mattermost", _install_mattermost)
