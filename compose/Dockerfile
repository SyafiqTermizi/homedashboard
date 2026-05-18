FROM python:3.13.13-slim-bookworm AS python-build-stage

# Install curl and clean up to keep the image small
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

WORKDIR /app/
COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/
RUN uv export --format requirements-txt --output-file requirements.txt
RUN pip wheel --wheel-dir /usr/src/app/wheels  -r requirements.txt

FROM python:3.13.13-slim-bookworm AS python-run-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/
