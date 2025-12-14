from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as user_router
from app.api.auth import router as auth_router
from app.api.student import router as student_router
from app.api.certificate import router as certificate_router
from app.api.issuer_reg import router as issuer_registration_router
from app.utils.config import settings
from app.database.connection import engine, Base

# Import all models to ensure they are registered with Base
from app.models.user import User
from app.models.nonce import Nonce
from app.models.session import Session
from app.models.student import Student
from app.models.certificate import Certificate
from app.models.Issuer_registration import Issuer_registration

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(student_router, prefix="/api", tags=["students"])
app.include_router(certificate_router, prefix="/api", tags=["certificates"])
app.include_router(issuer_registration_router, prefix="/api", tags=["issuer-registrations"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}