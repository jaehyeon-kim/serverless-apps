import os
from typing import Union
from fastapi import FastAPI, HTTPException

from src.util import MangumExt
from src.todo import TodoItems
from src.models import BasicError, Status, NewItem, PatchItem, Item, Items

app = FastAPI(title="To do list backend")

if not os.getenv("LOCAL_STACK_ENDPOINT_URL"):
    app.docs_url = None
    app.redoc_url = None
    handler = MangumExt(app)


@app.get("/", response_model=Status, tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.get(
    "/items",
    response_model=Union[Item, Items],
    tags=["todo"],
    description="<br><br>".join(
        [
            "Get one or more items",
            "`created_at` should be either datetime string (eg 2019-01-01T12:00:00Z) or date string (eg 2019-01-01).",
            "When `all_items` equals `False`, only datetime string will return an item. Otherwise both will do.",
        ]
    ),
    responses={404: {"model": BasicError}},
)
async def get_to_do_items(username: str, created_at: str, all_items: bool = False):
    result = TodoItems().get_items(username, created_at, all_items)
    key = "items" if all_items else "item"
    if len(result[key]) == 0:
        raise HTTPException(404, detail="No {0} found".format(key))
    return result


@app.post("/item", response_model=Item, tags=["todo"])
async def create_to_do_item(item: NewItem):
    return TodoItems().create_item(item)


@app.patch("/item", response_model=Item, tags=["todo"], responses={404: {"model": BasicError}})
async def update_to_do_item(item: PatchItem):
    if not TodoItems().is_exist(item.username, item.created_at):
        raise HTTPException(404, detail="Item not found")
    return TodoItems().update_item(item)


@app.delete(
    "/item",
    response_model=Status,
    tags=["todo"],
    description="<br><br>".join(
        ["Get an item", "`created_at` should be datetime string (eg 2019-01-01T12:00:00Z).",]
    ),
    responses={404: {"model": BasicError}},
)
async def delete_to_do_item(username: str, created_at: str):
    if not TodoItems().is_exist(username, created_at):
        raise HTTPException(404, detail="Item not found")
    TodoItems().delete_item(username, created_at)
    return {"status": "deleted"}
