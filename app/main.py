from fastapi import FastAPI
from app.database import Base, engine
from app.routes import dishes, auth, user_data
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Foodi API",
    version="1.0.0"
)

# Session Middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "dev-secret-change-me"),
    session_cookie="foodi_session",
    same_site="none",      # REQUIRED for cross-site (Vercel)
    https_only=True        # REQUIRED when same_site="none"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://foodi-res-app.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(dishes.router)
app.include_router(auth.router)
app.include_router(user_data.router)

@app.get("/")
def root():
    return {"status": "Foodi backend running"}
