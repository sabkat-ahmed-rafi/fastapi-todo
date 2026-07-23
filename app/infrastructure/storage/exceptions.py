class StorageError(Exception):
    """Base storage exception."""


class FileNotFound(StorageError):
    pass


class UploadFailed(StorageError):
    pass