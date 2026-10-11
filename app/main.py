from fastapi import FastAPI

from app import models  # noqa: F401  (registers tables on Base.metadata)
from app.api import accounts, journal
from app.config import Settings, get_settings
from app.db import Base, make_engine, make_session_factory


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    engine = make_engine(settings.database_url)
    # No migrations yet; tables are created on startup.
    Base.metadata.create_all(engine)
    app.state.engine = engine
    app.state.session_factory = make_session_factory(engine)

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(accounts.router, prefix="/api/v1")
    app.include_router(journal.router, prefix="/api/v1")
    return app


app = create_app()
