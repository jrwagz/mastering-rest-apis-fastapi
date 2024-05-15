from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from socialapi.logging_conf import configure_logging
from socialapi.routers.post import router as router_post

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager

    Args:
        app: FastAPI app object
    """
    configure_logging()
    logger.info("Application is configured and ready to start!")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=router_post)
