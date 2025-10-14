from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr

class UpdateProfile(BaseModel):
    displayName: Optional[str] = None
    photoURL: Optional[str] = None
    phoneNumber: Optional[str] = None

class LoginWithIdToken(BaseModel):
    id_token: str

RoleLiteral = Literal["student", "teacher", "admin"]

class MeResponse(BaseModel):
    uid: str
    email: Optional[EmailStr] = None
    displayName: Optional[str] = None
    photoURL: Optional[str] = None
    profile: Optional[dict] = None

    # 🔽 nuevos campos que tu endpoint ya está devolviendo
    role: Optional[RoleLiteral] = "student"           # rol primario
    is_admin: bool = False
    roles: List[RoleLiteral] = []
    admin_careers: List[str] = []
    platform_admin: bool = False