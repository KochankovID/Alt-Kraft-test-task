import pytest
import pytest_asyncio
from app.core.config import settings
from app.db.mongodb import mongo_storage
from app.main import app
from httpx import AsyncClient
from tests.utils import is_responsive


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(scope="session")
def setup_db(docker_ip, docker_services):
    url = f"http://{settings.DB_HOST}:{settings.DB_PORT}"
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )


@pytest_asyncio.fixture
async def client(setup_db):
    await mongo_storage.set_up(settings.DB_URL, settings.DB_NAME)
    async with AsyncClient(
        app=app, base_url="http://", headers={"host": "localhost"}
    ) as ac:
        yield ac


@pytest.fixture
def mock_data():
    return [
        {
            "name": "Joseph Bishop",
            "text": "Bar reach piece my catch its. Letter commercial process. "
            "Parent themselves necessary within mother center your.",
            "address": "077 Caldwell Street Suite 230 West Stephanie, DE 51163",
        }
        for _ in range(3)
    ]


@pytest_asyncio.fixture
async def fill_mock_data(setup_db, mock_data):
    db = mongo_storage.get_mongo_db()
    await db.comments.insert_many(mock_data)
    yield
    await db.comments.drop()
