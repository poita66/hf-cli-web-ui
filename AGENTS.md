# Project Description

This is a Hugging Face CLI Cache Manager web application that provides a user interface for managing the Hugging Face cache. It allows users to view cache statistics, browse cached files, download models, and clear the cache.

## Key Features

- View cache statistics (total size, number of files, etc.)
- Browse cached files and their properties
- Download models directly from the web UI
- Clear the entire cache
- Responsive web interface built with React/Vite

## Architecture

### Backend
- Built with Python Flask
- Uses the Hugging Face Hub library to manage cache operations
- Provides RESTful API endpoints for frontend interaction
- Handles caching and file management logic

### Frontend
- Built with React and Vite
- Uses modern JavaScript/TypeScript
- Responsive design for various screen sizes
- Interacts with the backend API

## How to Run

### Prerequisites
- Python 3.8+
- Node.js 16+

### Setup
1. Install Python dependencies:
   ```
   pip install -r backend/requirements.txt
   ```

2. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

3. Build the frontend:
   ```
   npm run build
   ```

4. Run the backend:
   ```
   cd backend
   python app.py
   ```

## API Endpoints

- `GET /api/cache/stats` - Get cache statistics
- `GET /api/cache/files` - Get list of cached files
- `POST /api/cache/download` - Start a model download
- `GET /api/cache/download/{id}/progress` - Get download progress
- `DELETE /api/cache/download/{id}` - Cancel a download
- `POST /api/cache/clear` - Clear the entire cache

## File Structure

```
.
├── backend/           # Python Flask backend
│   ├── app.py         # Main application file
│   ├── requirements.txt  # Python dependencies
│   └── ...
├── frontend/          # React/Vite frontend
│   ├── src/           # Source files
│   ├── dist/          # Built files
│   └── ...
├── AGENTS.md          # This file
└── README.md          # Project overview
```

## Development Notes

For future LLM coding agent sessions, remember:
- The backend runs on port 5000 by default
- The frontend is built with Vite and serves from the dist directory
- Static assets are served from the frontend's dist/assets directory
- The backend uses the Hugging Face Hub library for cache management
## Development Notes

For future LLM coding agent sessions, remember:
- The backend runs on port 5000 by default
- The frontend is built with Vite and serves from the dist directory
- Static assets are served from the frontend's dist/assets directory
- The backend uses the Hugging Face Hub library for cache management
- Commit early and often to maintain a clean history
- Generate tests BEFORE implementing features
- Update the README.md file when making changes that affect users or developers
