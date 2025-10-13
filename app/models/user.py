from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
    uid: str
    email: Optional[str] = None
    displayName: Optional[str] = None
    photoURL: Optional[str] = None
