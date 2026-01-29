from floyd.domain.exceptions.domain_exception import DomainException


class PRAlreadyExistsException(DomainException):
    """Raised when a PR already exists for the branch."""

    def __init__(self, head_branch: str, base_branch: str) -> None:
        super().__init__(
            f"A pull request already exists for '{head_branch}' -> '{base_branch}'"
        )
        self.head_branch = head_branch
        self.base_branch = base_branch
