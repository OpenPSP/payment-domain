from payment_domain import CancellationReason, Refund, RefundStatus


def test_refund_initialization():
    """Test that the Refund class is initialized correctly with required fields."""
    refund = Refund(
        id="refund_12345",
        amount=500,
        currency="EUR",
        order="order_001",
        status=RefundStatus.CREATED
    )

    assert refund.id == "refund_12345"
    assert refund.amount == 500
    assert refund.currency == "EUR"
    assert refund.order == "order_001"
    assert refund.status == RefundStatus.CREATED


def test_refund_status_transitions():
    """Test refund status transitions."""
    refund = Refund(
        id="refund_12345",
        amount=500,
        currency="EUR",
        order="order_001",
        status=RefundStatus.CREATED
    )

    refund.status = RefundStatus.SUCCEEDED
    assert refund.status == RefundStatus.SUCCEEDED

    refund.status = RefundStatus.CANCELED
    assert refund.status == RefundStatus.CANCELED


def test_cancellation_reason():
    """Test assigning a cancellation reason to a refund."""
    refund = Refund(
        id="refund_12345",
        amount=500,
        currency="EUR",
        order="order_001",
        status=RefundStatus.CREATED
    )


    refund.cancel(reason=CancellationReason.REQUESTED_BY_CUSTOMER)
    assert refund.status == RefundStatus.CANCELED
    assert refund.cancellation_reason == CancellationReason.REQUESTED_BY_CUSTOMER