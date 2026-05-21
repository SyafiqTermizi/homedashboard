FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS python-build-stage

COPY pyproject.toml ./

WORKDIR /app/
RUN uv export --format requirements-txt --output-file requirements.txt
RUN pip wheel --wheel-dir /usr/src/app/wheels  -r requirements.txt

FROM python:3.13.13-slim-bookworm AS python-run-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN addgroup --system homedsb \
  && adduser --system --ingroup homedsb --home /home/homedsb homedsb

WORKDIR /app/

COPY --from=python-build-stage --chown=homedsb:homedsb /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY --chown=homedsb:homedsb .. /app/

RUN chown homedsb:homedsb /app

USER homedsb
