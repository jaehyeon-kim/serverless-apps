import os
from typing import List
from datetime import datetime
from pydantic import BaseModel
import boto3
from boto3.dynamodb.conditions import Key


class BasicError(BaseModel):
    detail: str


class Status(BaseModel):
    status: str


class NewItem(BaseModel):
    username: str
    todo: str


class UpdateItem(NewItem):
    created_at: datetime


class Item(BaseModel):
    todo: str
    username: str
    created_at: datetime
    updated_at: datetime = None


class Items(BaseModel):
    records: List[Item] = []


class TodoItems:
    def __init__(self):
        self.table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
        self.hash_key = "username"
        self.range_key = "created_at"

    def get_items(self, username: str, created_at: str, all_items: bool):
        return []

    def create_item(self, item: NewItem):
        return {}

    def patch_item(self, item: UpdateItem):
        return {}

    def delete_item(self, username: str, created_at: str):
        return {}

    # def item(self, todo_id: int):
    #     return next(r for r in self.items.records if r.id == todo_id)

    # def create_item(self, item: NewItem):
    #     new_item = Item(id=len(self.items.records) + 1, todo=item.todo, username=item.username)
    #     self.items.records.append(new_item)
    #     return new_item

    # def patch_item(self, todo_id: int, todo: str):
    #     item = next(r for r in self.items.records if r.id == todo_id)
    #     item.todo = todo
    #     item.updated_at = datetime.utcnow()
    #     return item

    # def delete_item(self, todo_id: int):
    #     self.items.records = [r for r in self.items.records if r.id != todo_id]
