from sqlalchemy import Column, String, Integer, Boolean, DateTime
from infrastructure.database import Base
from .enums import FileStatus


class File(Base):

    __tablename__ = "files"

    id = Column(
        String,
        primary_key=True
    )

    original_name = Column(
        String,
        nullable=False
    )

    storage_key = Column(
        String,
        nullable=False
    )

    provider = Column(
        String,
        nullable=False
    )

    mime_type = Column(
        String,
        nullable=False
    )

    size = Column(
        Integer,
        nullable=False
    )

    owner_type = Column(
        String,
        nullable=False
    )

    owner_id = Column(
        String,
        nullable=False
    )

    category = Column(
        String,
        nullable=False
    )

    is_public = Column(
        Boolean,
        default=False
    )

    status = Column(
        String,
        default=FileStatus.PENDING
    )


    deleted_at = Column(
        DateTime,
        nullable=True
    )