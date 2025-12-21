FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system deps needed for some packages
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
# Install app deps + gunicorn for production serving
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy app code
COPY . .

# Ensure DB exists and any migrations are applied at build time
RUN python -c "from database import init_db; init_db()"

EXPOSE 5000

# Run with gunicorn binding to internal port 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "1"]
