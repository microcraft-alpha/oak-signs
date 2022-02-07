"""App handlers."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from structlog import get_logger

from oak_signs.settings import settings

log = get_logger(__name__)


def create_application() -> FastAPI:
    """Create the FastAPI application.

    Returns:
        FastAPI: created app.
    """
    log.info("Creating app...")
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url="/api/docs",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
    )
    return app


app = create_application()
