import uvicorn
from app.core import logger
from app.core.config import settings
from app.core.init_app import configure_logging, register_routers, set_up_db
from app.core.logger import LOGGING
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    contact=settings.CONTACTS,
    openapi_tags=settings.TAGS_METADATA,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

set_up_db(app, settings.DB_URL, settings.DB_NAME)
register_routers(app)
configure_logging(logger.LOGGING)
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=settings.PORT,
        log_config=LOGGING,
    )
