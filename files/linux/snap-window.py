#!/usr/bin/env python3

# Snaps active window to the left or right half of the screen. Supports multiple monitors.
# Usage:
# $ ./snap-window.py left
# $ ./snap-window.py right
# When configuring global keyboard shortcuts, use python to call the script, e.g.:
#   Meta + Shift + L: /usr/bin/python3 /home/chris/projects/system/scripts/linux/snap-window.py left

import os
import re
import sys
import shlex
import subprocess
from subprocess import CompletedProcess
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler


def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kws)


TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")
logging.Logger.trace = trace

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(__file__.replace(".py", ".log"), maxBytes=1000),
    ],  # 1000000)],
)
logger = logging.getLogger("snap-window")


def exec(
    cmd: str, cwd: str = None, logger: Logger = None, venv_dir: str = None, capture: bool = False
) -> CompletedProcess[str]:
    args = [arg.strip() for arg in shlex.split(cmd.strip())]
    if isinstance(logger, Logger) and not capture:
        if cwd:
            logger.info("Executing: [%s] Cwd: [%s]", " ".join(args), cwd)
        else:
            logger.info("Executing: [%s]", " ".join(args))

    try:
        return subprocess.run(
            args,
            check=False,
            text=True,
            cwd=cwd,
            capture_output=capture,
        )
    except Exception as ex:
        return CompletedProcess(args=args, returncode=1, stdout="", stderr=str(ex))


def rx_group(index: int, regex: str, text: str) -> str:
    return re.search(regex, text).groups()[index]


def get_window_geometry(window: str) -> dict:
    """
    Returns a dict of (width, height, x, y)
    """
    p = re.search(r"Position:\s+([0-9]+),([0-9]+)", window).groups()
    d = re.search(r"Geometry:\s+([0-9]+)x([0-9]+)", window).groups()
    return {
        "width": int(d[0]),
        "height": int(d[1]),
        "x": int(p[0]),
        "y": int(p[1]),
    }


def get_monitor_geometry(monitor: str) -> dict:
    """
    Returns a dict of (width, height, x, y)
    """
    g = re.search(r"([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)", monitor).groups()
    return {
        "width": int(g[0]),
        "height": int(g[1]),
        "x": int(g[2]),
        "y": int(g[3]),
    }


def get_border_geometry(border: str) -> dict:
    """
    Returns a dict of (left width, right width, top height, bottom height)
    """
    g = re.search(r"([0-9]+),\s+([0-9]+),\s+([0-9]+),\s+([0-9]+)", border).groups()
    return {
        "left": int(g[0]),
        "right": int(g[1]),
        "top": int(g[2]),
        "bottom": int(g[3]),
    }


def main():
    try:
        window_side = "right" if "right" in sys.argv else "left"
        logger.info("")
        logger.info(f"New request to move window {window_side}")
        active_window = int(exec("xdotool getactivewindow", capture=True).stdout.strip())
        # for debugging:
        # active_window = 39845894
        logger.info("Active window: %s", active_window)

        window = get_window_geometry(exec(f"xdotool getwindowgeometry {active_window}", capture=True).stdout.strip())
        logger.info("Window: %s", window)

        borders = get_border_geometry(
            exec(f"xprop -id {active_window} _NET_FRAME_EXTENTS", capture=True).stdout.strip()
        )
        logger.info(f"Borders: {borders}")

        xrandr = exec("xrandr", capture=True).stdout.strip().split("\n")
        monitors = [get_monitor_geometry(x) for x in xrandr if " connected" in x]
        for monitor in monitors:
            if window["x"] >= monitor["x"] and window["x"] < monitor["x"] + monitor["width"]:
                new_width = int(monitor["width"] / 2) - (borders["left"] + borders["right"])
                new_height = monitor["height"] - (borders["top"] + borders["bottom"])
                new_x = monitor["x"]
                new_y = monitor["y"]

                if "right" in window_side:
                    new_x = monitor["x"] + new_width + borders["left"] + borders["right"]

                logger.info("Moving and resizing to: %s", f"{new_width}x{new_height}+{new_x}+{new_y}")
                exec(f"wmctrl -i -r {active_window} -b remove,maximized_vert,maximized_horz")
                exec(f"wmctrl -i -r {active_window} -e 0,{new_x},{new_y},{new_width},{new_height}")
                break
    except Exception as ex:
        logger.exception(ex)


if __name__ == "__main__":
    main()
