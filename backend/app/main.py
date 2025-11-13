from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .config import settings
from .db import get_db
from .routes.users import router as users_router
from .routes.backup import router as backup_router

app = FastAPI(title="Secure Users API", version="0.2.0")

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "up"}
    except Exception as e:
        return {"status": "degraded", "error": str(e)}

@app.get("/")
def root():
    return {"message": "Secure Users API - base online"}

# Montar endpoints de usuarios (register/login/users)
app.include_router(users_router)
app.include_router(backup_router)
