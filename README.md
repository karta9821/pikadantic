# Pikadantic

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
<!-- TODO: Add examples -->

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

This project was inspired by [pika-pydantic](https://github.com/ttamg/pika-pydantic/tree/main/pika_pydantic), which elegantly combines Pika and Pydantic for message validation.
