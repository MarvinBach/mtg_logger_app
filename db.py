from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

SUPABASE_URL = "ncjplkroyenlrsuhkevf.supabase.co"
SUPABASE_PASSWORD = "asflkj897Add!"

DATABASE_URL = f"postgresql://postgres:{SUPABASE_PASSWORD}@db.{SUPABASE_URL}:5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
