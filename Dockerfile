# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install Node.js for frontend build
RUN apt-get update && apt-get install -y nodejs npm

# Copy the requirements file
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ ./backend/

# Copy frontend files for build
COPY frontend/ ./frontend/

# Build frontend
RUN cd frontend && npm install && npm run build

# Expose the port the app will run on
EXPOSE 5000

# Run the application
CMD ["python", "backend/app.py"]