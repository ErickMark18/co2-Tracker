# CO2 Tracker

Estimates and visualizes the carbon footprint of GitHub Actions deployments based on server region and size.

![CO2](https://co2-tracker.up.railway.app/badge/ErickMark18/co2-Tracker)

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  GitHub Actions │────▶│   FastAPI API   │────▶│   PostgreSQL    │
│  workflow_run   │     │   Railway       │     │   (persistent)  │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
              ┌─────▼─────┐ ┌───▼────┐ ┌────▼────┐
              │ /dashboard│ │/badge  │ │ /stats  │
              │ (Chart.js)│ │ (SVG)  │ │ (JSON)  │
              └───────────┘ └────────┘ └─────────┘
```

## Quick Start

### 1. Run with Docker

```bash
docker compose up
```

API available at http://localhost:8000

### 2. Or run locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start API
python -m src.api

# Start CLI
python -m src.calculate --duration 300 --region eu-north-1 --size medium
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/deploys` | POST | Create deploy (requires `X-API-Key`) |
| `/deploys` | GET | List deploys with filters |
| `/deploys/{id}` | GET | Get single deploy |
| `/stats` | GET | Aggregated statistics |
| `/badge/{repo}` | GET | SVG badge (shields.io style) |
| `/dashboard` | GET | Web dashboard |
| `/region/alternative` | GET | Best alternative region |

## Deploy to Railway

1. Fork or clone this repo
2. Create a new project in [Railway](https://railway.app)
3. Connect your GitHub repo
4. Add a PostgreSQL database to the project
5. Add environment variables:
   - `CO2_API_KEY`: Your API key
   - `DATABASE_URL`: (auto-generated when you add PostgreSQL)
6. Railway auto-detects Python and deploys

## GitHub Actions Integration

1. Deploy the API to Railway
2. Add GitHub Secrets to each repo you want to track:
   - `CO2_API_URL`: Your Railway URL (e.g., `https://co2-tracker.up.railway.app`)
   - `CO2_API_KEY`: Your API key

3. Copy `.github/workflows/co2-tracker.yml` to your repos

Or use the [CO2 Tracker Template](https://github.com/ErickMark18/co2-tracker-template) to bootstrap new repos.

## For Other Repos

Use the [co2-tracker-template](https://github.com/ErickMark18/co2-tracker-template) repository as a template for new projects. It includes the workflow file and instructions.

## CO2 Calculation

```
CO2 (g) = (duration_s / 3600) * power_kW * PUE * carbon_intensity_g_per_kWh
```

- **PUE**: 1.45
- **Runner power (kW)**: small=1.7, medium=3.5, large=6.5
- **Carbon intensity**: varies by region (g CO2/kWh)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CO2_API_KEY` | `dev-api-key-change-me` | API authentication key |
| `ELECTRICITY_MAPS_TOKEN` | (none) | electricityMaps API token for real-time data |
| `DATABASE_URL` | (none) | PostgreSQL connection string |

## Project Structure

```
co2-Tracker/
├── src/
│   ├── api.py             # FastAPI application
│   ├── carbon.py          # Static carbon intensity data
│   ├── calculate.py       # CO2 calculation engine + CLI
│   ├── database.py        # SQLAlchemy models (PostgreSQL/SQLite)
│   ├── models.py          # Pydantic schemas
│   └── electricity_maps.py # electricityMaps API integration
├── tests/
│   ├── test_api.py         # API tests
│   └── test_carbon.py     # Calculation tests
├── dashboard/
│   └── index.html          # Dashboard UI
├── .github/workflows/
│   └── co2-tracker.yml    # GitHub Actions workflow
├── Dockerfile
├── docker-compose.yml
├── requirements.txt        # Python dependencies
├── pyproject.toml
├── README.md
└── Agents.md              # Context for coding agents
```

## License

MIT License