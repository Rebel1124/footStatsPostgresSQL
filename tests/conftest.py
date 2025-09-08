import pytest

from src.db import BaseDB, engine, get_db


@pytest.fixture(autouse=True)
def db_life():
    with engine.connect() as conn:
        BaseDB.metadata.create_all(conn)
        conn.commit()
        yield
        BaseDB.metadata.drop_all(conn)
        conn.commit()


@pytest.fixture
def db():
    with get_db() as database:
        yield database
