from fastapi import status
from mock import patch

from app.api.core.tax import TaxCalculator


def test_calculate_tax_successful(client, sample_tax_calculation):
    # Need to mock '_instance' because TaxCalculator is singleton
    with patch.object(TaxCalculator, "_instance") as mock_instance:
        mock_instance.calculate.return_value = sample_tax_calculation
        response = client.get("api/calculate-tax?salary=100000&tax_year=2022")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == sample_tax_calculation


def test_calculate_tax_value_error(client):
    with patch.object(TaxCalculator, "_instance") as mock_instance:
        mock_instance.calculate.side_effect = ValueError(
            "Something went wrong"
        )  # Force ValueError
        response = client.get("api/calculate-tax?salary=-1000&tax_year=2022")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_calculate_tax_internal_server_error(client):
    with patch.object(TaxCalculator, "_instance") as mock_instance:
        mock_instance.calculate.side_effect = Exception(
            "Something went wrong"
        )  # Force generic exception
        response = client.get("api/calculate-tax?salary=100000&tax_year=2022")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Internal server error" in response.json()["detail"]
