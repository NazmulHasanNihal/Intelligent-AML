# Stage 1: Build & Dependencies
FROM python:3.11-slim AS builder
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git libgomp1 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt pyproject.toml ./
RUN pip install --user --no-warn-script-location -r requirements.txt

# Stage 2: Hardened Non-Root Distroless-Style Runtime
FROM python:3.11-slim AS runner
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PATH="/home/amlapp/.local/bin:${PATH}"
RUN groupadd -g 10001 amlgroup && \
    useradd -u 10001 -g amlgroup -s /bin/bash -m amlapp && \
    apt-get update && apt-get install -y --no-install-recommends libgomp1 curl && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder --chown=amlapp:amlgroup /root/.local /home/amlapp/.local
COPY --chown=amlapp:amlgroup src/ ./src/
COPY --chown=amlapp:amlgroup configs/ ./configs/
COPY --chown=amlapp:amlgroup pyproject.toml ./
RUN pip install --no-deps -e .
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
ENTRYPOINT ["uvicorn", "src.engine.api:app", "--host", "0.0.0.0", "--port", "8000"]
