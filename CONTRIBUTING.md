# Contributing to CO2 Tracker

Thank you for your interest in contributing!

## Adding New Cloud Regions

CO2 Tracker supports AWS, Azure, and GCP regions. To add a new region:

### 1. Add carbon intensity data

Edit `src/carbon.py`:

```python
AWS_REGION_INTENSITY = {
    # ... existing regions ...
    "new-region": 150,  # intensity in g CO2/kWh
}
```

### 2. Add electricityMaps zone mapping

Edit `src/electricity_maps.py` `ZONE_MAP`:

```python
ZONE_MAP = {
    "aws": {
        # ... existing mappings ...
        "new-region": "XX",  # electricityMaps zone code
    },
}
```

### 3. Test your changes

```bash
python -m pytest tests/ -v
```

### 4. Verify calculation

```bash
python -m src.calculate --duration 300 --region new-region --size medium --provider aws
```

## Adding New Cloud Providers

To add support for a new cloud provider (e.g., Oracle Cloud):

### 1. Add intensity data in `src/carbon.py`

```python
ORACLE_REGION_INTENSITY = {
    "us-phoenix-1": 456,
    "eu-frankfurt-1": 362,
}
```

### 2. Add to provider handling in `src/calculate.py`

```python
def get_carbon_intensity(region: str, provider: Provider = "aws") -> int:
    if provider == "aws":
        return AWS_REGION_INTENSITY.get(region, 400)
    # ... existing providers ...
    elif provider == "oracle":
        return ORACLE_REGION_INTENSITY.get(region, 400)
    return 400
```

### 3. Add zone mapping in `src/electricity_maps.py`

```python
ZONE_MAP = {
    "oracle": {
        "us-phoenix-1": "US",
        "eu-frankfurt-1": "DE",
    },
}
```

### 4. Update Pydantic model in `src/models.py`

```python
Provider = Literal["aws", "azure", "gcp", "oracle"]
```

## Testing Guidelines

- All tests must pass: `python -m pytest tests/ -v`
- New regions should have ratio test: Stockholm vs new region ~15-25x
- Add tests in `tests/test_carbon.py` for new providers

## Code Style

- Use type hints for all function parameters and return values
- Follow existing patterns for imports and module structure
- Use `Literal` types for provider choices

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-region`)
3. Add tests for new regions
4. Ensure all tests pass
5. Submit a pull request with description of changes

## Issues

Feel free to open issues for:
- Bug reports
- Feature requests
- New region additions
- Documentation improvements