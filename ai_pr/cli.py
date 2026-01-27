import sys

from . import ui
from .workflow import run_workflow


def main():
    ui.show_icon()

    if len(sys.argv) < 2:
        ui.show_warning("Usage: ai-pr <target-branch>")
        return

    target_branch = sys.argv[1]

    run_workflow(target_branch)
