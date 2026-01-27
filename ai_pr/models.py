from .git import run_command
from . import ui
from .utils import get_config


def load_config():
    config = get_config("ai")

    settings = {"diff_limit": "", "instructions": ""}

    if not config:
        return settings

    if isinstance(config, dict):
        settings.update(config)

        for key, value in settings.items():
            if value:
                display_value = (
                    f"{str(value)[:30]}..." if len(str(value)) > 30 else value
                )
                ui.show_info(f"'{key}' loaded with value: {display_value}")

    return settings


def get_ai_review(diff, branch_name, commits, target_branch, diff_stat):
    config = load_config()

    custom_instructions = config.get("instructions", "")
    diff_limit = config.get("diff_limit", "-1")

    try:
        limit = int(diff_limit) if diff_limit and str(diff_limit).strip('-').isdigit() else -1
    except ValueError:
        limit = -1

    if limit != -1 and len(diff) > limit:
        ui.show_warning(f"Diff exceeds character limit. Truncating to {limit} chars.")

        diff = diff[:limit] + "\n\n[... DIFF TRUNCATED FOR TOKEN LIMITS ...]"

    extra_prompt = ""

    if custom_instructions:
        extra_prompt = f"\nUSER-SPECIFIC INSTRUCTIONS:\n{custom_instructions}\n"

    prompt = (
        f"Context:\n"
        f"- Working on branch: {branch_name}\n"
        f"- Target branch: {target_branch}\n"
        f"- Recent commits:\n{commits}\n\n"
        f"- File Change Summary:\n{diff_stat}\n\n"
        f"Task: Review the git diff below and write a PR title and description. "
        f"Use the commit history to understand the intent behind the changes.\n\n"
        f"{extra_prompt}"
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
