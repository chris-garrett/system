import os
from __task__ import TaskBuilder, TaskContext
from __system__ import apt_install


module_name = "vm"


def _setup(ctx: TaskContext):
    if ctx.system.distro == "debian":
        if not os.path.exists("/usr/sbin/kvm-ok"):
            ctx.exec(
                "sudo apt install -y bridge-utils cpu-checker libvirt-clients libvirt-daemon qemu qemu-kvm virt-manager ovmf net-tools"  # noqa
            )
        else:
            ctx.log.info("already installed")
    else:
        raise NotImplementedError(f"{module_name} not implemented")


def _guest(ctx: TaskContext):
    if ctx.system.distro == "debian":
        apt_install(ctx, "open-vm-tools-desktop", "/usr/bin/vmware-user")
        apt_install(ctx, "qemu-guest-agent", "/etc/init.d/qemu-guest-agent")
        # tools for window snapping. map to win+left, win+right etc
        apt_install(ctx, "xdotool", "/usr/bin/xdotool")
        apt_install(ctx, "wmctrl", "/usr/bin/wmctrl")
    else:
        raise NotImplementedError(f"{module_name}:guest not implemented")


def _vm_create(ctx: TaskContext, name: str):
    if ctx.system.platform == "linux":
        iso_path = os.path.expanduser("~/Downloads/OS/lubuntu-22.04.3-desktop-amd64.iso")
        vm_name = name.lower()
        vm_dir = os.path.expanduser(f"~/vms/{name}")

        if not os.path.exists(vm_dir):
            os.makedirs(vm_dir, exist_ok=True)

            ctx.exec(
                f"""virt-install \
                    --name {vm_name} \
                    --vcpus 12 \
                    --memory 16384 \
                    --disk path={vm_dir}/{vm_name}-os.qcow2,size=100 \
                    --network network=default \
                    --graphics spice \
                    --video qxl,vram=262144 \
                    --os-variant ubuntu22.04 \
                    --cdrom {iso_path}
                """
            )
        else:
            ctx.log.info("already created")

    else:
        raise NotImplementedError(f"{module_name} not implemented")


def _vm_start(ctx: TaskContext, name: str):
    if ctx.system.distro == "debian":
        ctx.exec(f"virsh start {name}")
    else:
        raise NotImplementedError(f"{module_name} not implemented")


def _vm_stop(ctx: TaskContext, name: str):
    if ctx.system.distro == "debian":
        ctx.exec(f"virsh start {name}")
    else:
        raise NotImplementedError(f"{module_name} not implemented")


def _vm_setup_bridge(ctx: TaskContext):
    if ctx.system.distro == "debian":
        ctx.exec(f"sudo bash {ctx.project_dir}/netplan-public-bridge-setup.sh")
    else:
        raise NotImplementedError(f"{module_name} not implemented")


def configure(builder: TaskBuilder):
    builder.add_task(module_name, f"{module_name}:install", _setup)
    builder.add_task(module_name, f"{module_name}:guest", _guest)
    builder.add_task(module_name, f"{module_name}:bridge", _vm_setup_bridge)
    builder.add_task(module_name, f"{module_name}:ce:create", lambda ctx: _vm_create(ctx, "ce"))
    builder.add_task(module_name, f"{module_name}:ce:up", lambda ctx: _vm_start(ctx, "ce"))
    builder.add_task(module_name, f"{module_name}:ce:down", lambda ctx: _vm_stop(ctx, "ce"))
