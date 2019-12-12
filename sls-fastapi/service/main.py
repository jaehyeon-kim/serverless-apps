from typing import Union
from fastapi import FastAPI, HTTPException

from src import BasicError, Status, NewItem, PatchItem, Item, Items, TodoItems, set_dt_field

app = FastAPI(title="To do list backend")


@app.get("/", response_model=Status, tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.get(
    "/items",
    response_model=Union[Item, Items],
    tags=["todo"],
    description="Get item or items\n\taaa",
)
async def get_to_do_items(username: str, created_at: str, all_items: bool = False):
    return TodoItems().get_items(username, created_at, all_items)


@app.post("/item", response_model=Item, tags=["todo"])
async def create_to_do_item(item: NewItem):
    return TodoItems().create_item(item)


@app.patch("/item", response_model=Item, tags=["todo"], responses={404: {"model": BasicError}})
async def update_to_do_item(item: PatchItem):
    if not TodoItems().is_exist(item.username, item.created_at):
        raise HTTPException(404, detail="Item not found")
    return TodoItems().update_item(item)


@app.delete("/item", response_model=Status, tags=["todo"], responses={404: {"model": BasicError}})
async def delete_to_do_item(username: str, created_at: str):
    if not TodoItems().is_exist(username, created_at):
        raise HTTPException(404, detail="Item not found")
    TodoItems().delete_item(username, created_at)
    return {"status": "deleted"}
