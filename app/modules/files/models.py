from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database import Base
from .enums import FileStatus


class File(Base):
    __tablename__ = "files"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )

    original_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    storage_key: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    provider: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    mime_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    size: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    owner_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    owner_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        default=FileStatus.ACTIVE,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )