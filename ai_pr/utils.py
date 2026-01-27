import subprocess
import os

from .ui import show_error


def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if e.stderr:
            show_error(f"\nCLI Error: {e.stderr.strip()}")
        return None


def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception as e:
        show_error(f"Could not read config at {path}: {e}")
        return ""


def get_config():
    xdg_config = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    global_config = os.path.join(xdg_config, ".ai-pr")

    if os.path.exists(global_config):
        return read_file(global_config)

    return ""
