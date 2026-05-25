"""Carbon intensity data by region for AWS, Azure and GCP (g CO2/kWh)."""

AWS_REGION_INTENSITY = {
    "us-east-1": 453,
    "us-east-2": 453,
    "us-west-1": 463,
    "us-west-2": 345,
    "eu-west-1": 309,
    "eu-west-2": 233,
    "eu-west-3": 53,
    "eu-north-1": 27,
    "eu-central-1": 362,
    "ap-southeast-1": 475,
    "ap-southeast-2": 502,
    "ap-northeast-1": 518,
    "ap-northeast-3": 506,
    "ap-south-1": 708,
    "sa-east-1": 88,
    "ca-central-1": 190,
}

AZURE_REGION_INTENSITY = {
    "eastus": 453,
    "eastus2": 453,
    "westus": 463,
    "westus2": 345,
    "westeurope": 233,
    "northeurope": 27,
    "uksouth": 309,
    "francecentral": 53,
    "germanywestcentral": 362,
    "switzerlandnorth": 29,
    "norwayeast": 20,
    "swedencentral": 22,
    "australiaeast": 502,
    "southeastasia": 475,
    "eastasia": 518,
    "southindia": 708,
    "brazilsouth": 88,
}

GCP_REGION_INTENSITY = {
    "us-east1": 453,
    "us-east4": 453,
    "us-central1": 453,
    "us-west1": 463,
    "us-west2": 345,
    "us-west3": 463,
    "us-west4": 345,
    "europe-west1": 233,
    "europe-west2": 53,
    "europe-west3": 362,
    "europe-west4": 27,
    "europe-west6": 29,
    "europe-north1": 27,
    "asia-east1": 518,
    "asia-east2": 506,
    "asia-southeast1": 475,
    "asia-south1": 708,
    "asia-northeast1": 518,
    "australia-southeast1": 502,
    "southamerica-east1": 88,
}

RUNNER_POWER = {
    "small": 1.7,
    "medium": 3.5,
    "large": 6.5,
}

PUE = 1.45