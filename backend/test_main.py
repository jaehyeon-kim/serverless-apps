import os
import time
import json
import pytest
from typing import Dict
from datetime import datetime
from starlette.testclient import TestClient

from main import app
from src.todo import TodoItems
from src.models import NewItem


def update_ats(result: Dict[str, str]):
    return {
        "created_at": result["item"]["created_at"],
        "updated_at": result["item"]["updated_at"],
    }


def get_items_resp(username: str, created_at: str, all_items: bool = False):
    params = {"username": username, "created_at": created_at, "all_items": all_items}
    return TestClient(app).get("/items", params=params)


pytest.ats = {"created_at": None, "updated_at": None}


@pytest.fixture(scope="module")
def todo_item():
    return {"username": "jakim", "todo": "Watch Parasite", "new_todo": "Watch Frozen 2"}


def test_hello_world():
    resp = TestClient(app).get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.parametrize("all_items", [True, False])
def test_no_item(all_items):
    resp = get_items_resp(username="FOO", created_at="2019-01-01", all_items=all_items)
    assert resp.status_code == 404


@pytest.mark.dependency(name="create")
def test_create_item(todo_item):
    data = {k: v for k, v in todo_item.items() if k != "new_todo"}
    resp = TestClient(app).post("/item", data=json.dumps(data))
    result = resp.json()
    pytest.ats = update_ats(result)
    assert resp.status_code == 200
    assert result["item"]["username"] == data["username"]
    assert result["item"]["todo"] == data["todo"]


@pytest.mark.dependency(name="update", depends=["create"])
def test_update_item(todo_item):
    data = {
        "username": todo_item["username"],
        "todo": todo_item["new_todo"],
        "created_at": pytest.ats["created_at"],
    }
    resp = TestClient(app).patch("/item", data=json.dumps(data))
    result = resp.json()

    assert resp.status_code == 200
    assert result["item"]["username"] == data["username"]
    assert result["item"]["todo"] == data["todo"]
    assert result["item"]["created_at"] == data["created_at"]

    # assert datetime.strptime(
    #     result["item"]["updated_at"], TodoItems().dt_format
    # ) > datetime.strptime(pytest.ats["updated_at"], TodoItems().dt_format)

    pytest.ats = update_ats(result)


@pytest.mark.dependency(name="read", depends=["create"])
@pytest.mark.parametrize("all_items", [True, False])
def test_read_item(todo_item, all_items):
    resp = get_items_resp(
        username=todo_item["username"], created_at=pytest.ats["created_at"], all_items=all_items
    )
    assert resp.status_code == 200


@pytest.mark.dependency(name="read", depends=["create"])
def test_delete_item(todo_item):
    params = {
        "username": todo_item["username"],
        "created_at": pytest.ats["created_at"],
    }
    resp = TestClient(app).delete("/item", params=params)
    assert resp.status_code == 200
