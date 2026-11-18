import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

os.environ.setdefault(
    "DATABASE_URL", "postgresql+psycopg://correspond:correspond@localhost:5433/correspond_test"
)

from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.demo_seed import ensure_demo_user  # noqa: E402

TEST_DATABASE_URL = os.environ["DATABASE_URL"]
_ADMIN_URL = TEST_DATABASE_URL.rsplit("/", 1)[0] + "/postgres"


def _ensure_test_database_exists() -> None:
    admin_engine = create_engine(_ADMIN_URL, isolation_level="AUTOCOMMIT")
    db_name = TEST_DATABASE_URL.rsplit("/", 1)[1]
    with admin_engine.connect() as conn:
        exists = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": db_name}).first()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
    admin_engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def _test_schema():
    _ensure_test_database_exists()
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def _clean_tables():
    with engine.begin() as conn:
        table_names = ", ".join(f'"{t.name}"' for t in Base.metadata.sorted_tables)
        conn.execute(text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE"))
    yield


@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def demo_user(db_session) -> User:
    return ensure_demo_user(db_session)
