from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
)

from files.service import FileService
from files.dependencies import get_file_service

from files.enums import (
    OwnerType,
    FileCategory,
)


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

@router.post("/upload")
async def upload_file(

    file: UploadFile = File(...),

    service: FileService = Depends(
        get_file_service
    )

):

    uploaded_file = await service.upload(

        file=file,

        owner_type=OwnerType.USER,

        owner_id="123",

        category=FileCategory.AVATAR,
    )


    return uploaded_file