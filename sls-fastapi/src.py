from typing import List
from datetime import datetime
from pydantic import BaseModel


class BasicError(BaseModel):
    detail: str


class Status(BaseModel):
    status: str


class ChangeItem(BaseModel):
    todo: str


class NewItem(ChangeItem):
    username: str = "John Doe"


class Item(BaseModel):
    id: int
    todo: str
    username: str = "John Doe"
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = None


class Items(BaseModel):
    records: List[Item] = []


class TodoItems:
    def __init__(self):
        self.items = Items(records=[Item(id=1, todo="Watch Parasite")])

    def item(self, todo_id: int):
        return next(r for r in self.items.records if r.id == todo_id)

    def create_item(self, item: NewItem):
        new_item = Item(id=len(self.items.records) + 1, todo=item.todo, username=item.username)
        self.items.records.append(new_item)
        return new_item

    def patch_item(self, todo_id: int, todo: str):
        item = next(r for r in self.items.records if r.id == todo_id)
        item.todo = todo
        item.updated_at = datetime.utcnow()
        return item

    def delete_item(self, todo_id: int):
        self.items.records = [r for r in self.items.records if r.id != todo_id]
