import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base, get_db
from app.main import app
# Import models explicitly before table creation
from app.models.user_model import \
    User  # 🔹 Ensure this is imported before calling create_all()

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override get_db to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    # Ensure database tables exist before running tests
    Base.metadata.create_all(bind=engine)  # Ensure tables are created
    test_client = TestClient(app)
    yield test_client  # This is the test client available in tests
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)
