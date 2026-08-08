from enum import Enum


class FileCategory(str, Enum):

    AVATAR = "avatar"

    PRODUCT_IMAGE = "product_image"

    INVOICE = "invoice"

    ATTACHMENT = "attachment"


class OwnerType(str, Enum):

    USER = "user"



class FileStatus(str, Enum):

    ACTIVE = "active"

    DELETED = "deleted"

    PENDING = "pending"