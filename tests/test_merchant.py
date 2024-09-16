import pytest

from payment_domain import Merchant


def test_merchant_initialization():
    """Test that the Merchant class is initialized correctly."""
    merchant = Merchant(
        id="merchant_12345",
        name="Test Merchant",
        fuc="123456789",
        terminal="001"
    )

    assert merchant.id == "merchant_12345"
    assert merchant.name == "Test Merchant"
    assert merchant.fuc == "123456789"
    assert merchant.terminal == "001"


def test_merchant_validation():
    """Test that validation on the FUC and terminal fields works correctly."""
    with pytest.raises(ValueError):
        Merchant(
            id="merchant_12345",
            name="Invalid Merchant",
            fuc="invalid_fuc",  # Invalid FUC, should raise validation error
            terminal="001"
        )

    with pytest.raises(ValueError):
        Merchant(
            id="merchant_12345",
            name="Invalid Merchant",
            fuc="123456789",
            terminal="invalid_terminal"  # Invalid terminal, should raise validation error
        )