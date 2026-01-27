import sys

from . import ui
from .workflow import run_workflow


def main():
    if len(sys.argv) < 2:
        ui.show_warning("Usage: ai-pr <target-branch>")
        return

    ui.show_icon()

    target_branch = sys.argv[1]
    
    try:
        run_workflow(target_branch)
    except KeyboardInterrupt:
        print("")
        ui.show_warning("Operation cancelled by user.")
        sys.exit(0)
