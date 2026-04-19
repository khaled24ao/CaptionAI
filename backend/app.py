from flask import Flask, render_template
from flask_cors import CORS
from flasgger import Swagger
from backend.config.settings import get_settings
from backend.error_handlers import register_error_handlers
from backend.security import add_security_headers
from backend.utils.logger import app_logger
import os


def create_app():
    settings = get_settings()
    
    template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    app = Flask(__name__, template_folder=template_folder)
    
    app.config["UPLOAD_FOLDER"] = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "storage", 
        "uploads"
    )
    app.config["MAX_CONTENT_LENGTH"] = settings.max_file_size_mb * 1024 * 1024
    app.config["SWAGGER"] = {
        "title": "CaptionAI API",
        "uiversion": 3,
        "info": {
            "title": "CaptionAI API",
            "description": "AI-powered image captioning service",
            "version": "1.0.0"
        }
    }
    
    CORS(app, origins=settings.cors_origins)
    Swagger(app)
    add_security_headers(app)
    register_error_handlers(app)
    
    from backend.routes.caption import caption_bp
    app.register_blueprint(caption_bp)
    
    @app.route("/")
    def index():
        return render_template("index.html")
    
    if settings.debug:
        app_logger.setLevel("DEBUG")
    
    app_logger.info(f"Application started: {settings.app_name}")
    
    return app