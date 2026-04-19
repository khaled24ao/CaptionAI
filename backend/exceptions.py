class CaptionAIException(Exception):
    status_code: int = 500
    message: str = "Internal server error"
    
    def __init__(self, message: str = None):
        self.message = message or self.message
        super().__init__(self.message)


class InvalidFileError(CaptionAIException):
    status_code = 400
    message = "Invalid file provided"


class FileSizeError(CaptionAIException):
    status_code = 413
    message = "File size exceeds maximum allowed"


class UnsupportedFormatError(CaptionAIException):
    status_code = 415
    message = "Unsupported file format"


class AIProcessingError(CaptionAIException):
    status_code = 502
    message = "Failed to process image with AI"


class ValidationError(CaptionAIException):
    status_code = 422
    message = "Validation error"