from typing import List

from fastapi import APIRouter, Body, Path, Query

from flyflower.trie import ztrie
from flyflower.models import Poetry


router = APIRouter()


@router.post(
    "",
    description="上传古诗词",
)
async def create(
    author: str = Body(..., max_length=32, description="作者"),
    rhythmic: str = Body(..., max_length=128, description="诗名"),
    paragraphs: List[str] = Body(..., description="诗句"),
):
    poetry = await Poetry.create(
        author=author,
        rhythmic=rhythmic,
        paragraphs=paragraphs,
    )
    for paragraph in paragraphs:
        ztrie.add(paragraph)
    return poetry


@router.get(
    "",
    description="查询所有古诗词",
)
async def reads(
    size: int = Query(10, description="每页数量"),
    page: int = Query(1, description="页码"),
):
    poetries = await Poetry.all().limit(size).offset((page - 1) * size)
    return poetries


@router.delete(
    "/{id}",
    description="删除古诗词",
)
async def delete(id: int = Path(..., description="诗词ID")):
    poetry = await Poetry.get_or_none(id=id)
    if poetry is not None:
        for paragraph in poetry.paragraphs:
            ztrie.remove(paragraph)
        await poetry.delete()
        rows = 1
    else:
        rows = 0
    return rows


@router.put(
    "/{id}",
    description="修改古诗词",
)
async def update(
    id: int = Path(..., description="诗词ID"),
    author: str = Body(..., max_length=32, description="作者"),
    rhythmic: str = Body(..., max_length=128, description="诗名"),
    paragraphs: List[str] = Body(..., description="诗句"),
):
    poetry = await Poetry.get_or_none(id=id)
    if poetry is not None:
        for paragraph in poetry.paragraphs:
            ztrie.remove(paragraph)
    rows = await Poetry.filter(id=id).update(
        author=author,
        rhythmic=rhythmic,
        paragraphs=paragraphs,
    )
    for paragraph in paragraphs:
        ztrie.add(paragraph)
    return rows


@router.get(
    "/{id}",
    description="查询古诗词",
)
async def get(id: int = Path(..., description="诗词ID")):
    poetry = await Poetry.get(id=id)
    return poetry


@router.get(
    "/search/slow",
    description="诗名称模糊查询古诗词",
)
async def search(
    key: str = Query(..., max_length=128, description="关键词"),
):
    # TODO 全文模糊搜索?
    poetries = await Poetry.filter(rhythmic__contains=key).all().limit(10)
    return poetries
