"""FastAPI application with CO2 tracking endpoints."""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Header, Query, Response
from fastapi.middleware.cors import CORSMiddleware

from src.database import init_db, get_session, Deploy
from src.models import (
    DeployCreate,
    DeployResponse,
    DeployListResponse,
    StatsResponse,
    HealthResponse,
)
from src.calculate import calculate_co2
from src.electricity_maps import get_carbon_intensity_from_api, get_carbon_intensity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.environ.get("CO2_API_KEY", "dev-api-key-change-me")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="CO2 Tracker API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://co2-tracker-production.up.railway.app", "https://co2-tracker.up.railway.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", version="1.0.0")


@app.post("/deploys", response_model=DeployResponse, dependencies=[Depends(verify_api_key)])
async def create_deploy(deploy: DeployCreate):
    carbon_intensity = await get_carbon_intensity_from_api(deploy.region, deploy.provider)

    if carbon_intensity is None:
        carbon_intensity = get_carbon_intensity(deploy.region, deploy.provider)
        logger.info(f"Using static intensity for {deploy.region}/{deploy.provider}: {carbon_intensity}")
    else:
        logger.info(f"Using ElectricityMaps intensity for {deploy.region}/{deploy.provider}: {carbon_intensity}")

    co2_grams = calculate_co2(
        deploy.duration_s,
        deploy.region,
        deploy.runner_size,
        deploy.provider,
    )

    db = get_session()
    try:
        db_deploy = Deploy(
            repo=deploy.repo,
            branch=deploy.branch,
            region=deploy.region,
            provider=deploy.provider,
            duration_s=deploy.duration_s,
            runner_size=deploy.runner_size,
            co2_grams=co2_grams,
            carbon_intensity=carbon_intensity,
            timestamp=datetime.now(timezone.utc),
            commit_sha=deploy.commit_sha,
            workflow_name=deploy.workflow_name,
        )
        db.add(db_deploy)
        db.commit()
        db.refresh(db_deploy)
        return db_deploy
    finally:
        db.close()


@app.get("/deploys", response_model=DeployListResponse)
def list_deploys(
    repo: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
):
    db = get_session()
    try:
        query = db.query(Deploy)

        if repo:
            query = query.filter(Deploy.repo == repo)
        if from_date:
            query = query.filter(Deploy.timestamp >= from_date)
        if to_date:
            query = query.filter(Deploy.timestamp <= to_date)

        total = query.count()
        deploys = query.order_by(Deploy.timestamp.desc()).offset(offset).limit(limit).all()

        return DeployListResponse(deploys=deploys, total=total)
    finally:
        db.close()


@app.get("/deploys/{deploy_id}", response_model=DeployResponse)
def get_deploy(deploy_id: int):
    db = get_session()
    try:
        deploy = db.query(Deploy).filter(Deploy.id == deploy_id).first()
        if not deploy:
            raise HTTPException(status_code=404, detail="Deploy not found")
        return deploy
    finally:
        db.close()


@app.get("/stats", response_model=StatsResponse)
def get_stats(
    repo: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
):
    db = get_session()
    try:
        query = db.query(Deploy)

        if repo:
            query = query.filter(Deploy.repo == repo)
        if from_date:
            query = query.filter(Deploy.timestamp >= from_date)
        if to_date:
            query = query.filter(Deploy.timestamp <= to_date)

        deploys = query.all()
        total_deploys = len(deploys)

        if total_deploys == 0:
            return StatsResponse(
                total_deploys=0,
                total_co2_g=0.0,
                avg_co2_g=0.0,
                by_region={},
                by_repo={},
            )

        total_co2 = sum(d.co2_grams for d in deploys)
        avg_co2 = total_co2 / total_deploys

        by_region: dict[str, dict[str, float]] = {}
        for d in deploys:
            if d.region not in by_region:
                by_region[d.region] = {"count": 0, "total_co2_g": 0.0}
            by_region[d.region]["count"] += 1
            by_region[d.region]["total_co2_g"] += d.co2_grams

        by_repo: dict[str, dict[str, float]] = {}
        for d in deploys:
            if d.repo not in by_repo:
                by_repo[d.repo] = {"count": 0, "total_co2_g": 0.0}
            by_repo[d.repo]["count"] += 1
            by_repo[d.repo]["total_co2_g"] += d.co2_grams

        return StatsResponse(
            total_deploys=total_deploys,
            total_co2_g=round(total_co2, 4),
            avg_co2_g=round(avg_co2, 4),
            by_region=by_region,
            by_repo=by_repo,
        )
    finally:
        db.close()


@app.get("/badge/{repo}")
def get_badge(repo: str):
    db = get_session()
    try:
        deploy = db.query(Deploy).filter(Deploy.repo == repo).order_by(Deploy.timestamp.desc()).first()
        if not deploy:
            svg = generate_badge_svg("no data", "0 g", "#9ca3af", "#6b7280")
            return Response(content=svg, media_type="image/svg+xml")

        if deploy.co2_grams < 1:
            label = f"{deploy.co2_grams * 1000:.1f} mg"
        elif deploy.co2_grams < 1000:
            label = f"{deploy.co2_grams:.1f} g"
        else:
            label = f"{deploy.co2_grams / 1000:.2f} kg"

        if deploy.co2_grams < 50:
            color = "#22c55e"
        elif deploy.co2_grams < 200:
            color = "#eab308"
        else:
            color = "#ef4444"

        svg = generate_badge_svg("CO2", label, color, "#ffffff")
        return Response(content=svg, media_type="image/svg+xml")
    finally:
        db.close()


@app.get("/region/alternative")
def get_alternative_region(
    region: str = Query(...),
    provider: str = Query("aws"),
):
    from src.carbon import AWS_REGION_INTENSITY, AZURE_REGION_INTENSITY, GCP_REGION_INTENSITY

    intensity_map = {
        "aws": AWS_REGION_INTENSITY,
        "azure": AZURE_REGION_INTENSITY,
        "gcp": GCP_REGION_INTENSITY,
    }

    current_intensity = intensity_map.get(provider, {}).get(region, 400)

    all_regions = intensity_map.get(provider, {})
    alternatives = [
        (r, i) for r, i in all_regions.items() if i < current_intensity
    ]
    alternatives.sort(key=lambda x: x[1])

    if not alternatives:
        return {"current_region": region, "current_intensity": current_intensity, "alternative_region": None, "potential_saving_percent": 0}

    best_region, best_intensity = alternatives[0]
    saving_percent = ((current_intensity - best_intensity) / current_intensity) * 100

    return {
        "current_region": region,
        "current_intensity": current_intensity,
        "alternative_region": best_region,
        "alternative_intensity": best_intensity,
        "potential_saving_percent": round(saving_percent, 1),
    }


def generate_badge_svg(label: str, value: str, color: str, text_color: str) -> str:
    label_width = len(label) * 6 + 10
    value_width = len(value) * 7 + 10
    total_width = label_width + value_width

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20">
  <rect x="0" y="0" width="{label_width}" height="20" rx="4" fill="#64748b"/>
  <text x="{label_width / 2}" y="14" text-anchor="middle" font-family="monospace" font-size="11" fill="#f1f5f9" font-weight="600">{label}</text>
  <rect x="{label_width}" y="0" width="{value_width}" height="20" rx="4" fill="{color}"/>
  <text x="{label_width + value_width / 2}" y="14" text-anchor="middle" font-family="monospace" font-size="11" fill="{text_color}" font-weight="600">{value}</text>
</svg>'''
    return svg


@app.get("/dashboard")
def get_dashboard():
    from pathlib import Path
    dashboard_path = Path(__file__).parent.parent / "dashboard" / "index.html"
    from fastapi.responses import FileResponse
    return FileResponse(dashboard_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)