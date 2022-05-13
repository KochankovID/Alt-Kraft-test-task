from logging.config import dictConfig

from app.db.mongodb import is_database_online, mongo_storage
from app.routers import comments
from fastapi import FastAPI
from fastapi_health import health


def register_routers(app: FastAPI):
    app.include_router(comments.router)
    app.add_api_route("/health", health([is_database_online]), tags=["health check"])


def configure_logging(logger_config: dict):
    dictConfig(logger_config)


def set_up_db(app: FastAPI, db_url: str, db_name: str):
    @app.on_event("startup")
    async def startup_event():
        await mongo_storage.set_up(db_url, db_name)
