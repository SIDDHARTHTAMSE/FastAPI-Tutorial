import databases
import sqlalchemy
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine

from storeapi.config import config


metadata = sqlalchemy.MetaData()

post_table = sqlalchemy.Table(
    "post",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String)
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("post.id"), nullable=False)
)

print(config.DEV_DATABASE_URL, "*****")

engine = sqlalchemy.create_engine(
    config.DEV_DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
database = databases.Database(
    config.DEV_DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
