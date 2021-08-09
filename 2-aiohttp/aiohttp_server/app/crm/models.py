import uuid
from dataclasses import dataclass


@dataclass
class User:
    id_: uuid.UUID
    email: str
