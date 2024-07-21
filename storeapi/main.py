
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import HTTPException

from storeapi.database import comment_table, post_table, database
from storeapi.models.post import (
    UserPost,
    UserPostIn,
    Comment,
    CommentIn,
    UserPostWithComment,
)

# Database connection with lifespan events in FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, world!, please go to /docs for swagger UI"}


# Our social media API: adding posts


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


@app.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.dict()
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@app.get("/post", response_model=list[UserPost])
async def get_all_post():
    query = post_table.select()
    return await database.fetch_all(query)


@app.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    data = comment.dict()
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@app.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comment_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)

# comments = []
#
# for c in comment_table.values():
#     if c["post_id"] == 1:
#         comments.append(c)
#
# print(comments)


@app.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comment_on_post(post_id)
    }
