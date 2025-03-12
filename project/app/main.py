import logging

from fastapi import FastAPI

from app.api import cash_flow, category, ping, summaries
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(category.router, prefix="/category", tags=["category"])
    application.include_router(
        summaries.router,
        prefix="/summaries",
        tags=["summaries"],
        include_in_schema=False,
    )
    application.include_router(
        cash_flow.router,
        prefix="/cash_flow",
        tags=["cash_flow"],
        include_in_schema=False,
    )

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
