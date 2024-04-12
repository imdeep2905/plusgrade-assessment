from typing import Annotated, Dict

from pydantic import BaseModel, Field, field_validator


class CalculateTaxResponse(BaseModel):
    """Response model for tax calculation."""

    total_taxes: Annotated[float, Field(ge=0)]  # Total taxes amount
    taxes_per_band: Dict[str, Annotated[float, Field(ge=0)]]  # Taxes per income band
    effective_rate: Annotated[float, Field(ge=0, le=100.0)]  # Effective tax rate in %

    @field_validator("total_taxes", "effective_rate")
    def round_float(cls, v: float) -> float:
        """Round float values to two decimal places."""
        return round(v, 2)

    @field_validator("taxes_per_band")
    def round_float_dict(cls, v: dict[str, float]) -> dict[str, float]:
        """Round float values in dictionary to two decimal places."""
        return {k: round(val, 2) for k, val in v.items()}
