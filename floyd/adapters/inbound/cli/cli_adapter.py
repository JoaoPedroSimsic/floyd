"""CLI Adapter - Primary adapter for command-line interface."""

import sys

from floyd.adapters.inbound.cli import ui
from floyd.application.ports.inbound.pr_generation_port import PRGenerationPort
from floyd.application.ports.outbound.git_repository_port import GitRepositoryPort
from floyd.domain.exceptions.domain_exception import DomainException
from floyd.domain.exceptions.git.invalid_branch_exception import InvalidBranchException
from floyd.domain.exceptions.git.branch_not_found_exception import (
    BranchNotFoundException,
)
from floyd.domain.exceptions.pr.pr_already_exist_exception import (
    PRAlreadyExistsException,
)
from floyd.domain.exceptions.pr.pr_generation_exception import PRGenerationException


class CLIAdapter:
    """Command-line interface adapter for Floyd."""

    def __init__(
        self,
        pr_generation_service: PRGenerationPort,
        git_repository: GitRepositoryPort,
    ) -> None:
        """Initialize CLI adapter with required services.

        Args:
            pr_generation_service: Service for PR generation.
            git_repository: Git repository for validation.
        """
        self._pr_service = pr_generation_service
        self._git_repository = git_repository

    def run(self, args: list[str]) -> int:
        """Run the CLI application.

        Args:
            args: Command-line arguments (excluding program name).

        Returns:
            Exit code (0 for success, non-zero for errors).
        """
        if len(args) < 1:
            ui.show_warning("Usage: floyd <target-branch>")
            return 1

        if not self._git_repository.is_git_repo():
            ui.show_error("Error: This directory is not a git repository.")
            return 1

        ui.show_icon()

        target_branch = args[0]

        try:
            return self._run_workflow(target_branch)
        except KeyboardInterrupt:
            print("")
            ui.show_warning("Operation cancelled by user.")
            return 0

    def _run_workflow(self, target_branch: str) -> int:
        """Execute the PR generation workflow.

        Args:
            target_branch: Target branch for the PR.

        Returns:
            Exit code.
        """
        current_branch = self._git_repository.get_current_branch()

        try:
            self._pr_service.validate_can_create_pr(current_branch, target_branch)
        except InvalidBranchException as e:
            ui.show_warning(e.message)
            return 1
        except BranchNotFoundException as e:
            ui.show_error(
                f"Error: The branch '{e.branch_name}' does not exist on origin."
            )
            return 1
        except PRAlreadyExistsException as e:
            ui.show_warning(
                f"An open PR already exists for '{e.head_branch}' -> '{e.base_branch}'"
            )
            return 1

        with ui.show_loading(f"Fetching git diff against '{target_branch}'..."):
            context = self._pr_service.get_git_context(target_branch)

        if not context.has_changes():
            ui.show_warning("No changes found to create a PR.")
            return 1

        ui.show_info("Successfully fetched branch diff")

        feedback: str | None = None

        while True:
            with ui.show_loading("Generating PR draft..."):
                try:
                    pr = self._pr_service.generate_draft(context, feedback)
                except PRGenerationException as e:
                    ui.show_error(f"Failed to generate PR: {e.message}")
                    return 1
                except DomainException as e:
                    ui.show_error(e.message)
                    return 1

            ui.display_draft(pr)
            choice = ui.get_action_choice()

            if choice == "create":
                with ui.show_loading("Creating pull request..."):
                    try:
                        url = self._pr_service.create_pr(pr, target_branch)
                        if url:
                            ui.show_success("PR successfully created!")
                            ui.show_info(url)
                        else:
                            ui.show_error("Failed to create PR.")
                            return 1
                    except DomainException as e:
                        ui.show_error(f"Failed to create PR: {e.message}")
                        return 1
                break

            elif choice == "refine":
                feedback = ui.get_refinement_feedback()
                ui.show_info("Regenerating with your feedback...")
                continue

            else:
                ui.show_warning("Operation cancelled.")
                break

        return 0


def main() -> None:
    """Entry point for the CLI application."""
    from floyd.container import create_container

    container = create_container()
    cli = CLIAdapter(
        pr_generation_service=container.pr_generation_service,
        git_repository=container.git_repository,
    )
    sys.exit(cli.run(sys.argv[1:]))
