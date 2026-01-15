"""
Flask Application Factory

This module creates and configures the Flask application instance.
It sets up:
1. Flask app with configuration
2. CORS (Cross-Origin Resource Sharing) for API access
3. File upload size limits
4. Blueprint registration for routes

Using the application factory pattern allows:
- Multiple app instances (testing, production, etc.)
- Flexible configuration
- Proper initialization order
"""
from flask import Flask
from flask_cors import CORS


def create_app():
    """
    Create and configure Flask application.
    
    This is the application factory function. It should be called
    to instantiate the app in different contexts (production, testing, etc).
    
    Configuration:
    - MAX_CONTENT_LENGTH: 100MB max file size for uploads
      Used for audio and CSV files
    - CORS: Enables cross-origin requests from any origin
      Allows frontend on different domain to access API
    
    Setup Steps:
    1. Create Flask app instance
    2. Set maximum upload file size (100MB)
    3. Enable CORS for all routes
    4. Import and register blueprints (routes)
    5. Return configured app
    
    Returns:
        Flask: Configured Flask application instance
        
    Usage in other files:
        from app import create_app
        app = create_app()
        app.run()
    
    Blueprints Registered:
    - main_bp (from app.routes): Contains all API endpoints
        Routes: /health, /transcribe, /load-csv, /retrieve-context, /generate-sql
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    # Configure max file upload size (100MB for large audio/CSV files)
    # This affects streaming and form data processing
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
    
    # Enable CORS (Cross-Origin Resource Sharing)
    # Allows frontend on different domains to access this API
    # In production, should restrict to specific origins
    CORS(app)
    
    # Import and register routes blueprint
    # This makes all routes in main_bp available on the app
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
