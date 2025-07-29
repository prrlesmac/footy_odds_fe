from flask import Flask
from app.routes.main import main_bp
from app.routes.health import health_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
    
    return app