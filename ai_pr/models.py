from .git import run_command
from . import ui


def get_ai_review(diff, branch_name, commits, target_branch, diff_stat):
    prompt = (
        f"Context:\n"
        f"- Working on branch: {branch_name}\n"
        f"- Target branch: {target_branch}\n"
        f"- Recent commits:\n{commits}\n\n"
        f"- File Change Summary:\n{diff_stat}\n\n"
        f"Task: Review the git diff below and write a PR title and description. "
        f"Use the commit history to understand the intent behind the changes.\n\n"
        f"IMPORTANT: Do not include any signatures, footers, or mentions of "
        f"being 'Generated with Claude Code' or any other tool.\n\n"
        f"Format your response exactly like this:\n"
        f"TITLE: [Your Title]\n"
        f"BODY: [Your Description]\n\n"
        f"Diff:\n{diff}"
    )
    response = run_command(["claude", "-p", prompt])

    if response is None:
        return "ERROR: CLAUDE_FETCH_FAILED"

    ui.show_info(f"Successfully generated a PR.")

    return response


def parse_ai_response(response):
    if response == "ERROR: CLAUDE_FETCH_FAILED":
        return None, None

    try:
        title = response.split("TITLE:")[1].split("BODY:")[0].strip()
        body = response.split("BODY:")[1].strip()

        if not title or not body:
            return None, None

        return title, body
    except IndexError, AttributeError:
        return None, None
