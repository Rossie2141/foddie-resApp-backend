from fastapi import FastAPI
from app.database import Base, engine
from app.routes import dishes

# Create tables (safe for Neon)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Foodi API",
    version="1.0.0"
)

app.include_router(dishes.router)


@app.get("/")
def root():
    return {"status": "Foodi backend running"}
