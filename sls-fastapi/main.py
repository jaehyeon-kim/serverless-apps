import os
from functools import wraps
from datetime import datetime
from fastapi import FastAPI, HTTPException

from src import BasicError, Status, TodoPatch, TodoPost, Item, Items, TodoItems

todos = TodoItems()

app = FastAPI(title="To do list backend")


def check_item(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        todo_id = kwargs["todo_id"]
        print("todo id in decorator - ", todo_id)
        return f(*args, **kwargs)

    return decorated


@app.get("/", response_model=Status, tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.get("/items", response_model=Items, tags=["todo"])
async def get_to_do_items():
    print(todos.items)
    return todos.items


@app.post("/item", response_model=Item, tags=["todo"], responses={404: {"model": BasicError}})
async def create_to_do_item(*, req: TodoPost):
    return {"id": 1, "todo": "foo bar baz", "username": "John Doe", "created_at": datetime.now()}


@app.get("/item/{todo_id}", tags=["todo"])
# @check_item
async def get_to_do_item(todo_id: int):
    print("todo id in get method - ", todo_id)
    print(todos.item(todo_id))
    # return todos.item(todo_id)


@app.delete("/item/{todo_id}", response_model=Status, tags=["todo"])
async def delete_to_do_item(todo_id: int):
    return {"status": "ok"}


@app.patch("/item/{todo_id}", response_model=Status, tags=["todo"])
async def patch_to_do_item(todo_id: int, req: TodoPatch):
    return {"status": "ok"}
