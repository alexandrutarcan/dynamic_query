# Use Python base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt ./


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose API port
EXPOSE 8000

# Run Uvicorn with FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]