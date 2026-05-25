FROM python:3.14-slim

WORKDIR /app

COPY src/ ./src/
COPY dashboard/ ./dashboard/
COPY tests/ ./tests/
COPY requirements.txt ./
COPY pyproject.toml ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "-m", "src.api"]