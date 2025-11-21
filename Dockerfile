FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY pyproject.toml README.md LICENSE ./
COPY ser/ ./ser/
COPY examples/ ./examples/

# Install dependencies and package
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir numpy>=1.20.0 scipy>=1.7.0 && \
    pip install --no-cache-dir jupyter notebook && \
    pip install --no-cache-dir .

# Expose Jupyter port
EXPOSE 8888

# Default command starts Jupyter notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
