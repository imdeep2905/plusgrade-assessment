# Tax-Calculator (Plusgrade take home assessment)

## How to Run

### Run locally

First set environment variable for tax brackets API by running `EXPORT TAX_CALCULATOR_API_URL=<url>`. If not set, the default URL (i.e. `http://localhost:5001/tax-calculator/tax-year`) will be used.

1. Install poetry `pip install poetry`.
2. Run `poetry install`.
3. Run `poetry run uvicorn app.main:app --reload `.

### Run inside a container

1. Build container by running `docker build -t tax-calculator  .`.
2. Run docker container by running `docker run -d -p 8000:8000  tax-calculator -e TAX_CALCULATOR_API_URL="<url>"`.

## Tools used

- Poetry
- FastAPI
- Ruff
- MyPy
- Pytest

## Example API call

`GET /api/calculate-tax?tax_year=2022&salary=1234567`

```
{
    "total_taxes": 385587.65,
    "taxes_per_band": {
        "0 to 50197": 7529.55,
        "50197 to 100392": 10289.97,
        "100392 to 155625": 14360.58,
        "155625 to 221708": 19164.07,
        "More than 221708": 334243.47
    },
    "effective_rate": 31.23
}
```
