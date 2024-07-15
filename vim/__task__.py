import os
import shutil

from __system__ import (apt_install, deb_install_github, snap_install, download_to_tmp_file, 
    install_msi, brew_install, get_github_download_url, extract_tmp_file_to)
from __task__ import TaskBuilder, TaskContext


def _clean(ctx: TaskContext):
    nvim_dir = os.path.expanduser("~/.config/nvim")
    if os.path.exists(nvim_dir):
        shutil.rmtree(nvim_dir)

    tmux_dir = os.path.expanduser("~/.config/tmux*")
    if os.path.exists(tmux_dir):
        shutil.rmtree(tmux_dir)


def _install_neovim(ctx: TaskContext):

    if ctx.system.is_unix():
        if ctx.system.is_mac():
            brew_install(ctx, "nvim")
        elif ctx.system.is_linux():
            # install neovim
            snap_install(ctx, "nvim", classic=True)

        config_dir = os.path.expanduser("~/.config")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)

        nvim_dir = os.path.expanduser("~/.config/nvim")
        if not os.path.exists(nvim_dir):
            ctx.exec(f"ln -sf {ctx.project_dir}/nvim {nvim_dir}")

        return
    elif ctx.system.platform == "windows":

        ret = ctx.exec("nvim --version")
        ctx.log.info(f">>> {ret}")

        # has to be run by admin
        # mklink /j c:\users\chris\AppData\Local\nvim d:\projects\system\vim\nvim

        # if ctx.exec("nvim --version").returncode == 0:
        #     ctx.log.info("neovim already installed")
        #     return

        # fname = download_to_tmp_file(ctx,
        #                         url="https://github.com/neovim/neovim/releases/latest/download/nvim-win64.msi",
        #                         name="nvim.msi"
        #                         )
        # ctx.log.info("installing neovim")
        # install_msi(ctx, fname)

    raise NotImplementedError(f"neovim not implemented on platform: {ctx.system.platform} distro:{ctx.system.distro}")


def _install_alacritty(ctx: TaskContext):

    if ctx.system.is_unix():
        if ctx.system.is_mac():
            brew_install(ctx, "alacritty", cask=True)
        elif ctx.system.is_linux():
            # install alacritty
            snap_install(ctx, "alacritty", classic=True)

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

    # %APPDATA%\alacritty\alacritty.toml

    raise NotImplementedError(f"alacritty not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _install_nerdfonts(ctx: TaskContext):
    if ctx.system.is_unix():
        font_dir = os.path.expanduser("~/.local/share/fonts/NerdFonts" if ctx.system.is_linux() else "~/Library/Fonts/NerdFonts")
        if not os.path.exists(font_dir):
            ctx.log.info("installing nerd fonts")
            os.makedirs(font_dir, exist_ok=True)
            download_to_tmp_file(ctx, "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/UbuntuMono.tar.xz", "ubuntumono.tar.xz")
            ctx.exec(f"tar xvf tmp/ubuntumono.tar.xz -C {font_dir}")
        else:
            ctx.log.info("nerd fonts already installed")

        return

    raise NotImplementedError(f"nerdfonts not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _install_tmux(ctx: TaskContext):

    if ctx.system.is_unix():
        if ctx.system.is_linux():
            # install tmux
            apt_install(ctx, "tmux", "/usr/bin/tmux")
        elif ctx.system.is_mac():
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
        tmuxifier_layouts_dir_src = os.path.join(ctx.project_dir, "tmuxifier", "layouts")
        tmuxifier_layouts_dir_dest = os.path.join(tmuxifier_dir, "layouts")
        shutil.rmtree(tmuxifier_layouts_dir_dest, ignore_errors=True)
        ctx.exec(f"ln -sf {tmuxifier_layouts_dir_src} {tmuxifier_layouts_dir_dest}")

        # install tmuxifier shell integration
        shell_exports = os.path.expanduser("~/.shell.d/tmux")
        if not os.path.exists(shell_exports):
            ctx.log.info("installing tmuxifier shell integration")
            with open(shell_exports, "w") as w:
                w.write("\n")
                w.write("# tmuxifier\n")
                w.write('export PATH="$HOME/tmuxifier/bin:$PATH"\n')
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

    raise NotImplementedError(f"xmodmap not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _install_ripgrep(ctx: TaskContext):
    if ctx.system.platform == "linux":
        deb_install_github(ctx, "ripgrep", "/usr/bin/rg", "BurntSushi", "ripgrep", "amd64.deb")
    elif ctx.system.is_mac():
        release_url = get_github_download_url(ctx, "BurntSushi", "ripgrep", "aarch64-apple-darwin.tar.gz")
        file_part = release_url.split("/")[-1].replace(".tar.gz","")
        download_to_tmp_file(ctx, release_url, "ripgrep.tar.gz")
        extract_tmp_file_to(ctx, "ripgrep.tar.gz", os.path.expanduser("~/bin"), args="--strip-components=1", filters=f"{file_part}/rg")
    else:
        raise NotImplementedError(f"ripgrep not implemented on platform: {ctx.system.platform}:{ctx.system.distro}")


def _install_all(ctx: TaskContext):
    _install_tmux(ctx)
    _install_neovim(ctx)
    _install_ripgrep(ctx)
    _install_alacritty(ctx)
    _install_nerdfonts(ctx)
    _install_xmodmap(ctx)


def configure(builder: TaskBuilder):
    module_name = "vi"

    all_deps = ["os:snap", "os:shell", "dev:build-essential"] if builder.system.is_linux() else ["os:shell"]
    builder.add_task(module_name, f"{module_name}:all", _install_all, deps=all_deps)

    builder.add_task(module_name, f"{module_name}:clean", _clean)
    builder.add_task(module_name, f"{module_name}:ripgrep", _install_ripgrep)
    builder.add_task(module_name, f"{module_name}:tmux", _install_tmux, deps=["os:ensure_shelld"])
