FROM python:3.11-slim

ARG VERSION=0.0.0
ARG BUILD_ID=0
ARG PORT=5000
ENV PORT=$PORT
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV VERSION=$VERSION
ENV BUILD_ID=$BUILD_ID

WORKDIR /app

# Copy app files
COPY . .

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    python3-dev \
    libffi-dev \
    && apt-get clean

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download the spaCy model
RUN python -m spacy download en_core_web_md && \
    python -m spacy download fr_core_news_md

# Make entrypoint executable
RUN chmod +x entrypoint.sh

EXPOSE $PORT
ENTRYPOINT ["/app/entrypoint.sh"]
