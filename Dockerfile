FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project metadata and source, then install only the local package.
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir --no-deps .

# Ensure src layout imports resolve even if install mode changes.
ENV PYTHONPATH=/app/src

# Copy entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 9007

ENTRYPOINT ["./entrypoint.sh"]
