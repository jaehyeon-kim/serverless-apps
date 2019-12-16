from typing import List, Union
from pydantic import BaseModel, Field


def set_dt_field(is_optional: bool):
    desc = "datetime string, format - eg) 2019-01-01T12:00:00Z"
    if is_optional:
        return Field(None, description=desc)
    else:
        return Field(..., description=desc)


class BasicError(BaseModel):
    detail: str


class Status(BaseModel):
    status: str


class NewItem(BaseModel):
    username: str
    todo: str


class PatchItem(NewItem):
    todo: str = None
    created_at: str = set_dt_field(is_optional=False)


class ItemFields(BaseModel):
    todo: str
    username: str
    created_at: str = set_dt_field(is_optional=False)
    updated_at: str = set_dt_field(is_optional=False)

    class Config:
        schema_extra = {
            "example": {
                "todo": "string",
                "username": "string",
                "created_at": "2019-01-01T12:00:00Z",
                "updated_at": "2019-01-01T12:00:00Z",
            }
        }


class Item(BaseModel):
    item: ItemFields


class Items(BaseModel):
    items: List[ItemFields]
