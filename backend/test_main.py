import os
import time
import json
import logging
import pytest
from starlette.testclient import TestClient
from main import app

from main import app
from src.todo import TodoItems
from src.models import NewItem


def wait_for_db():
    while True:
        try:
            TodoItems()._table()
            break
        except Exception:
            logging.info("waiting for dynamodb table to be ready")
            time.time(1)


wait_for_db()


def test_hello_world():
    resp = TestClient(app).get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_record():
    username = "jakim"
    todo = "Watch Parisite"
    resp = TestClient(app).post("/item", data={"username": username, "todo": todo})
    result = resp.json()
    print(result)
    assert resp.status_code == 200
    assert resp["username"] == username
    assert resp["todo"] == todo
