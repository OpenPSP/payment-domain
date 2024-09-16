# `payment-domain`

A Python package for handling common payment-related domain models, such as Payment, Refund, and Merchant. This package provides a standardized way to manage payment data and ensures consistency across various services and clients like the Redsys gateway, Bizum, and Redsys clients.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Models](#models)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Standardized payment domain models including `Payment`, `Refund`, and `Merchant`.
- Enum types for common statuses and reasons (e.g., `PaymentStatus`, `RefundStatus`, `CancellationReason`).
- Simple serialization and deserialization for payment data.
- Type-safe and consistent validation with [Pydantic](https://pydantic-docs.helpmanual.io/).

## Installation

To install `payment-domain` directly from GitHub:

1. Add the following line to your `pyproject.toml` in the `[tool.poetry.dependencies]` section:

    ```toml
    payment-domain = { git = "https://github.com/yourusername/payment-domain.git", branch = "main" }
    ```

2. Run the following command to install the package:

    ```bash
    poetry install
    ```

Alternatively, you can clone the repository and install it locally:

```bash
git clone https://github.com/yourusername/payment-domain.git
cd payment-domain
poetry install
```

## Usage

Here is a basic example of how to use the `Payment`, `Refund`, and `Merchant` models:

```python
from payment_domain.models import Payment, Refund, Merchant, PaymentStatus

# Create a new Payment
payment = Payment(
    amount=10000,
    currency="EUR",
    order="ORDER12345",
    status=PaymentStatus.CREATED,
    payment_method="bizum"
)

# Cancel a Payment
payment.cancel(reason="requested_by_customer")

# Create a Refund
refund = Refund(
    amount=10000,
    currency="EUR",
    order="ORDER12345",
    payment_id=payment.id
)
```

## Models

### Payment

The `Payment` model represents a payment transaction and includes fields like `amount`, `currency`, `status`, and metadata.

- **Attributes:**
  - `id`: A unique identifier for the payment.
  - `amount`: The amount to be charged.
  - `currency`: Currency code in ISO 4217 format.
  - `status`: The current status of the payment (e.g., `created`, `processing`).
  - `metadata`: Additional metadata related to the payment.
  
### Refund

The `Refund` model represents a refund related to a payment transaction.

- **Attributes:**
  - `id`: A unique identifier for the refund.
  - `amount`: The amount to be refunded.
  - `payment_id`: Reference to the original payment.
  - `status`: The current status of the refund (e.g., `created`, `succeeded`).
  
### Merchant

The `Merchant` model represents merchant information.

- **Attributes:**
  - `id`: A unique identifier for the merchant.
  - `fuc`: Merchant's FUC (Código de Comercio).
  - `terminal`: Merchant terminal identifier.

## Configuration

`payment-domain` uses [Pydantic](https://pydantic-docs.helpmanual.io/) for model validation. All models can be serialized and deserialized using Pydantic's `.dict()` and `.json()` methods.

## Contributing

We welcome contributions! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

Please make sure to run tests and use `black`, `isort`, and `mypy` for code formatting and type checking before submitting your pull request.

### Running Tests

To run the tests, first install the test dependencies:

```bash
poetry install --with dev
```

Then run:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

