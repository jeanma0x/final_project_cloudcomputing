from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..db import get_db
from ..models import User
from ..schemas import RegisterRequest, LoginRequest, TokenResponse, UserOut
from ..auth import hash_password, verify_password, create_access_token, get_current_user
from ..config import settings
from ..audit import record_audit_log

router = APIRouter(prefix="", tags=["users"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario:
    - Valida unicidad de email
    - Hashea contraseña con bcrypt
    - Retorna info pública del usuario
    """
    new_user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        is_active=True
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    record_audit_log(db, action="REGISTER", actor_email=new_user.email, payload={"user_id": new_user.id})
    return new_user

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica usuario por email/password:
    - Busca email
    - Verifica contraseña con bcrypt
    - Emite JWT firmado (Bearer)
    """
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.email)
    record_audit_log(db, action="LOGIN", actor_email=user.email)
    return TokenResponse(access_token=token, expires_in_minutes=int(settings.APP_PORT) * 0 + 60)  # 60 por defecto

@router.get("/users", response_model=list[UserOut])
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Lista usuarios (ruta protegida por JWT).
    - Requiere: Authorization: Bearer <token>
    """
    users = db.query(User).order_by(User.id).all()
    return users
