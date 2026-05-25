"""ElectricityMaps API integration with fallback to static data."""

import logging
import os
from typing import Optional

import httpx

from src.calculate import get_carbon_intensity as get_static_intensity

logger = logging.getLogger(__name__)

ELECTRICITY_MAPS_TOKEN = os.environ.get("ELECTRICITY_MAPS_TOKEN")

ZONE_MAP = {
    "aws": {
        "eu-north-1": "SE",
        "eu-west-1": "IE",
        "eu-west-2": "GB",
        "eu-west-3": "FR",
        "eu-central-1": "DE",
        "us-east-1": "US",
        "us-east-2": "US",
        "us-west-1": "US",
        "us-west-2": "US",
        "ap-southeast-1": "SG",
        "ap-southeast-2": "AU-NSW",
        "ap-northeast-1": "JP",
        "ap-northeast-3": "JP",
        "ap-south-1": "IN",
        "sa-east-1": "BR",
        "ca-central-1": "CA",
    },
    "azure": {
        "northeurope": "IE",
        "westeurope": "NL",
        "uksouth": "GB",
        "francecentral": "FR",
        "germanywestcentral": "DE",
        "switzerlandnorth": "CH",
        "norwayeast": "NO",
        "swedencentral": "SE",
        "australiaeast": "AU-NSW",
        "southeastasia": "SG",
        "eastasia": "HK",
        "southindia": "IN",
        "brazilsouth": "BR",
        "eastus": "US",
        "eastus2": "US",
        "westus": "US",
        "westus2": "US",
    },
    "gcp": {
        "europe-north1": "FI",
        "europe-west1": "BE",
        "europe-west2": "GB",
        "europe-west3": "DE",
        "europe-west4": "NL",
        "europe-west6": "CH",
        "asia-east1": "TW",
        "asia-east2": "HK",
        "asia-southeast1": "SG",
        "asia-south1": "IN",
        "asia-northeast1": "JP",
        "australia-southeast1": "AU-NSW",
        "southamerica-east1": "BR",
        "us-east1": "US",
        "us-east4": "US",
        "us-central1": "US",
        "us-west1": "US",
        "us-west2": "US",
        "us-west3": "US",
        "us-west4": "US",
    },
}


def get_zone_for_region(region: str, provider: str) -> Optional[str]:
    return ZONE_MAP.get(provider, {}).get(region)


async def get_carbon_intensity_from_api(region: str, provider: str = "aws") -> Optional[float]:
    if not ELECTRICITY_MAPS_TOKEN:
        logger.info("ELECTRICITY_MAPS_TOKEN not set, skipping API call")
        return None
    zone = get_zone_for_region(region, provider)
    if not zone:
        logger.info(f"No zone mapping for {provider}/{region}")
        return None

    url = f"https://api.electricitymaps.com/v3/carbon-intensity/latest?zone={zone}"
    headers = {"auth-token": ELECTRICITY_MAPS_TOKEN}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            logger.info(f"ElectricityMaps API response for {zone}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                intensity = data.get("carbonIntensity")
                logger.info(f"ElectricityMaps intensity for {zone}: {intensity}")
                return intensity
            else:
                logger.warning(f"ElectricityMaps API error: {response.status_code}")
    except Exception as e:
        logger.warning(f"ElectricityMaps API exception: {e}")

    return None


def get_carbon_intensity(region: str, provider: str = "aws") -> int:
    return get_static_intensity(region, provider)