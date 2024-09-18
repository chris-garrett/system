import os
import shutil

from __system__ import apt_install, deb_install_github, snap_install, download_to_tmp, install_msi, brew_install
from __tasklib__ import TaskBuilder, TaskContext


def _clean(ctx: TaskContext):
    nvim_dir = os.path.expanduser("~/.config/nvim")
    if os.path.exists(nvim_dir):
        shutil.rmtree(nvim_dir)

    tmux_dir = os.path.expanduser("~/.config/tmux*")
    if os.path.exists(tmux_dir):
        shutil.rmtree(tmux_dir)


def _install_neovim(ctx: TaskContext):

    def install_config_posix():
        nvim_dir = os.path.expanduser("~/.config/nvim")
        if not os.path.exists(nvim_dir):
            ctx.exec(f"ln -sf {ctx.project_dir}/nvim {nvim_dir}")

    if ctx.system.platform == "linux":

        # install neovim
        snap_install(ctx, "nvim", classic=True)
        install_config_posix()

        return
    elif ctx.system.platform == "windows":

        ret = ctx.exec("nvim --version")
        ctx.log.info(f">>> {ret}")

        # has to be run by admin
        # mklink /j c:\users\chris\AppData\Local\nvim d:\projects\system\vim\nvim

        # if ctx.exec("nvim --version").returncode == 0:
        #     ctx.log.info("neovim already installed")
        #     return

        # fname = download_to_tmp(ctx,
        #                         url="https://github.com/neovim/neovim/releases/latest/download/nvim-win64.msi",
        #                         name="nvim.msi"
        #                         )
        # ctx.log.info("installing neovim")
        # install_msi(ctx, fname)
    elif ctx.system.platform == "darwin":
        if not os.path.exists("/opt/homebrew/bin/nvim"):
            ctx.log.info("installing neovim")
            ctx.exec("brew install nvim")
        else:
            ctx.log.info("neovim already installed")

        install_config_posix()

        return

    raise NotImplementedError(f"neovim not implemented on platform: {ctx.system.platform} distro:{ctx.system.distro}")


def _install_alacritty(ctx: TaskContext):

    def install_config_posix():
        config_dir = os.path.expanduser("~/.config")

        # install config file
        alacritty_toml = "alacritty.toml"
        alacritty_dir = os.path.join(config_dir, "alacritty")
        if not os.path.exists(os.path.join(alacritty_dir, alacritty_toml)):
            ctx.log.info("installing alacritty config")
            ctx.exec(f"mkdir -p {alacritty_dir}")
            ctx.exec(f"cp {ctx.project_dir}/{alacritty_toml} {alacritty_dir}/{alacritty_toml}")
        else:
            ctx.log.info("alacritty config already installed")

    if ctx.system.platform == "linux":

        # install alacritty
        snap_install(ctx, "alacritty", classic=True)

        install_config_posix()

        # replace caps lock with ctrl
        xmod_file = os.path.expanduser("~/.Xmodmap")
        if not os.path.exists(xmod_file):
            ctx.log.info("installing xmodmap config")
            with open(f"{ctx.project_dir}/Xmodmap", "r") as r:
                with open(f"{xmod_file}", "a") as w:
                    w.write(r.read())
        else:
            ctx.log.info("xmodmap config already installed")

        return
    elif ctx.system.platform == "darwin":
        if not os.path.exists("/opt/homebrew/bin/alacritty"):
            ctx.log.info("installing alacritty")
            ctx.exec("brew install alacritty")
        else:
            ctx.log.info("alacritty already installed")

        install_config_posix()
        return

    # %APPDATA%\alacritty\alacritty.toml

    raise NotImplementedError(f"alacritty not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _install_nerdfonts(ctx: TaskContext):
    if ctx.system.platform == "linux" or ctx.system.platform == "darwin":
        
        if ctx.system.platform == "linux":
            dest = os.path.expanduser("~/.local/share/fonts/NerdFonts")
        if ctx.system.platform == "darwin":
            dest = os.path.expanduser("~/Library/Fonts/NerdFonts")

        if not os.path.exists(dest):
            ctx.log.info("installing nerd fonts")
            if not os.path.exists("/tmp/nerd-fonts"):
                ctx.exec("git clone --depth=1 https://github.com/ryanoasis/nerd-fonts.git /tmp/nerd-fonts")
            ctx.exec("/bin/bash /tmp/nerd-fonts/install.sh UbuntuMono")
        else:
            ctx.log.info("nerd fonts already installed")

        return

    raise NotImplementedError(f"nerdfonts not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _install_tmux(ctx: TaskContext):

    if ctx.system.platform == "linux" or ctx.system.platform == "darwin":

        # install tmux
        if ctx.system.platform == "linux":
            apt_install(ctx, "tmux", "/usr/bin/tmux")
        elif ctx.system.platform == "darwin":
            brew_install(ctx, "tmux")

        # link tmux config
        ctx.log.info("installing tmux config")
        tmux_config = os.path.expanduser("~/.tmux.conf")
        shutil.rmtree(tmux_config, ignore_errors=True)
        ctx.exec(f"ln -sf {ctx.project_dir}/tmux.conf {tmux_config}")

        # install tmux plugins
        tmp_plugins_dir = os.path.expanduser("~/.tmux/plugins")
        if not os.path.exists(f"{tmp_plugins_dir}/tpm"):
            ctx.log.info("installing tmux plugins")
            ctx.exec(f"mkdir -p {tmp_plugins_dir}")
            ctx.exec(f"git clone https://github.com/tmux-plugins/tpm {tmp_plugins_dir}/tpm")
        else:
            ctx.log.info("tmux plugins already installed")

        # install tmuxifier
        tmuxifier_dir = os.path.expanduser("~/.tmuxifier")
        if not os.path.exists(tmuxifier_dir):
            ctx.log.info("installing tmuxifier")
            ctx.exec(f"git clone git@github.com:jimeh/tmuxifier.git {tmuxifier_dir}")
        else:
            ctx.log.info("tmuxifier already installed")

        # link tmuxifier layouts
        tmuxifier_layouts_dir = f"{tmuxifier_dir}/layouts"
        shutil.rmtree(tmuxifier_layouts_dir, ignore_errors=True)
        ctx.exec(f"ln -sf {ctx.project_dir}/tmuxifier/layouts {tmuxifier_layouts_dir}")

        # install tmuxifier shell integration
        shell_exports = os.path.expanduser("~/.shell.d/tmux")
        if not os.path.exists(shell_exports):
            ctx.log.info("installing tmuxifier shell integration")
            with open(shell_exports, "w") as w:
                w.write("\n")
                w.write("# tmuxifier\n")
                w.write('export PATH="~/.tmuxifier/bin:$PATH"\n')
                w.write('eval "$(tmuxifier init -)"\n')
        else:
            ctx.log.info("tmuxifier shell integration already installed")

        return

    raise NotImplementedError(f"tmux not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _install_xmodmap(ctx: TaskContext):

    if ctx.system.platform == "linux":

        # replace caps lock with ctrl
        xmod_file = os.path.expanduser("~/.Xmodmap")
        if not os.path.exists(xmod_file):
            ctx.log.info("installing xmodmap config")
            with open(f"{ctx.project_dir}/Xmodmap", "r") as r:
                with open(f"{xmod_file}", "a") as w:
                    w.write(r.read())
        else:
            ctx.log.info("xmodmap config already installed")

        bashrc_file = os.path.expanduser("~/.bashrc")
        with open(bashrc_file, "r") as r:
            bashrc_contents = r.read()

        if "xmodmap ~/.Xmodmap" not in bashrc_contents:
            ctx.log.info("installing xmodmap in bashrc")
            with open(bashrc_file, "a") as w:
                w.write("\n")
                w.write("# xmodmap\n")
                w.write("xmodmap ~/.Xmodmap\n")
        else:
            ctx.log.info("xmodmap already in bashrc")

        return

    #raise NotImplementedError(f"xmodmap not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _install_ripgrep(ctx: TaskContext):
    if ctx.system.platform == "linux":
        deb_install_github(ctx, "ripgrep", "/usr/bin/rg", "BurntSushi", "ripgrep", "amd64.deb")
    elif ctx.system.platform == "darwin":
        brew_install(ctx, "ripgrep", "/opt/homebrew/bin/rg")
    else:
        raise NotImplementedError(f"ripgrep not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")

def _install_python(ctx: TaskContext):
    if ctx.system.platform == "linux":
        apt_install(ctx, "python3-venv", "/usr/bin/python3-venv")
    else:
        raise NotImplementedError(f"ripgrep not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")

def _install_all(ctx: TaskContext):
    #_install_python(ctx)
    _install_neovim(ctx)

    _install_alacritty(ctx)
    _install_tmux(ctx)
    _install_nerdfonts(ctx)
    _install_xmodmap(ctx)
    _install_ripgrep(ctx)


def configure(builder: TaskBuilder):
    module_name = "vi"
    builder.add_task(module_name, f"{module_name}:all", _install_all) #, deps=["os:snap", "os:shell", "dev:build-essential"])
    builder.add_task(module_name, f"{module_name}:clean", _clean)
    builder.add_task(module_name, f"{module_name}:ripgrep", _install_ripgrep)
