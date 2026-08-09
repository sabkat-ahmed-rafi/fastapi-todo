from sqlalchemy import Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database import TimestampMixin

from infrastructure.database import Base
from .enums import FileStatus


class File(TimestampMixin, Base):
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