import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import engine
from app.models.dish import Base

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")

if __name__ == "__main__":
    create_tables()
