"""服务入口"""

from fastapi import FastAPI


app = FastAPI()


@app.get("/health", description="健康检查", tags=["探针"])
async def health():
    return True


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
