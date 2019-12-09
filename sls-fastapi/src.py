from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class BasicError(BaseModel):
    detail: str


class Status(BaseModel):
    status: str


class TodoPatch(BaseModel):
    todo: str


class TodoPost(TodoPatch):
    username: str = Field("John Doe")


class Item(BaseModel):
    id: int
    todo: str
    username: str
    created_at: datetime
    updated_at: datetime = Field(None)


class Items(BaseModel):
    items: List[Item] = []


class TodoItems:
    def __init__(self):
        self.items = [
            {
                "id": 1,
                "todo": "Watch Parasite",
                "username": "John Doe",
                "created_at": datetime.utcnow(),
            }
        ]

    def item(self, id):
        return next(i for i in self.items if i["id"] == id)

    def create_item(self, item: TodoPost):
        new_item = {
            "id": len(self.items) + 1,
            "todo": item.todo,
            "username": item.username,
            "created_at": datetime.utcnow(),
        }
        self.items.append(new_item)
        return new_item

