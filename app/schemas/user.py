from typing import Optional
from pydantic import BaseModel, EmailStr

class UpdateProfile(BaseModel):
    displayName: Optional[str] = None
    photoURL: Optional[str] = None
    phoneNumber: Optional[str] = None

class LoginWithIdToken(BaseModel):
    id_token: str

class MeResponse(BaseModel):
    uid: str
    email: Optional[EmailStr] = None
    displayName: Optional[str] = None
    photoURL: Optional[str] = None
    profile: Optional[dict] = None
