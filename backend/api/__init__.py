from flask import Blueprint

# Create a blueprint for API routes
api_bp = Blueprint('api', __name__)

# Import all API modules to register their routes
from . import cache
from . import downloads

# Register the blueprints in the main application
def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='/api')