from typing import NoReturn


def main() -> NoReturn:
    """Application entry point.
    
    Creates and runs the Flask application.
    """
    # Ensure .env is loaded before any imports that use env vars
    from dotenv import load_dotenv
    load_dotenv()
    
    from backend.app import create_app
    
    app = create_app()
    app.run(host="0.0.0.0", port=7860, debug=True)


if __name__ == "__main__":
    main()