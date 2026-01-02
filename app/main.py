from fastapi import FastAPI
from app.database import Base, engine
from app.routes import dishes

from fastapi.middleware.cors import CORSMiddleware


# Create tables (safe for Neon)
Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="Foodi API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",       # local dev
        "https://foodi-res-app.vercel.app"  # prod frontend (later)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dishes.router)


@app.get("/")
def root():
    return {"status": "Foodi backend running"}
