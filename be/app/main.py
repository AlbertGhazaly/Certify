from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as user_router
from app.api.auth import router as auth_router
from app.utils.config import settings


app = FastAPI(title=settings.app_name)

app.include_router(user_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}