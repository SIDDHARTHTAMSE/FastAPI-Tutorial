
from contextlib import asynccontextmanager
from fastapi import FastAPI

from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.models.post import router as post_router
from storeapi.tests.routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(post_router)
app.include_router(user_router)
