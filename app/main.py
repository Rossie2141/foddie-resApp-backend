from fastapi import FastAPI
from app.database import Base, engine
from app.routes import dishes, auth  # Added auth router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware # Import this

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Foodi API",
    version="1.0.0"
)

# 1. Add Session Middleware 
# In production, move 'secret-key' to an environment variable (.env)
app.add_middleware(
    SessionMiddleware, 
    secret_key="your_very_secret_random_string",
    session_cookie="foodi_session",  # Name of the cookie
    same_site="lax",                 # Essential for local development
)

# 2. Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",       
        "https://foodi-res-app.vercel.app" 
    ],
    allow_credentials=True,           # MUST be True for sessions
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include Routers
app.include_router(dishes.router)
app.include_router(auth.router) # You will create this next

@app.get("/")
def root():
    return {"status": "Foodi backend running"}