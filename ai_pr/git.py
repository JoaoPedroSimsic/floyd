import subprocess

from . import ui
from .utils import run_command


def branch_exists(branch_name):
    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", "--heads", "origin", branch_name],
        capture_output=True,
        text=True,
    )

    return result.returncode == 0


def get_current_branch():
    return run_command(["git", "branch", "--show-current"])


def get_recent_commits(base_branch):
    return run_command(["git", "log", f"{base_branch}..HEAD", "--oneline"])


def get_diff_stat(base_branch):
    return run_command(
        [
            "git",
            "diff",
            "--stat",
            "--merge-base",
            base_branch,
            ":!*.lock",
            ":!*-lock.json",
        ]
    )


def get_git_diff(base_branch=None):
    if not branch_exists(base_branch):
        ui.show_error(f"Error: The branch '{base_branch}' does not exist on origin.")
        return None

    diff = run_command(
        ["git", "diff", "--merge-base", base_branch, ":!*.lock", ":!*-lock.json"]
    )

    if diff:
        ui.show_info(f"Successfully fetched branch diff")
        return diff

    return None


def pr_exists(head_branch, base_branch):
    result = run_command(
        [
            "gh",
            "pr",
            "list",
            "--head",
            head_branch,
            "--base",
            base_branch,
            "--state",
            "open",
            "--json",
            "number",
            "--jq",
            ".[0].number",
        ]
    )

    return bool(result)


def create_pull_request(title, body, base):
    with ui.show_loading(f"Creating pull request..."):
        result = run_command(
            ["gh", "pr", "create", "--title", title, "--body", body, "--base", base]
        )
        return result is not None
