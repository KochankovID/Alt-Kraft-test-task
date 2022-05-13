from typing import Any

from app.db.mongodb import mongo_storage
from app.models.comment import Comment
from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetPage, Page
from fastapi_pagination.ext.motor import paginate
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter()


@router.get("/comments/default", tags=["comments"], response_model=Page[Comment])
@router.get(
    "/comments/limit-offset", tags=["comments"], response_model=LimitOffsetPage[Comment]
)
async def read_comments(
    db: AsyncIOMotorCollection = Depends(mongo_storage.get_mongo_db),
) -> Any:
    return await paginate(db.comments)
