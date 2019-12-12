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


class Item(BaseModel):
    item: Union[ItemFields, dict]


class Items(BaseModel):
    items: Union[List[ItemFields], list]
