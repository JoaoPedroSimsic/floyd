import sys

from .git import get_git_diff, create_pull_request
from .models import get_ai_review, parse_ai_response
from . import ui


def main():
    ui.show_icon()

    if len(sys.argv) < 2:
        ui.show_warning("Usage: ai-pr <target-branch>")
        return

    target_branch = sys.argv[1]
    
    with ui.show_loading(f"Fetching git diff against {target_branch}..."):
        diff = get_git_diff(target_branch)

    if not diff:
        return

    ui.show_info("Generating initial PR draft...")

    while True:
        with ui.show_loading("Generating PR draft..."):
            response = get_ai_review(diff)

        if not response:
            ui.show_error("Claude didn't return a response.")
            return

        title, body = parse_ai_response(response)

        if not title or not body:
            ui.show_warning("Parsing error: Unexpected format.")
            return

        ui.display_draft(title, body)
        choice = ui.get_action_choice()

        if choice == "create":
            if create_pull_request(title, body, target_branch):
                ui.show_success("PR successfully created!")
            else:
                ui.show_error("Failed to create PR.")
            break
        else:
            ui.show_warning("Operation cancelled.")
            break
