# Dockerfile
FROM python:3.11-slim

# install curl (health check helper) and build essentials if needed
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# default command (can be overridden in compose)
CMD ["python", "vardhman_price_exporter.py"]
