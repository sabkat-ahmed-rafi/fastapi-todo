class FileException(Exception):
    pass


class InvalidFileType(FileException):
    pass


class FileTooLarge(FileException):
    pass


class FileNotFound(FileException):
    pass