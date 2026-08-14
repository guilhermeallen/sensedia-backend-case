import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app
from app.models.models import Base


@pytest.fixture(scope="function")
def test_db():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield SessionLocal()
    
    # Cleanup
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    """Create a TestClient instance."""
    return TestClient(app)
