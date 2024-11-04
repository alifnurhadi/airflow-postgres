# Build stage
FROM apache/airflow:slim-2.9.3-python3.11 AS builder

USER root

# Install build dependencies without MySQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libpq-dev \
        pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and set permissions for pip cache directory
RUN mkdir -p /home/airflow/.cache/pip && \
    mkdir -p /home/airflow/.local && \
    chown -R airflow:root /home/airflow/.cache && \
    chown -R airflow:root /home/airflow/.local && \
    chmod -R 775 /home/airflow/.cache && \
    chmod -R 775 /home/airflow/.local

# Switch to airflow user for pip installations
USER airflow

# Upgrade pip first as a separate step
RUN pip install --upgrade pip

# Install Airflow and providers without MySQL
RUN pip install --no-cache-dir apache-airflow==2.9.3

# Copy and install requirements
COPY --chown=airflow:root requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Final stage
FROM apache/airflow:slim-2.9.3-python3.11

USER root

# Install only runtime dependencies without MySQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && find /var/lib/apt/lists /var/cache/apt/archives -type f -delete

# Remove unnecessary files
RUN rm -rf /usr/share/doc \
           /usr/share/man \
           /usr/share/locale \
           /var/lib/apt/lists/* \
           /var/cache/apt/* \
           /var/log/* \
           /tmp/* \
           /var/tmp/*

# Prepare directory for airflow user
RUN mkdir -p /home/airflow/.local && \
    chown -R airflow:root /home/airflow/.local && \
    chmod -R 775 /home/airflow/.local

USER airflow

# Copy installed packages
COPY --from=builder --chown=airflow:root /home/airflow/.local /home/airflow/.local

# Clean up Python packages
RUN find /home/airflow/.local -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true \
    && find /home/airflow/.local -type f -name "*.pyc" -delete \
    && find /home/airflow/.local -type f -name "*.pyo" -delete \
    && find /home/airflow/.local -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true \
    && find /home/airflow/.local -type d -name "test" -exec rm -rf {} + 2>/dev/null || true

# Set working directory and Python path
WORKDIR /opt/airflow
ENV PYTHONPATH=/opt/airflow \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=2

# Verify installation
RUN python -c "import airflow; print(f'Airflow version: {airflow.__version__}')"
