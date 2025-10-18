# Образ питона
FROM python:3.13-slim-bookworm AS py-builder

# Задаем рабочую директорию
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry \
  && poetry config virtualenvs.in-project true \
  && poetry install --only main --no-interaction --no-ansi \
  && rm -rf $(poetry config cache-dir)/{cache,artifacts}


FROM python:3.13-slim-bookworm

# копируем само приложение
COPY --from=py-builder /app /app

WORKDIR /app
ENV PATH="/app/.venv/bin:${PATH}"
