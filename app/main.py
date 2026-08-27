from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import alerts, devices, readings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Create database tables when the application starts."""

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Device Monitoring Service",
    description="API for managing devices, readings, and alerts.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(devices.router)
app.include_router(readings.router)
app.include_router(alerts.router)



@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {
        "message": "Device Monitoring Service is running",
        "documentation": "/docs",
    }


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "healthy"}