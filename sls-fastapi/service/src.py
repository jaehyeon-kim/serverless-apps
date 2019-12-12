import os
from typing import List, Union
from datetime import datetime
from pydantic import BaseModel, Field
import boto3
from boto3.dynamodb.conditions import Key


def set_dt_field(is_optional: bool):
    desc = "Datetime string, format - eg) 2019-01-01T12:00:00Z"
    if is_optional:
        return Field(None, description=desc)
    else:
        return Field(..., description=desc)


class BasicError(BaseModel):
    detail: str


class Status(BaseModel):
    status: str


class NewItem(BaseModel):
    username: str
    todo: str
    when_at: str = set_dt_field(is_optional=True)


class PatchItem(NewItem):
    todo: str = None
    created_at: str = set_dt_field(is_optional=False)


class ItemFields(BaseModel):
    todo: str
    username: str
    when_at: str = None
    created_at: str = set_dt_field(is_optional=False)
    updated_at: str = set_dt_field(is_optional=False)


class Item(BaseModel):
    item: Union[ItemFields, dict]


class Items(BaseModel):
    items: Union[List[ItemFields], list]


class TodoItems:
    def __init__(self):
        self.endpoint_url = os.getenv("LOCAL_STACK_ENDPOINT_URL")
        self.tablename = os.environ["TABLE_NAME"]
        self.dt_format = "%Y-%m-%dT%H:%M:%SZ"

    def get_items(self, username: str, created_at: str, all_items: bool = False):
        if all_items:
            args = {
                "KeyConditionExpression": Key("username").eq(username)
                & Key("created_at").gte(created_at),
                "ScanIndexForward": False,
            }
            resp = self._table().query(**args)
            return {"items": resp.get("Items", [])}
        else:
            resp = self._table().get_item(Key={"username": username, "created_at": created_at})
            return {"item": resp.get("Item", {})}

    def create_item(self, item: NewItem):
        args = {"todo": item.todo, "username": item.username, "is_create": True}
        return self._upsert_item(**args)

    def update_item(self, item: PatchItem):
        args = {"todo": item.todo, "username": item.username, "created_at": item.created_at}
        return self._upsert_item(**args)

    def delete_item(self, username: str, created_at: str):
        self._table().delete_item(Key={"username": username, "created_at": created_at})

    def is_exist(self, username: str, created_at: str):
        return len(TodoItems().get_items(username, created_at, all_items=False)["item"]) > 0

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

    def _upsert_item(self, **kwargs):
        dt = datetime.utcnow().strftime(self.dt_format)
        created_at = kwargs["created_at"] if kwargs.get("created_at") else dt
        if kwargs.get("is_create"):
            self._table().put_item(
                Item={
                    "todo": kwargs["todo"],
                    "username": kwargs["username"],
                    "created_at": created_at,
                    "updated_at": dt,
                }
            )
        else:
            args = {
                **{"Key": {"username": kwargs["username"], "created_at": created_at}},
                **self._set_expr_values({**kwargs, **{"updated_at": dt}}),
            }
            self._table().update_item(**args)
        return self.get_items(kwargs["username"], created_at, all_items=False)

    def _set_expr_values(self, d):
        keys = ["todo", "when_at", "updated_at"]
        expr = "set {0}".format(
            ", ".join(["{0} = :{0}value".format(k) for k, _ in d.items() if k in keys])
        )
        expr_values = {}
        for k, _ in d.items():
            if k in keys:
                expr_values.update({":{0}value".format(k): d[k]})
        return {"UpdateExpression": expr, "ExpressionAttributeValues": expr_values}
