FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && \
    apt-get install -yq --no-install-recommends -o Dpkg::Use-Pty=0 \
      curl build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --no-root

RUN pip install --no-cache-dir "uvicorn[standard]>=0.30"

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn ${APP_MODULE:-app.main:app} --host 0.0.0.0 --port 8000 --workers ${WORKERS:-2}"]


