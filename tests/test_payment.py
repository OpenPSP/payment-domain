from payment_domain import CancellationReason, Payment, PaymentStatus


def test_payment_initialization():
    """Test that the Payment class is initialized correctly with required fields."""
    payment = Payment(
        id="payment_12345",
        amount=1000,
        currency="EUR",
        order="order_001",
        status=PaymentStatus.CREATED
    )

    assert payment.id == "payment_12345"
    assert payment.amount == 1000
    assert payment.currency == "EUR"
    assert payment.order == "order_001"
    assert payment.status == PaymentStatus.CREATED


def test_payment_cancel():
    """Test that canceling a payment sets the correct status and cancellation reason."""
    payment = Payment(
        id="payment_12345",
        amount=1000,
        currency="EUR",
        order="order_001",
        status=PaymentStatus.CREATED
    )

    payment.cancel(reason=CancellationReason.REQUESTED_BY_CUSTOMER)

    assert payment.status == PaymentStatus.CANCELED
    assert payment.cancellation_reason == CancellationReason.REQUESTED_BY_CUSTOMER
    assert payment.canceled_at is not None


def test_payment_status_transitions():
    """Test payment status transitions."""
    payment = Payment(
        id="payment_12345",
        amount=1000,
        currency="EUR",
        order="order_001",
        status=PaymentStatus.CREATED
    )

    payment.mark_succeeded()
    assert payment.status == PaymentStatus.SUCCEEDED

    payment.require_action()
    assert payment.status == PaymentStatus.REQUIRES_ACTION

    payment.confirm()
    assert payment.status == PaymentStatus.PROCESSING


def test_update_metadata():
    """Test that updating metadata works as expected."""
    payment = Payment(
        id="payment_12345",
        amount=1000,
        currency="EUR",
        order="order_001",
        status=PaymentStatus.CREATED
    )

    payment.update_metadata('customer_id', 'cust_123')
    assert payment.metadata['customer_id'] == 'cust_123'