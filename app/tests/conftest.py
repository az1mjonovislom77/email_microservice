import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db  # Sizning Base va get_db bu yerda bo'lishi kerak

# Test uchun lokal DB URL — GitHub Actions yoki lokal test uchun mos yozing
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/email_service"

# SQLAlchemy engine va sessiya
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Test sessiyasi boshida jadval yaratish va oxirida o‘chirish."""
    # Jadval yaratish
    Base.metadata.create_all(bind=engine)
    yield
    # Jadval o‘chirish (ixtiyoriy)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Har bir test uchun alohida DB sessiyasi yaratish."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI test client va DB sessiyasini override qilish."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
