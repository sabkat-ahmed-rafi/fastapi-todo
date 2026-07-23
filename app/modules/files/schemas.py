from datetime import datetime
from pydantic import BaseModel


class FileResponse(BaseModel):

    id: str

    original_name: str

    url: str

    mime_type: str

    size: int

    created_at: datetime