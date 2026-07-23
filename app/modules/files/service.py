import uuid

from infrastructure.storage.base import StorageProvider

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
        file,
        owner_type: OwnerType,
        owner_id: str,
        category: FileCategory,
    ):
        # Validate
        self.validator.validate_image(
            content_type=file.content_type,
            size=file.size,
        )

        # Generate filename
        extension = (
            file.filename
            .split(".")[-1]
        )

        filename = self.namer.generate(
            extension
        )

        # Generate storage path
        path = self.path_generator.generate(
            owner_type=owner_type,
            owner_id=owner_id,
            category=category,
            filename=filename
        )

        # Send to storage
        content = await file.read()

        storage_key = await self.storage.upload(
            path=path,
            content=content,
            content_type=file.content_type,
        )

        # Save metadata
        file_record = File(
            id=str(uuid.uuid4()),
            original_name=file.filename,
            storage_key=storage_key,
            provider="local",
            mime_type=file.content_type,
            size=file.size,
            owner_type=owner_type,
            owner_id=owner_id,
            category=category,
        )

        return await self.repository.create(file_record)


    async def delete(
        self,
        file_id: str
    ):

        file = await self.repository.get_by_id(
            file_id
        )


        if not file:
            raise FileNotFound()


        await self.storage.delete(
            file.storage_key
        )


        file.status = FileStatus.DELETED


        await self.repository.update(
            file
        )
