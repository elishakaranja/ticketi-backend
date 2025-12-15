FROM python:3.10.13-slim

WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DATABASE_URL=${DATABASE_URL}

# Use the port Koyeb assigns
ENV PORT=${PORT}

# Run migrations first, then start server
CMD ["sh", "-c", "flask db upgrade && gunicorn app:app --bind 0.0.0.0:$PORT"]


