import uuid

from fastapi import UploadFile

from infrastructure.storage import StorageProvider
from core.config import settings

from .models import File
from .repository import FileRepository
from .validators import FileValidator
from .naming import FileNamer
from .enums import FileCategory, OwnerType, FileStatus
from .paths import FilePath
from .exceptions import FileNotFound


class FileService:

    def __init__(
        self,
        repository: FileRepository,
        storage: StorageProvider,
        validator: FileValidator,
        namer: FileNamer,
        path_generator: FilePath,
    ):

        self.repository = repository
        self.storage = storage
        self.validator = validator
        self.namer = namer
        self.path_generator = path_generator


    async def upload(
        self,
        *,
        file: UploadFile,
        owner_type: OwnerType,
        owner_id: str,
        category: FileCategory,
    ) -> File:

        # Validate based on category
        self.validator.validate(
            content_type=file.content_type,
            size=file.size,
            category=category,
        )

        # Generate unique filename
        extension = file.filename.rsplit(".", 1)[-1]

        filename = self.namer.generate(extension)

        # Build storage path
        path = self.path_generator.generate(
            owner_type=owner_type,
            owner_id=owner_id,
            category=category,
            filename=filename,
        )

        # Store the file
        content = await file.read()

        storage_key = await self.storage.upload(
            path=path,
            content=content,
            content_type=file.content_type,
        )

        # Save metadata to database
        file_record = File(
            id=str(uuid.uuid4()),
            original_name=file.filename,
            storage_key=storage_key,
            provider=settings.STORAGE_PROVIDER,
            mime_type=file.content_type,
            size=file.size,
            owner_type=owner_type,
            owner_id=owner_id,
            category=category,
        )

        return await self.repository.create(file_record)


    async def get(self, file_id: str) -> File:

        file = await self.repository.get_by_id(file_id)

        if not file:
            raise FileNotFound()

        return file


    def get_url(self, file: File) -> str:

        return self.storage.get_url(file.storage_key)


    async def delete(self, file_id: str) -> None:

        file = await self.get(file_id)

        await self.storage.delete(file.storage_key)

        file.status = FileStatus.DELETED

        await self.repository.update(file)
