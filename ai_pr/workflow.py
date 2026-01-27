from .git import run_command, pr_exists, create_pull_request, get_git_diff
from .models import get_ai_review, parse_ai_response
from . import ui


def run_workflow(target_branch):
    current_branch = run_command(["git", "branch", "--show-current"])

    if pr_exists(current_branch, target_branch):
        ui.show_warning(
            f"An open PR already exists for {current_branch} -> {target_branch}"
        )
        return

    with ui.show_loading(f"Fetching git diff against {target_branch}..."):
        diff = get_git_diff(target_branch)

    if not diff:
        return

    while True:
        with ui.show_loading("Generating PR draft..."):
            response = get_ai_review(diff)

        if response == "ERROR: CLAUDE_FETCH_FAILED":
            ui.show_error(
                "The 'claude' command failed to execute. Please check your CLI setup."
            )
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
