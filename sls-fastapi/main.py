import os
from fastapi import FastAPI, HTTPException

from src import BasicError, Status, ChangeItem, NewItem, Item, Items, TodoItems

todos = TodoItems()

app = FastAPI(title="To do list backend")


@app.get("/", response_model=Status, tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.get("/items", response_model=Items, tags=["todo"])
async def get_to_do_items():
    return todos.items


@app.get(
    "/item/{todo_id}", response_model=Item, tags=["todo"], responses={404: {"model": BasicError}}
)
async def get_to_do_item(todo_id: int):
    try:
        return todos.item(todo_id)
    except StopIteration:
        raise HTTPException(404, detail="Item not found")


@app.delete("/item/{todo_id}", response_model=Status, tags=["todo"])
async def delete_to_do_item(todo_id: int):
    todos.delete_item(todo_id)
    return {"status": "deleted"}


@app.patch(
    "/item/{todo_id}", response_model=Item, tags=["todo"], responses={404: {"model": BasicError}}
)
async def patch_to_do_item(todo_id: int, item: ChangeItem):
    try:
        return todos.patch_item(todo_id, item.todo)
    except StopIteration:
        raise HTTPException(404, detail="Item not found")


@app.post("/item", response_model=Item, tags=["todo"])
async def create_to_do_item(*, item: NewItem):
    return todos.create_item(item)
