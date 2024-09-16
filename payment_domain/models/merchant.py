from pydantic import BaseModel, Field


class Merchant(BaseModel):
    """
    Represents a merchant with its unique identifier, name, FUC, and terminal.

    Attributes:
        id (str): Unique identifier for the merchant.
        name (str): Name of the merchant.
        fuc (str): Merchant's commerce code (FUC), which is a numerical code up to 9 digits.
        terminal (str): The terminal number of the merchant, which is a numerical code up to 3 digits.
    """

    id: str = Field(default="", description="Merchant unique identifier.")
    name: str = Field(default="", description="Merchant name.")
    fuc: str = Field(
        ..., description="The commerce code of the store.", pattern=r"^\d{1,9}$"
    )
    terminal: str = Field(
        ..., description="The terminal number of the merchant.", pattern=r"^\d{1,3}$"
    )
