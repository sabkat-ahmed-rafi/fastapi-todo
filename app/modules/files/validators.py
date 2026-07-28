from .enums import FileCategory
from .exceptions import (
    InvalidFileType,
    FileTooLarge
)


IMAGE_TYPES = [
    "image/png",
    "image/jpeg",
    "image/webp"
]

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

IMAGE_CATEGORIES = {
    FileCategory.AVATAR,
    FileCategory.PRODUCT_IMAGE,
}


class FileValidator:

    def validate(
        self,
        *,
        content_type: str,
        size: int,
        category: FileCategory,
    ):

        if category in IMAGE_CATEGORIES:
            self._validate_image(content_type, size)


    def _validate_image(
        self,
        content_type: str,
        size: int,
    ):

        if content_type not in IMAGE_TYPES:
            raise InvalidFileType()

        if size > MAX_IMAGE_SIZE:
            raise FileTooLarge()