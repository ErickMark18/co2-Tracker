"""CO2 calculation engine for deployment carbon footprint."""

import argparse
from typing import Literal

from src.carbon import (
    AWS_REGION_INTENSITY,
    AZURE_REGION_INTENSITY,
    GCP_REGION_INTENSITY,
    RUNNER_POWER,
    PUE,
)

Provider = Literal["aws", "azure", "gcp"]


def get_carbon_intensity(region: str, provider: Provider = "aws") -> int:
    if provider == "aws":
        return AWS_REGION_INTENSITY.get(region, 400)
    elif provider == "azure":
        return AZURE_REGION_INTENSITY.get(region, 400)
    elif provider == "gcp":
        return GCP_REGION_INTENSITY.get(region, 400)
    return 400


def calculate_co2(duration_s: float, region: str, runner_size: str = "medium", provider: Provider = "aws") -> float:
    """
    Calculate CO₂ emissions in grams for a deployment.

    Formula: duration_s x power_kW x PUE x carbon intensity in g CO2/kWh / 3600

    Args:
        duration_s: Duration of the deployment in seconds
        region: Cloud region (e.g., 'eu-north-1' for AWS)
        runner_size: Size of the runner ('small', 'medium', 'large')
        provider: Cloud provider ('aws', 'azure', 'gcp')

    Returns:
CO2 emissions in grams
    """
    power_kw = RUNNER_POWER.get(runner_size, 3.5)
    carbon_intensity = get_carbon_intensity(region, provider)
    co2_grams = (duration_s / 3600) * power_kw * PUE * carbon_intensity
    return round(co2_grams, 4)


def main():
    parser = argparse.ArgumentParser(description="Calculate CO2 emissions for a deployment")
    parser.add_argument("--duration", type=float, required=True, help="Duration in seconds")
    parser.add_argument("--region", type=str, required=True, help="Cloud region (e.g., eu-north-1)")
    parser.add_argument("--size", type=str, default="medium", choices=["small", "medium", "large"], help="Runner size")
    parser.add_argument("--provider", type=str, default="aws", choices=["aws", "azure", "gcp"], help="Cloud provider")
    args = parser.parse_args()

    co2 = calculate_co2(args.duration, args.region, args.size, args.provider)
    intensity = get_carbon_intensity(args.region, args.provider)

    print(f"Deployment CO2 Calculator")
    print(f"=" * 40)
    print(f"Region: {args.region} ({args.provider})")
    print(f"Duration: {args.duration}s ({args.duration / 60:.1f} min)")
    print(f"Runner size: {args.size} ({RUNNER_POWER.get(args.size, 3.5)} kW)")
    print(f"PUE: {PUE}")
    print(f"Carbon intensity: {intensity} g CO2/kWh")
    print(f"-" * 40)
    print(f"CO2 emissions: {co2:.4f} g")


if __name__ == "__main__":
    main()