# Pikadantic

[![CI](https://img.shields.io/github/actions/workflow/status/karta9821/pikadantic/test.yml)](https://github.com/karta9821/pikadantic/actions?query=event%3Apush+branch%3Amaster+workflow%3ACI)
[![pypi](https://img.shields.io/pypi/v/pikadantic.svg)](https://pypi.python.org/pypi/pikadantic)
[![versions](https://img.shields.io/pypi/pyversions/pikadantic.svg)](https://github.com/karta9821/pikadantic)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Pikadantic** is a Python library that integrates [Pika](https://github.com/pika/pika/tree/main/pika) with [Pydantic](https://docs.pydantic.dev/latest/) to provide robust data validation for RabbitMQ messaging.

## 🚀 Why Pikadantic?

* **Seamless Integration**: Combines Pika's messaging capabilities with Pydantic's data validation.
* **Type Safety**: Leverages Python's type hints for clear and enforceable message schemas.
* **Data Integrity**: Validates messages before sending or processing, reducing runtime errors.

## 📦 Installation

Install Pikadantic using pip:

```bash
pip install pikadantic
```

## 🧩 Example Usage

Here's a simple example of how to use Pikadantic with RabbitMQ:

```python
from pika import BlockingConnection, ConnectionParameters
from pydantic import BaseModel
from pikadantic import validate_body

# Define your message model
class UserMessage(BaseModel):
    user_id: int
    name: str
    email: str

# Create a connection
connection = BlockingConnection(ConnectionParameters('localhost'))
channel = connection.channel()

# Define your message handler with validation
@validate_body(UserMessage)
def handle_message(channel, method, properties, body):
    # The body is already validated against UserMessage model
    print(f"Received message: {body}")

# Alternative approach using only_model=True
@validate_body(UserMessage, only_model=True)
def handle_message_simplified(message: UserMessage):
    # You get the validated model directly
    print(f"User {message.name} with ID {message.user_id}")

# Set up consumer
channel.basic_consume(
    queue='user_queue',
    on_message_callback=handle_message
)

# Start consuming
channel.start_consuming()
```

In this example:
- We define a `UserMessage` model using Pydantic
- The `validate_body` decorator ensures that incoming messages match our model
- We can use either the standard callback format or simplified model-only format
- Invalid messages will raise `PikadanticValidationError`

## 🛠️ Contributing

Contributions are welcome! If you'd like to add a new feature or fix a bug, please:
- Set up your local environment using uv.
- Run `make install` to install dependencies.
- Ensure 100% test coverage for your changes.
- Open a pull request and tag `@karta9821` as a reviewer.
- Pull requests without sufficient tests or that reduce test coverage will not be accepted.

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

> **Note**: Pikadantic is currently in an experimental phase. Use with caution in production environments.

---

## 🙏 Acknowledgments

This project was inspired by [pika-pydantic](https://github.com/ttamg/pika-pydantic/tree/main/pika_pydantic).
