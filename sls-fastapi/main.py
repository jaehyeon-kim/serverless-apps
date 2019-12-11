from typing import Union
from fastapi import FastAPI, HTTPException

from src import BasicError, Status, NewItem, UpdateItem, Item, Items, TodoItems

app = FastAPI(title="To do list backend")


@app.get("/", response_model=Status, tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.get("/item", response_model=Union[Item, Items], tags=["todo"])
async def get_to_do_items(username: str, created_at: str, all_items: bool = False):
    return TodoItems().get_items(username, created_at, all_items)


@app.post("/item", response_model=Item, tags=["todo"])
async def create_to_do_item(item: NewItem):
    return TodoItems().create_item(item)


@app.put("/item", response_model=Item, tags=["todo"], responses={404: {"model": BasicError}})
async def update_to_do_item(item: UpdateItem):
    return TodoItems().update_item(item)


@app.delete("/item", response_model=Status, tags=["todo"], responses={404: {"model": BasicError}})
async def delete_to_do_item(username: str, created_at: str):
    item = TodoItems().get_items(username, created_at, all_items=False)
    if len(item["item"]) == 0:
        raise HTTPException(404, detail="Item not found")
    TodoItems().delete_item(username, created_at)
    return {"status": "deleted"}
