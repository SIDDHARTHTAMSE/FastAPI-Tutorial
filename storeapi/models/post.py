from fastapi import APIRouter
from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int

    class Config:
        orm_mode = True


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int

    class Config:
        orm_mode = True


class UserPostWithComment(BaseModel):
    post: UserPost
    comments: list[Comment]


router = APIRouter()
