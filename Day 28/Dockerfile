
# Use an official lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Prevent Python from creating bytecode files
ENV PYTHONDONTWRITEBYTECODE=1

# Display logs immediately
ENV PYTHONUNBUFFERED=1

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the API port
EXPOSE 8000

# Start the FastAPI application
CMD ["python", "api.py"]
