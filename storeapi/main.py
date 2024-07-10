
from fastapi import FastAPI, HTTPException, APIRouter
from storeapi.models.post import router as post_router

from contextlib import asynccontextmanager
from storeapi.database import database
from storeapi.models.post import (
    UserPost,
    UserPostIn,
    Comment,
    CommentIn,
    UserPostWithComment,
)
app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello, world!"}


# Our social media API: adding posts


post_table = {}
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


@app.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@app.get("/post", response_model=list[UserPost])
async def get_all_post():
    return list(post_table.values())


@app.post("/comment", response_model=Comment)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    data = comment.dict()
    last_record_id = len(comment_table)
    new_comment = {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment
    return new_comment


@app.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comment_on_post(post_id: int):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]

comments = []

for c in comment_table.values():
    if c["post_id"] == 1:
        comments.append(c)

print(comments)


@app.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comment_on_post(post_id)
    }


# Database connection with lifespan events in FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
