from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Dict, Union
from app.core.configs import settings


_connect_args: Dict[str, Union[int, str]] = {"connect_timeout": 3}
if "render.com" in settings.DATABASE_URL:
    _connect_args["sslmode"] = "require"

engine = create_engine(settings.DATABASE_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()