FROM python:3.12-slim

WORKDIR /app

# Copy project metadata and source before install so package discovery works.
COPY pyproject.toml .
COPY src/ src/

# Install project into the image (non-editable for runtime stability).
RUN pip install --no-cache-dir .

# Ensure src layout imports resolve even if install mode changes.
ENV PYTHONPATH=/app/src

# Copy entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 9007

ENTRYPOINT ["./entrypoint.sh"]
