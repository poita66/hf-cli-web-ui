# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ ./backend/

# Copy the frontend build (if available)
# Note: In a real deployment, you'd typically build the frontend first
# and copy the built files here
COPY frontend/dist ./frontend/dist

# Expose the port the app will run on
EXPOSE 5000

# Run the application
CMD ["python", "backend/app.py"]