FROM python:3.10

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000
# Run FastAPI
CMD ["cd", "app","fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]