from marshmallow import Schema, fields, validate, validates, ValidationError
from typing import Any


class CaptionResponseSchema(Schema):
    caption = fields.Str(required=True)
    detailed_description = fields.Str(allow_none=True)
    hashtags = fields.List(fields.Str(), allow_none=True)
    alt_text = fields.Str(allow_none=True)
    mood = fields.Str(allow_none=True)
    use_cases = fields.List(fields.Str(), allow_none=True)


class ErrorSchema(Schema):
    error = fields.Str(required=True)
    details = fields.Dict(keys=fields.Str(), allow_none=True)


class ImageUploadSchema(Schema):
    image = fields.Raw(required=True, metadata={"type": "file"})
    
    @validates("image")
    def validate_image(self, value: Any) -> None:
        if not value:
            raise ValidationError("No image file provided")
        if hasattr(value, "filename") and not value.filename:
            raise ValidationError("No file selected")


image_upload_schema = ImageUploadSchema()
caption_response_schema = CaptionResponseSchema()
error_schema = ErrorSchema()