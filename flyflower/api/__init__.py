"""路由配置"""

from fastapi import APIRouter

from flyflower.api import poetry


router = APIRouter()


@router.get("/health", description="健康检查", tags=["探针"])
async def health():
    return True


router.include_router(
    poetry.router,
    prefix="/poetry",
    tags=["诗歌"],
)
