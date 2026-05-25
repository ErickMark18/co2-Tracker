# Agents.md

## Project Overview

CO2 Tracker estimates and visualizes the carbon footprint of GitHub Actions deployments based on server region and size.

## Development Environment

- **Python**: 3.14+
- **Test Runner**: pytest
- **Run tests**: `py -3 -m pytest tests/ -v`
- **Start API**: `py -3 -m src.api` (runs on http://localhost:8000)

## Project Structure

```
co2-Tracker/
├── src/
│   ├── __init__.py
│   ├── carbon.py          # Static carbon intensity data by region
│   ├── calculate.py       # CO2 calculation engine + CLI
│   ├── database.py        # SQLAlchemy models (PostgreSQL/SQLite)
│   ├── models.py          # Pydantic request/response schemas
│   ├── electricity_maps.py # ElectricityMaps API integration
│   └── api.py             # FastAPI application
├── tests/
│   ├── conftest.py
│   ├── test_carbon.py
│   └── test_api.py
├── dashboard/
│   └── index.html         # Dashboard UI with Chart.js
├── .github/
│   └── workflows/
│       └── co2-tracker.yml  # GitHub Actions workflow
├── Dockerfile
├── requirements.txt        # Python dependencies
├── pyproject.toml
├── README.md
└── Agents.md
```

## Running the CLI

```bash
py -3 -m src.calculate --duration 300 --region eu-north-1 --size medium
```

## Running the API

```bash
pip install -r requirements.txt
py -3 -m src.api
```

## API Endpoints

- `GET /health` - Health check
- `POST /deploys` - Create deploy record (requires `X-API-Key` header)
- `GET /deploys` - List deploys with filters (?repo=...&from_date=...&to_date=...)
- `GET /deploys/{id}` - Get single deploy
- `GET /stats` - Aggregated statistics
- `GET /badge/{repo}` - SVG badge for last deploy CO2 (shields.io style)
- `GET /dashboard` - Web dashboard UI
- `GET /region/alternative?region=...&provider=...` - Best alternative region

## API Authentication

Set `CO2_API_KEY` environment variable. Default for development: `dev-api-key-change-me`

## Dashboard

Access at `http://localhost:8000/dashboard` when API is running.

Features:
- Total deploys, CO2, and average stats
- Emissions over time (line chart)
- Top repos by CO2 (ranking list)
- Emissions by region (bar chart)
- Alternative region suggestion with potential savings

## Badge

Add to README.md:
```markdown
![CO2](https://co2-tracker.up.railway.app/badge/owner/repo)
```

Badge colors:
- Green: < 50g CO2
- Yellow: 50-200g CO2
- Red: > 200g CO2

## CO2 Calculation Formula

```
CO2 (g) = (duration_s / 3600) * power_kW * PUE * carbon_intensity_g_per_kWh
```

- **PUE**: 1.45 (Power Usage Effectiveness)
- **Runner power (kW)**: small=1.7, medium=3.5, large=6.5
- **Carbon intensity**: varies by region (g CO2/kWh)

## Adding New Regions

Edit `src/carbon.py` and `src/electricity_maps.py` (zone mapping):

1. Add the region's carbon intensity to `AWS_REGION_INTENSITY`, `AZURE_REGION_INTENSITY`, or `GCP_REGION_INTENSITY`
2. Add zone mapping in `ZONE_MAP` for electricityMaps API
3. Run tests to verify: `py -3 -m pytest tests/ -v`

## ElectricityMaps API

- **Token**: Set via `ELECTRICITY_MAPS_TOKEN` environment variable
- API is called in real-time when creating deploys, with fallback to static data if it fails
- Zones mapped: SE, IE, GB, FR, DE, NL, CH, NO, FI, US, SG, AU-NSW, JP, IN, BR, CA, HK, TW

## GitHub Actions Integration

The workflow `.github/workflows/co2-tracker.yml` automatically tracks CO2 emissions from all workflow runs.

### Setup

1. Deploy the API to Railway (recommended) or Render
2. Add GitHub Secrets to each repo:
   - `CO2_API_URL`: Your API URL (e.g., `https://co2-tracker.up.railway.app`)
   - `CO2_API_KEY`: Your API key

### Workflow Behavior

- Runs on every `workflow_run` event and on push to master
- Extracts duration from `run_started_at` and `updated_at`
- Detects cloud region from `AWS_REGION`, `AZURE_REGION`, `GCP_REGION` env vars
- Falls back to `eu-north-1` if no region detected
- POSTs data to `/deploys` endpoint

### Testing Locally

To test the workflow locally, you can simulate a deploy:

```bash
Invoke-RestMethod -Uri "http://localhost:8000/deploys" -Method Post -ContentType "application/json" -Headers @{"X-API-Key"="dev-api-key-change-me"} -Body '{"repo":"test/repo","branch":"main","region":"eu-north-1","duration_s":300}'
```

## Database

Uses PostgreSQL for production (Railway) with SQLite fallback for local development.

Connection is configured via `DATABASE_URL` environment variable. If not set, falls back to local SQLite file.

## Deployment

### Railway (Recommended)

1. Create project at [railway.app](https://railway.app)
2. Connect GitHub repo
3. Add PostgreSQL database
4. Add environment variables: `CO2_API_KEY`, `DATABASE_URL` (auto-generated)
5. Railway auto-deploys on push

### Docker

```bash
docker compose up
```

## Test Expectations

- Stockholm (eu-north-1) vs Sydney (ap-southeast-2) ratio for 5-min deploy: ~15-25x
- All 22 tests must pass before merging

## Template Repository

For adding CO2 tracking to other repos you can use:
https://github.com/ErickMark18/co2-tracker-template