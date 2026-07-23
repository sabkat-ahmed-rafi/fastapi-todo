from .exceptions import (
    InvalidFileType,
    FileTooLarge
)

IMAGE_TYPES = [
    "image/png",
    "image/jpeg",
    "image/webp"
]

MAX_IMAGE_SIZE = 5 * 1024 * 1024

class FileValidator:

    def validate_image(
        self,
        *,
        content_type: str,
        size: int
    ):

        if content_type not in IMAGE_TYPES:
            raise InvalidFileType()


        if size > MAX_IMAGE_SIZE:
            raise FileTooLarge()