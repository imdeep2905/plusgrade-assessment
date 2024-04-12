import logging
from functools import lru_cache

import requests
from singleton_decorator import singleton  # type: ignore
from tenacity import retry, stop_after_attempt, wait_fixed

from app.api.models.tax import CalculateTaxResponse
from app.config import settings

logger = logging.getLogger(__name__)


@singleton
class TaxCalculator:
    def __init__(self) -> None:
        self.tax_year_api_url = settings.tax_calculator_api_url
        logger.debug(f"TaxCalculator initialized with API URL: {self.tax_year_api_url}")

    @retry(
        stop=stop_after_attempt(settings.tax_calculator_retries),
        wait=wait_fixed(settings.tax_calculator_wait_time),
        retry_error_callback=lambda retry_state: logger.warning(
            f"Retry attempt {retry_state.attempt_number} for fetching tax brackets failed with error: {retry_state.outcome.exception()}"
            if retry_state.outcome
            else f"Retry attempt {retry_state.attempt_number} for fetching tax brackets failed with no outcome available"
        ),
        reraise=True,
    )
    @lru_cache(maxsize=5)  # Cache results to reduce API calls
    def fetch_tax_brackets(self, tax_year: int) -> dict:
        """
        Fetches tax brackets for a given tax year. Retries are attempted
        for a configured number of times if the API call fails.

        Args:
            tax_year (int): The tax year.

        Returns:
            dict: The tax brackets data.
        """
        url = f"{self.tax_year_api_url}/{tax_year}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("tax_brackets")

    def calculate(self, tax_year: int, salary: float) -> CalculateTaxResponse:
        """
        Calculate taxes based on tax year and salary.

        Args:
            `tax_year` (int): The tax year.
            `salary` (float): The salary amount.

        Returns:
            `CalculateTaxResponse`: The calculated tax response.

        Raises:
            `ValueError`: If tax year is not supported or salary is negative.
        """
        if tax_year not in settings.tax_calculator_supported_years:
            raise ValueError(
                f"Tax year is not supported yet. Supported years are {settings.tax_calculator_supported_years}."
            )

        if salary < 0:
            raise ValueError("Salary can't be negative.")

        tax_brackets = self.fetch_tax_brackets(tax_year)
        total_taxes = 0.0
        taxes_per_band: dict[str, float] = {}
        effective_rate = 0.0

        for bracket in tax_brackets:
            if "max" in bracket and "min" in bracket:
                band_label = f"{bracket['min']} to {bracket['max']}"
            else:
                band_label = f"More than {bracket['min']}"  # For last bracket

            taxes_per_band[band_label] = 0

            # If max is not there salary is considered max
            max_income = min(bracket.get("max", salary), salary)
            min_income = bracket["min"]
            rate = bracket["rate"]

            # Taxable income for this bracket
            taxable_income = max_income - min_income

            if taxable_income > 0:
                tax_for_band = taxable_income * rate
                total_taxes += tax_for_band
                taxes_per_band[band_label] = tax_for_band

        if salary > 0:
            effective_rate = (total_taxes / salary) * 100

        return CalculateTaxResponse(
            total_taxes=total_taxes,
            taxes_per_band=taxes_per_band,
            effective_rate=effective_rate,
        )
