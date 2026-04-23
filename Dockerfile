FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer-cached)
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy source
COPY src/ src/

# Copy entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 9007

ENTRYPOINT ["./entrypoint.sh"]
