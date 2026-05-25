"""Pydantic models for API request/response schemas."""

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field, ConfigDict

Provider = Literal["aws", "azure", "gcp"]


class DeployCreate(BaseModel):
    repo: str = Field(..., description="Repository name (e.g., 'owner/project')")
    branch: str = Field(..., description="Branch name")
    region: str = Field(..., description="Cloud region (e.g., 'eu-north-1')")
    provider: Provider = Field(default="aws", description="Cloud provider")
    duration_s: float = Field(..., gt=0, description="Duration in seconds")
    runner_size: str = Field(default="medium", description="Runner size: small, medium, large")
    commit_sha: Optional[str] = Field(None, description="Git commit SHA")
    workflow_name: Optional[str] = Field(None, description="Workflow name")


class DeployResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    repo: str
    branch: str
    region: str
    provider: str
    duration_s: float
    runner_size: str
    co2_grams: float
    carbon_intensity: float
    timestamp: datetime
    commit_sha: Optional[str]
    workflow_name: Optional[str]


class DeployListResponse(BaseModel):
    deploys: list[DeployResponse]
    total: int


class StatsResponse(BaseModel):
    total_deploys: int
    total_co2_g: float
    avg_co2_g: float
    by_region: dict[str, dict[str, float]]
    by_repo: dict[str, dict[str, float]]


class HealthResponse(BaseModel):
    status: str
    version: str