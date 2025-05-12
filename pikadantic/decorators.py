from functools import wraps
from typing import Any, Callable, Literal, TypeVar, Union, cast, overload

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties
from pydantic import BaseModel, ValidationError

from pikadantic.exceptions import PikadanticValidationError

Model = TypeVar("Model", bound=BaseModel)
OnlyModelFunc = Callable[[Model], None]
StandardFunc = Callable[[BlockingChannel, str, BasicProperties, bytes], None]


def _handle_model_callback(
    model: type[Model],
    func: OnlyModelFunc[Model],
    json: bool,
    raise_on_error: bool,
) -> StandardFunc:
    """
    Internal function to handle model-only callbacks.

    Args:
        model: The Pydantic model to validate against.
        func: The callback function that takes only the model.
        json: Whether to parse body as JSON.
        raise_on_error: Whether to raise on validation error.

    Returns:
        A standard RabbitMQ callback function.
    """

    @wraps(func)
    def wrapper(
        _channel: BlockingChannel,
        _method: str,
        _properties: BasicProperties,
        body: bytes,
    ) -> None:
        try:
            result: Model = model.model_validate_json(body) if json else model.model_validate(body)
        except ValidationError as e:
            if raise_on_error:
                raise PikadanticValidationError(e) from e
            return

        func(result)

    return wrapper


def _handle_standard_callback(
    model: type[Model],
    func: StandardFunc,
    json: bool,
    raise_on_error: bool,
) -> StandardFunc:
    """
    Internal function to handle standard callbacks.

    Args:
        model: The Pydantic model to validate against.
        func: The standard RabbitMQ callback function.
        json: Whether to parse body as JSON.
        raise_on_error: Whether to raise on validation error.

    Returns:
        A standard RabbitMQ callback function with validation.
    """

    @wraps(func)
    def wrapper(
        channel: BlockingChannel,
        method: str,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        try:
            model.model_validate_json(body) if json else model.model_validate(body)
        except ValidationError as e:
            if raise_on_error:
                raise PikadanticValidationError(e) from e
            return

        func(channel, method, properties, body)

    return wrapper


@overload
def validate_body(
    model: type[Model], *, json: bool = True, raise_on_error: bool = True, only_model: Literal[True]
) -> Callable[[OnlyModelFunc[Model]], StandardFunc]: ...


@overload
def validate_body(
    model: type[Model], *, json: bool = True, raise_on_error: bool = True, only_model: Literal[False]
) -> Callable[[StandardFunc], StandardFunc]: ...


def validate_body(
    model: type[Model],
    *,
    json: bool = True,
    raise_on_error: bool = True,
    only_model: bool = False,
) -> Any:
    """
    Decorator that validates RabbitMQ message bodies against a Pydantic model.

    This decorator can be used in two ways:
    1. With only_model=False (default): Wraps a standard RabbitMQ callback function
    2. With only_model=True: Converts a function that takes only the validated model to a standard callback

    Args:
        model: A Pydantic model class to validate the message body against.
        json: If True, expects JSON string in body. If False, expects raw bytes.
        raise_on_error: If True, raises PikadanticValidationError on validation failure.
        only_model: If True, the decorated function should take only the validated model as argument.

    Returns:
        A decorator that adds validation to a RabbitMQ callback function.

    Raises:
        PikadanticValidationError: If validation fails and raise_on_error is True.

    Example:
        ```python
        from pydantic import BaseModel
        from pikadantic import validate_body

        class UserMessage(BaseModel):
            user_id: int
            name: str

        # Standard callback format
        @validate_body(UserMessage)
        def handle_message(channel, method, properties, body):
            # body is already validated
            print(f"Received: {body}")

        # Simplified model-only format
        @validate_body(UserMessage, only_model=True)
        def handle_message_simplified(message: UserMessage):
            print(f"User {message.name} with ID {message.user_id}")
        ```
    """

    def decorator(func: Union[OnlyModelFunc[Model], StandardFunc]) -> StandardFunc:
        if only_model:
            return _handle_model_callback(
                model,
                cast("OnlyModelFunc[Model]", func),
                json,
                raise_on_error,
            )
        return _handle_standard_callback(
            model,
            cast("StandardFunc", func),
            json,
            raise_on_error,
        )

    return decorator


__all__ = ["validate_body"]
