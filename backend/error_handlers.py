from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from backend.exceptions import CaptionAIException


def register_error_handlers(app: Flask):
    @app.errorhandler(CaptionAIException)
    def handle_custom_exception(e: CaptionAIException):
        return jsonify({"error": e.message}), e.status_code
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        return jsonify({"error": e.description, "name": e.name}), e.code
    
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request"}), 400
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500
    
    return app