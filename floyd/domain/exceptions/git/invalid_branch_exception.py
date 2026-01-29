from floyd.domain.exceptions.domain_exception import DomainException


class InvalidBranchException(DomainException):
    """Raised when branch validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
