import logging

from fastapi import APIRouter, HTTPException, status

from app.api.core.tax import TaxCalculator
from app.api.models.tax import CalculateTaxResponse

# Get the logger for this module
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/calculate-tax",
    response_model=CalculateTaxResponse,
    description="Calculate taxes based on salary and tax year.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CalculateTaxResponse,
            "content": {
                "application/json": {
                    "example": {
                        "total_taxes": 385587.65,
                        "taxes_per_band": {
                            "0 to 50197": 7529.55,
                            "50197 to 100392": 10289.97,
                            "100392 to 155625": 14360.58,
                            "155625 to 221708": 19164.07,
                            "More than 221708": 334243.47,
                        },
                        "effective_rate": 31.23,
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad request - Invalid input",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid input. Possible reasons include: negative salary, unsupported tax year."
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error - Something went wrong on the server side",
        },
    },
)
async def calculate_tax(salary: float, tax_year: int) -> CalculateTaxResponse:
    """
    Calculate taxes based on salary and tax year.

    Args:
        `salary` (float): The salary amount.
        `tax_year` (int): The tax year.

    Returns:
        `CalculateTaxResponse`: The calculated tax response.

    Raises:
        `HTTPException`: If there's a bad request or internal server error.
    """
    try:
        tax_calculator = TaxCalculator()
        return tax_calculator.calculate(tax_year, salary)
    except ValueError as e:
        logger.debug(str(e))
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error."
        )
