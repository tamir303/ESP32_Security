from pydantic import BaseModel
from typing import Optional


class UserCreateDTO(BaseModel):
    username: str
    password: str
    api_key: Optional[str] = None


class UserResponseDTO(BaseModel):
    username: str
    api_key: str
