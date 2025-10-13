from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import auth as fb_auth
from app.deps.auth import get_current_user
from app.schemas.user import MeResponse, UpdateProfile
from app.services.users_service import upsert_profile, get_profile, delete_profile

router = APIRouter(prefix="/users", tags=["users"])

# users router (añade/ajusta en /users/me)
@router.get("/me", response_model=MeResponse)
def me(current=Depends(get_current_user)):
    prof = current.get("profile") or {}
    # Fuente de verdad: DB profile.role (o 'student' por defecto)
    role = prof.get("role", "student")
    is_admin = (role == "admin")

    return {
        "uid": current["uid"],
        "email": current.get("email"),
        "displayName": current.get("displayName"),
        "photoURL": current.get("photoURL"),
        "profile": prof,
        "role": role,          # <-- nuevo
        "is_admin": is_admin,  # <-- nuevo
    }

@router.get("/me/profile")
def read_my_profile(current=Depends(get_current_user)):
    prof = get_profile(current["uid"])
    return {"ok": True, "profile": prof}

@router.post("/me/profile")
def update_my_profile(body: UpdateProfile, current=Depends(get_current_user)):
    data = {k: v for k, v in body.dict().items() if v is not None}
    if not data:
        return {"ok": True, "profile": current.get("profile")}
    profile = upsert_profile(current["uid"], data)
    return {"ok": True, "profile": profile}

@router.delete("/me")
def delete_my_account(current=Depends(get_current_user)):
    uid = current["uid"]
    try:
        fb_auth.delete_user(uid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo borrar el usuario en Auth: {e}")
    try:
        delete_profile(uid)
    except Exception:
        pass
    return {"ok": True}
