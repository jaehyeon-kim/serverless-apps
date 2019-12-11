import os
from typing import List, Union
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


class ItemFields(BaseModel):
    todo: str
    username: str
    created_at: str
    updated_at: str


class Item(BaseModel):
    item: Union[ItemFields, dict]


class Items(BaseModel):
    items: List[ItemFields] = []


class TodoItems:
    def __init__(self):
        self.endpoint_url = os.getenv("LOCAL_STACK_ENDPOINT_URL", None)
        self.tablename = os.environ["TABLE_NAME"]
        self.dt_format = "%Y-%m-%dT%H:%M:%SZ"
        self.hash_key = "username"
        self.range_key = "created_at"

    def _table(self):
        if not self.endpoint_url:
            return boto3.resource("dynamodb").Table(self.tablename)
        else:
            session = boto3.session.Session()
            return session.resource(
                service_name="dynamodb",
                region_name=os.environ["AWS_DEFAULT_REGION"],
                endpoint_url=self.endpoint_url,
            ).Table(self.tablename)

    def get_items(self, username: str, created_at: str, all_items: bool = False):
        if all_items:
            args = {
                "KeyConditionExpression": Key(self.hash_key).eq(username)
                & Key(self.range_key).gte(created_at),
                "ScanIndexForward": False,
            }
            resp = self._table().query(**args)
            return {"items": resp.get("Items", [])}
        else:
            resp = self._table().get_item(Key={"username": username, "created_at": created_at})
            return {"item": resp.get("Item", {})}

    def create_item(self, item: NewItem):
        created_at = datetime.utcnow().strftime(self.dt_format)
        self._table().put_item(
            Item={
                "todo": item.todo,
                "username": item.username,
                "created_at": created_at,
                "updated_at": created_at,
            }
        )
        return self.get_items(item.username, created_at, all_items=False)

    def update_item(self, item: UpdateItem):
        return {}

    def delete_item(self, username: str, created_at: str):
        self._table().delete_item(
            Key={"username": username, "created_at": created_at,}
        )
