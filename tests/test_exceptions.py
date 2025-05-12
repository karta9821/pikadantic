import pytest
from pikadantic.exceptions import PikadanticValidationError
from pydantic import BaseModel, ValidationError


@pytest.mark.parametrize("exc", [PikadanticValidationError])
def test_pikadantic_validation_error_inherits_from_exception(exc: type[Exception]):
    assert issubclass(exc, Exception)


class TestPikadanticValidationError:
    class M(BaseModel):
        a: int

    def test_when_error_is_validation_error_then_str_returns_error_message(self):
        try:
            self.M.model_validate_json(b'{"a": "not an int"}')
        except ValidationError as e:
            error = e

        assert "Validation error" in str(PikadanticValidationError(error))

    def test_when_error_is_validation_error_then_repr_returns_error_message(self):
        try:
            self.M.model_validate_json(b'{"a": "not an int"}')
        except ValidationError as e:
            error = e

        assert "PikadanticValidationError" in repr(PikadanticValidationError(error))
