from fastapi import FastAPI, HTTPException

from src import BasicError, Status, NewItem, UpdateItem, Item, Items, TodoItems

todos = TodoItems()

app = FastAPI(title="To do list backend")


@app.get("/", response_model=Status, tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.get("/item", response_model=Items, tags=["todo"])
async def get_to_do_items(username: str, created_at: str, all_items: bool = False):
    return todos.get_items(username, created_at, all_items)


@app.post("/item", response_model=Item, tags=["todo"])
async def create_to_do_item(item: NewItem):
    return todos.create_item(item)


@app.patch("/item", response_model=Item, tags=["todo"], responses={404: {"model": BasicError}})
async def patch_to_do_item(item: UpdateItem):
    try:
        return todos.patch_item(item)
    except StopIteration:
        raise HTTPException(404, detail="Item not found")


@app.delete("/item", response_model=Status, tags=["todo"])
async def delete_to_do_item(username: str, created_at: str):
    todos.delete_item(username, created_at)
    return {"status": "deleted"}

