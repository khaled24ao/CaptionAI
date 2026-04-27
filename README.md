# CaptionAI 🖼️

AI-powered image captioning service that automatically generates detailed captions, hashtags, alt text, and use cases for your images.

![screenshot](docs/demo.png)

## Features

- **AI-Generated Captions** - One professional sentence description per image
- **Detailed Descriptions** - 3-sentence detailed breakdown of image content
- **Smart Hashtags** - 10 relevant hashtags automatically generated (without #)
- **Accessibility Alt Text** - WCAG-compliant alt text for screen readers
- **Mood Analysis** - Detects the emotional tone and feeling of images
- **Use Case Suggestions** - 3 recommended ways to use each image

## Tech Stack

- **Backend**: Python 3.11, Flask
- **AI Engine**: Groq API (Meta-Llama/Llama-4-Scout)
- **Image Processing**: Pillow (PIL)
- **API Docs**: Flasgger (Swagger)
- **Validation**: Pydantic, Marshmallow
- **Deployment**: Docker, Docker Compose

## How to Run

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd protofolio-8
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open http://localhost:7860 in your browser

## Docker

Build and run with Docker Compose:

```bash
docker-compose up --build
```

The application will be available at http://localhost:7860

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key (required) | - |
| `DEBUG` | Enable debug mode | `False` |
| `APP_NAME` | Application name | `CaptionAI` |
| `MAX_FILE_SIZE_MB` | Maximum upload file size (MB) | `5` |
| `ALLOWED_EXTENSIONS` | Comma-separated allowed extensions | `jpg,jpeg,png,webp` |
| `UPLOAD_FOLDER` | Upload storage directory | `storage/uploads` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |
| `FLASK_ENV` | Flask environment | `production` |

## API Endpoints

- `GET /` - Web interface
- `POST /api/v1/caption` - Generate image caption (multipart/form-data)
- `GET /apidocs` - Swagger API documentation

## License

MIT
