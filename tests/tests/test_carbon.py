"""Tests for CO₂ calculation engine."""

import pytest
from src.calculate import calculate_co2, get_carbon_intensity


class TestCarbonIntensity:
    def test_aws_regions_exist(self):
        assert get_carbon_intensity("eu-north-1", "aws") == 27
        assert get_carbon_intensity("us-east-1", "aws") == 453
        assert get_carbon_intensity("ap-southeast-2", "aws") == 502

    def test_azure_regions_exist(self):
        assert get_carbon_intensity("northeurope", "azure") == 27
        assert get_carbon_intensity("westeurope", "azure") == 233

    def test_gcp_regions_exist(self):
        assert get_carbon_intensity("europe-north1", "gcp") == 27
        assert get_carbon_intensity("us-east1", "gcp") == 453

    def test_unknown_region_fallback(self):
        assert get_carbon_intensity("unknown-region", "aws") == 400


class TestCO2Calculation:
    def test_stockholm_vs_sydney_ratio(self):
        stockholm_co2 = calculate_co2(duration_s=300, region="eu-north-1", runner_size="medium", provider="aws")
        sydney_co2 = calculate_co2(duration_s=300, region="ap-southeast-2", runner_size="medium", provider="aws")
        assert stockholm_co2 < sydney_co2
        assert sydney_co2 / stockholm_co2 > 15

    def test_sydney_vs_stockholm_5min_deploy(self):
        stockholm = calculate_co2(300, "eu-north-1", "medium", "aws")
        sydney = calculate_co2(300, "ap-southeast-2", "medium", "aws")
        ratio = sydney / stockholm
        assert 15 < ratio < 25

    def test_different_runner_sizes(self):
        small = calculate_co2(300, "eu-north-1", "small", "aws")
        medium = calculate_co2(300, "eu-north-1", "medium", "aws")
        large = calculate_co2(300, "eu-north-1", "large", "aws")
        assert small < medium < large
        assert medium / small > 1.5
        assert large / medium > 1.5

    def test_duration_proportionality(self):
        five_min = calculate_co2(300, "eu-north-1", "medium", "aws")
        ten_min = calculate_co2(600, "eu-north-1", "medium", "aws")
        assert ten_min == pytest.approx(five_min * 2, rel=0.001)

    def test_result_in_grams(self):
        result = calculate_co2(3600, "eu-north-1", "medium", "aws")
        assert 0 < result < 500

    def test_zero_duration(self):
        result = calculate_co2(0, "eu-north-1", "medium", "aws")
        assert result == 0