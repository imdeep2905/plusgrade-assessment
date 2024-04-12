import pytest
import requests
from mock import patch

from app.api.core.tax import TaxCalculator
from app.api.models.tax import CalculateTaxResponse
from app.config import settings


def test_calculate_tax_successful_calculation(sample_tax_brackets):
    calculator = TaxCalculator()

    # Mocking the API call to fetch tax brackets
    with patch.object(calculator, "fetch_tax_brackets") as mock_fetch:
        mock_fetch.return_value = sample_tax_brackets["tax_brackets"]

        # Calculate taxes for a valid tax year and salary
        tax_year = 2022
        salary = 1234567
        response = calculator.calculate(tax_year, salary)

        assert response == CalculateTaxResponse(
            total_taxes=385587.65,
            taxes_per_band={
                "0 to 50197": 7529.55,
                "50197 to 100392": 10289.97,
                "100392 to 155625": 14360.58,
                "155625 to 221708": 19164.07,
                "More than 221708": 334243.47,
            },
            effective_rate=31.23,
        )

        # Calculate tax for 0 salary
        response = calculator.calculate(tax_year, 0)

        assert response == CalculateTaxResponse(
            total_taxes=0,
            taxes_per_band={
                "0 to 50197": 0,
                "50197 to 100392": 0,
                "100392 to 155625": 0,
                "155625 to 221708": 0,
                "More than 221708": 0,
            },
            effective_rate=0,
        )


def test_calculate_tax_invalid_inputs():
    calculator = TaxCalculator()

    # Calculate taxes for an invalid tax year
    with pytest.raises(ValueError) as exc_info:
        calculator.calculate(settings.tax_calculator_supported_years[-1] + 1, 10000)
    assert "Tax year is not supported" in str(exc_info.value)

    # Calculate taxes for a negative salary
    with pytest.raises(ValueError) as exc_info:
        calculator.calculate(settings.tax_calculator_supported_years[0], -50000)
    assert "Salary can't be negative" in str(exc_info.value)


def test_fetch_tax_brackets(sample_tax_brackets):
    calculator = TaxCalculator()
    # Successful fetching of tax brackets
    with patch.object(requests, "get") as mock_get:
        mock_get.return_value.json.return_value = sample_tax_brackets
        assert (
            calculator.fetch_tax_brackets(2022) == sample_tax_brackets["tax_brackets"]
        )
