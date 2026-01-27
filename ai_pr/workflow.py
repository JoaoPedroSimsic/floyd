from .git import (
    get_diff_stat,
    get_recent_commits,
    pr_exists,
    create_pull_request,
    get_git_diff,
    get_current_branch,
)
from .models import get_ai_review, parse_ai_response
from . import ui
from .utils import get_config


def run_workflow(target_branch):
    current_branch = get_current_branch()

    if target_branch == current_branch:
        ui.show_warning(f"You cannot create a PR from '{current_branch}' to itself.")
        return

    if pr_exists(current_branch, target_branch):
        ui.show_warning(
            f"An open PR already exists for '{current_branch}' -> '{target_branch}'"
        )
        return

    with ui.show_loading(f"Fetching git diff against '{target_branch}'..."):
        diff = get_git_diff(target_branch)

    if not diff:
        return

    commits = get_recent_commits(target_branch)
    diff_stat = get_diff_stat(target_branch)

    extra_instructions = get_config("ai")

    if extra_instructions:
        ui.show_info("AI config loaded successfully.")

    refinement_notes = ""

    while True:
        with ui.show_loading("Generating PR draft..."):
            response = get_ai_review(
                diff,
                current_branch,
                commits,
                target_branch,
                diff_stat,
                extra_instructions,
            )

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
        elif choice == "refine":
            refinement_notes = ui.get_refinement_feedback()
            ui.show_info("Regenerating with your feedback...")
            continue
        else:
            ui.show_warning("Operation cancelled.")
            break
