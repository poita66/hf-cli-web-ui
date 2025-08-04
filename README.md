# Hugging Face CLI Cache Manager

A web interface for managing the Hugging Face CLI cache, built with Flask (Python) backend and React/TypeScript frontend.

## Features

- View cache statistics (size, number of files, folders)
- View cached files with metadata
- Download models from Hugging Face Hub with progress tracking
- Clear the entire cache
- Real-time progress updates for downloads

## Backend

### Technologies
- Flask (Python web framework)
- Hugging Face Hub SDK
- Flask-CORS for cross-origin resource sharing

### Endpoints
- `GET /api/cache/stats` - Get cache statistics
- `GET /api/cache/files` - Get list of cached files
- `POST /api/cache/download` - Start downloading a model
- `GET /api/cache/download/<download_id>/progress` - Get download progress
- `DELETE /api/cache/download/<download_id>` - Cancel a download
- `POST /api/cache/clear` - Clear the entire cache

## Frontend

### Technologies
- React (TypeScript)
- Vite for development
- Tailwind CSS for styling

### Components
- Cache statistics dashboard
- Download form
- Active downloads tracker
- Cached files table

## Setup Instructions

### Using run.sh script
The project includes a convenient `run.sh` script that automates the setup and running of both backend and frontend:

1. Make the script executable:
   ```
   chmod +x run.sh
   ```

2. Run the application:
   ```
   ./run.sh
   ```

This will:
- Set up the Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Start both backend and frontend servers

### Using uv (recommended for faster installation)
The project supports [uv](https://github.com/astral-sh/uv) for faster Python package installation.

1. Install uv if you haven't already:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Set up the environment with uv:
   ```
   cd backend
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   cd ..
   ```

3. Run the application with the run.sh script:
   ```
   ./run.sh
   ```

### Manual Setup
#### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```
   python app.py
   ```

#### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run dev
   ```

The frontend will be available at http://localhost:3000 and will proxy API requests to the backend at http://localhost:5000.

## Development Notes

- The backend uses threading to handle concurrent downloads
- Progress tracking is implemented with a polling mechanism
- The frontend uses React hooks for state management
- All API calls are proxied through the Vite development server for easier development