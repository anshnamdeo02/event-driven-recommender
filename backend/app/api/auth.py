from datetime import datetime, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.db.session import SessionLocal
from backend.app.models.user import User
from backend.app.schemas.auth import SignupRequest, LoginRequest, VerifyRequest
from backend.app.core.security import hash_password, verify_password, create_access_token
from backend.app.core.deps import get_current_user
from backend.app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest
from backend.app.core.email import send_email

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- SIGNUP ----------------

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")

    otp = str(random.randint(100000, 999999))

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hash_password(data.password),
        otp_code=otp
    )

    db.add(user)
    db.commit()

    print(f"📧 OTP for {data.email}: {otp}")


    return {"message": "Signup successful: {otp}"}


# ---------------- VERIFY ----------------

@router.post("/verify")
def verify(data: VerifyRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or user.otp_code != data.otp:
        raise HTTPException(400, "Invalid OTP")

    user.is_verified = True
    user.otp_code = None
    db.commit()

    return {"msg": "Account verified"}


# ---------------- LOGIN ----------------

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Swagger sends "username" field
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(400, "Invalid credentials")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(400, "Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user.id)
    }


@router.get("/protected")
def protected(user_id: str = Depends(get_current_user)):
    return {"msg": f"Hello {user_id}"}

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(404, "User not found")

    otp = str(random.randint(100000, 999999))
    user.otp_code = otp
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
    db.commit()

    print(f"📧 RESET OTP for {user.email}: {otp}")

    return {"msg": "Password reset OTP sent"}

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or user.otp_code != data.otp:
        raise HTTPException(400, "Invalid OTP")

    if datetime.utcnow() > user.otp_expires_at:
        raise HTTPException(400, "OTP expired")

    user.hashed_password = hash_password(data.new_password)
    user.otp_code = None
    user.otp_expires_at = None

    db.commit()
    return {"msg": "Password reset successful"}
