from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional, Union

from ksuid import Ksuid
from pydantic import BaseModel, Field

from ..models.refund import CancellationReason


class PaymentStatus(Enum):
    """
    Enum that represents the different payment statuses.
    """

    CREATED = "created"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    REQUIRES_ACTION = "requires_action"
    PROCESSING = "processing"
    CANCELED = "canceled"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

    @classmethod
    def from_name(cls, name: str) -> "PaymentStatus":
        """
        Convert a string name to a corresponding PaymentStatus.

        Args:
            name (str): The name of the payment status (case insensitive).

        Returns:
            PaymentStatus: The corresponding PaymentStatus instance.

        Raises:
            ValueError: If the name does not match any valid payment status.
        """
        try:
            return cls[name.upper()]  # Ensure case insensitivity
        except KeyError:
            raise ValueError(f"Invalid payment status name: {name}")

    def __str__(self):
        """
        Return the string representation of the PaymentStatus enum.

        Returns:
            str: The value of the enum.
        """
        return str(self.value)


class Payment(BaseModel):
    """
    Represents a payment transaction with various attributes such as amount, currency, status, etc.

    Attributes:
        id (str): Unique identifier for the payment.
        object (str): Type of the object, always 'payment'.
        amount (int): Amount to be charged in the smallest currency unit.
        currency (str): Currency code following ISO 4217 alpha-3 format.
        order (str): Order identifier.
        created (int): Timestamp of payment creation in seconds since Unix epoch.
        authorization (Optional[str]): Authorization identifier if available.
        status (PaymentStatus): Status of the payment.
        canceled_at (Optional[int]): Timestamp of when the payment was canceled, in seconds since Unix epoch.
        cancellation_reason (Optional[CancellationReason]): Reason for the payment cancellation.
        metadata (Optional[Dict[str, Union[str, int, float, bool]]]): Additional metadata related to the payment.
        phone (Optional[str]): Customer's phone number associated with the payment.
        payment_method (str): Payment method used, default is 'bizum'.
        operation_id (Optional[str]): Bizum operation ID.
        truncated_account (Optional[str]): Bizum truncated account.
        store_id (Optional[str]): Store identification.
    """

    id: str = Field(
        default_factory=lambda: str(Ksuid()),
        description="Unique identifier for the payment.",
    )
    object: str = Field(
        default="payment", description="Type of the object, always 'payment'."
    )
    amount: int = Field(
        ..., description="Amount to be charged in the smallest currency unit."
    )
    currency: str = Field(
        ..., description="Currency code following ISO 4217 alpha-3 format."
    )
    order: str = Field(..., description="Order identifier.")
    created: int = Field(
        default_factory=lambda: int(datetime.now(timezone.utc).timestamp()),
        description="Timestamp of when the payment was created, measured in seconds since Unix epoch.",
    )
    authorization: Optional[str] = Field(
        None, description="Authorization identifier if available."
    )
    status: PaymentStatus = Field(..., description="Status of the payment.")
    canceled_at: Optional[int] = Field(
        None,
        description="Timestamp of when the payment was canceled, measured in seconds since Unix epoch.",
    )
    cancellation_reason: Optional[CancellationReason] = Field(
        None, description="Reason for the payment cancellation."
    )
    metadata: Optional[Dict[str, Union[str, int, float, bool]]] = Field(
        default_factory=dict, description="Additional metadata related to the payment."
    )
    phone: Optional[str] = Field(
        None, description="Customer's phone number associated with the payment."
    )
    payment_method: str = Field(
        default="bizum", description="Payment method used, default is 'bizum'."
    )
    operation_id: Optional[str] = Field(default=None, description="Bizum operation id")
    truncated_account: Optional[str] = Field(
        default=None, description="Bizum truncated account"
    )
    store_id: Optional[str] = Field(default=None, description="Store identification")

    def cancel(self, reason: CancellationReason) -> None:
        """
        Cancel the payment and provide a reason for cancellation.

        Args:
            reason (CancellationReason): The reason why the payment was canceled.
        """
        self.status = PaymentStatus.CANCELED
        self.canceled_at = int(datetime.now(timezone.utc).timestamp())
        self.cancellation_reason = reason

    def mark_succeeded(self) -> None:
        """
        Mark the payment as successful.
        """
        self.status = PaymentStatus.SUCCEEDED

    def require_action(self) -> None:
        """
        Mark the payment as requiring additional action from the customer.
        """
        self.status = PaymentStatus.REQUIRES_ACTION

    def confirm(self) -> None:
        """
        Confirm the payment, moving it to the processing state.
        """
        self.status = PaymentStatus.PROCESSING

    def update_metadata(self, key: str, value: Union[str, int, float, bool]) -> None:
        """
        Update or add a metadata key-value pair.

        Args:
            key (str): The metadata key.
            value (Union[str, int, float, bool]): The metadata value.
        """
        self.metadata[key] = value
