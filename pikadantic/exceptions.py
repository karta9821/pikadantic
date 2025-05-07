from pydantic import ValidationError


class PikadanticBaseError(Exception):
    pass


class PikadanticValidationError(PikadanticBaseError):
    def __init__(self, error: ValidationError) -> None:
        self.error = error

    def __str__(self) -> str:
        return f"Validation error: {self.error}"

    def __repr__(self) -> str:
        return f"PikadanticValidationError(error={self.error!r})"
