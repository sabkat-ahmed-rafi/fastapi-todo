from dataclasses import dataclass


@dataclass(slots=True)
class StoredFile:
    key: str
    url: str