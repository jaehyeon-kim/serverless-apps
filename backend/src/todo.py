import os
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key

from src.models import NewItem, PatchItem


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
        keys = ["todo", "updated_at"]
        expr = "set {0}".format(
            ", ".join(["{0} = :{0}value".format(k) for k, _ in d.items() if k in keys])
        )
        expr_values = {}
        for k, _ in d.items():
            if k in keys:
                expr_values.update({":{0}value".format(k): d[k]})
        return {"UpdateExpression": expr, "ExpressionAttributeValues": expr_values}
