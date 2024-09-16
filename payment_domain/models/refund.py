from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional, Union

from ksuid import Ksuid
from pydantic import BaseModel, Field


class RefundStatus(Enum):
    """
    Enum representing the different statuses a refund can have.
    """

    CREATED = "created"
    PROCESSING = "processing"
    CANCELED = "canceled"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

    @classmethod
    def from_name(cls, name: str) -> "RefundStatus":
        """
        Convert a string name to a corresponding RefundStatus.

        Args:
            name (str): The name of the refund status (case insensitive).

        Returns:
            RefundStatus: The corresponding RefundStatus instance.

        Raises:
            ValueError: If the name does not match any valid refund status.
        """
        try:
            return cls[name.upper()]  # Ensure case insensitivity
        except KeyError:
            raise ValueError(f"Invalid payment status name: {name}")

    def __str__(self):
        """
        Return the string representation of the RefundStatus enum.

        Returns:
            str: The value of the enum.
        """
        return str(self.value)


class CancellationReason(Enum):
    """
    Enum representing the different reasons for transaction cancellations.
    """

    DUPLICATE = "duplicate"
    FRAUDULENT = "fraudulent"
    REQUESTED_BY_CUSTOMER = "requested"
    ABANDONED = "abandoned"
    AUTOMATIC = "automatic"
    WITHOUT_ORIGINAL = "without_original"

    @classmethod
    def from_name(cls, name: str) -> "CancellationReason":
        """
        Convert a string name to a corresponding CancellationReason.

        Args:
            name (str): The name of the cancellation reason (case insensitive).

        Returns:
            CancellationReason: The corresponding CancellationReason instance.

        Raises:
            ValueError: If the name does not match any valid cancellation reason.
        """
        try:
            return cls[name.upper()]  # Ensure case insensitivity
        except KeyError:
            raise ValueError(f"Invalid cancellation reason name: {name}")

    def __str__(self):
        """
        Return the string representation of the CancellationReason enum.

        Returns:
            str: The value of the enum.
        """
        return str(self.value)


class Refund(BaseModel):
    """
    Represents a refund transaction with various attributes such as amount, currency, status, etc.

    Attributes:
        id (str): Unique identifier for the refund.
        object (str): Type of the object, always 'refund'.
        amount (int): Amount to be refunded in the smallest currency unit.
        currency (str): Currency code following ISO 4217 alpha-3 format.
        order (str): Order identifier.
        created (int): Timestamp of refund creation in seconds since Unix epoch.
        payment_id (Optional[str]): Original payment ID.
        authorization (Optional[str]): Authorization identifier if available.
        status (RefundStatus): Status of the refund.
        cancellation_reason (Optional[CancellationReason]): Reason for refund cancellation.
        metadata (Optional[Dict[str, Union[str, int, float, bool]]]): Additional metadata related to the refund.
        payment_method (str): Payment method used, default is 'bizum'.
        operation_id (Optional[str]): Bizum operation ID.
    """

    id: str = Field(
        default_factory=lambda: str(Ksuid()),
        description="Unique identifier for the refund.",
    )
    object: str = Field(
        default="refund", description="Type of the object, always 'refund'."
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
        description="Timestamp of when the refund was created, measured in seconds since Unix epoch.",
    )
    payment_id: Optional[str] = Field(None, description="Original payment id")
    authorization: Optional[str] = Field(
        None, description="Authorization identifier if available."
    )
    status: RefundStatus = Field(..., description="Status of the refund.")
    cancellation_reason: Optional[CancellationReason] = Field(
        None, description="Reason for the payment cancellation."
    )
    metadata: Optional[Dict[str, Union[str, int, float, bool]]] = Field(
        default_factory=dict, description="Additional metadata related to the refund."
    )
    # phone: Optional[str] = Field(None, description="Customer's phone number associated with the payment.")
    payment_method: str = Field(
        default="bizum", description="Payment method used, default is 'bizum'."
    )
    operation_id: Optional[str] = Field(default=None, description="Bizum operation id")
    # truncated_account: Optional[str] = Field(default=None, description="Bizum truncated account")

    def cancel(self, reason: CancellationReason) -> None:
        """
        Cancel the refund and provide a reason for cancellation.

        Args:
            reason (CancellationReason): The reason why the refund was canceled.
        """
        self.status = RefundStatus.CANCELED
        self.cancellation_reason = reason