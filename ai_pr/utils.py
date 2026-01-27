import subprocess
import os
import tomllib

from .ui import show_error


def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if e.stderr:
            show_error(f"\nCLI Error: {e.stderr.strip()}")
        return None


def get_config(profile="ai"):
    xdg_config = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    config_path = os.path.join(xdg_config, ".ai-pr")

    if not os.path.exists(config_path):
        return ""

    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        
        if not profile or profile not in data:
            return ""
            
        return data[profile].get("instructions", "").strip()
            
    except Exception:
        return ""
