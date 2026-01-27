import sys

from . import ui
from .workflow import run_workflow


def main():
    if len(sys.argv) < 2:
        ui.show_warning("Usage: ai-pr <target-branch>")
        return

    ui.show_icon()

    target_branch = sys.argv[1]

    run_workflow(target_branch)
