"""服务入口"""

from contextlib import asynccontextmanager

from aerich import Command
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from flyflower import models
from flyflower.api import router
from flyflower.trie import ztrie
from flyflower.settings import APP_NAME, TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    command = Command(
        tortoise_config=TORTOISE_ORM,
        app=APP_NAME,
        location="./migrations",
    )
    await command.init()
    await command.upgrade(run_in_transaction=True)
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        add_exception_handlers=False,
    )
    async for poetry in models.Poetry.all():
        for paragraph in poetry.paragraphs:
            ztrie.add(paragraph)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
