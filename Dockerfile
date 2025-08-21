# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional: for some ML libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

# Expose the port your Dash app runs on
EXPOSE 8050

# Run with Gunicorn (production server)
# Replace 'app:server' with your entrypoint:
#   - 'app' is your app.py filename (without .py)
#   - 'server' is the Flask/Dash server instance inside app.py
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
