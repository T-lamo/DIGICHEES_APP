# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from src.main import app
from src.conf.db.database import Database
from src.models import Utilisateur
from src.core.auth.auth_dependencies import get_current_active_user



# SQLite de test
TEST_DATABASE_URL = "sqlite:///./test.db"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


def override_get_current_user():
    return Utilisateur(
        id=1,
        username="testuser",
        password="test1234"
    )

def override_get_session():
    with Session(engine_test) as session:
        yield session


@pytest.fixture(scope="function")
def client():
    # Crée les tables
    SQLModel.metadata.create_all(engine_test)

    # Override la dépendance
    app.dependency_overrides[Database.get_session] = override_get_session
    app.dependency_overrides[get_current_active_user] = override_get_current_user 


    with TestClient(app) as test_client:
        yield test_client

    # Cleanup
    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine_test)
