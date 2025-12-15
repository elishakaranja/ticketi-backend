FROM python:3.10.13-slim

WORKDIR /app

# Install system dependencies for PostgreSQL + Python build
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DATABASE_URL=${DATABASE_URL}
ENV PORT=${PORT}

# Run migrations and start server
CMD ["sh", "-c", "flask db upgrade && gunicorn app:app --bind 0.0.0.0:$PORT"]
