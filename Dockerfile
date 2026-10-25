FROM python:3.12-slim

WORKDIR /app

# Install libraries first: Docker caches this step, so rebuilds are fast
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the app code
COPY app.py VERSION ./
COPY templates ./templates

EXPOSE 8000

# Ask the app if it is alive every 30 seconds
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# One worker on purpose: products live in memory, so more workers would not share data
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "app:app"]
