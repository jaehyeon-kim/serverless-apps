import os
import json
import requests
from pprint import pprint
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

api_host = os.getenv("API_HOST", "simple-todo.jaehyeon.me")
api_base_path = os.getenv("API_BASE_PATH", "api")
aws_region = os.getenv("AWS_REGION", "ap-southeast-2")
base_url = "https://{0}/{1}".format(api_host, api_base_path)

auth = BotoAWSRequestsAuth(aws_host=api_host, aws_region=aws_region, aws_service="execute-api")


def set_data(**kwargs):
    data = {}
    for k, v in kwargs.items():
        if k in ["username", "created_at", "all_items", "todo"]:
            data.update({k: v})
    return data


## hello world
resp = requests.get(base_url, auth=auth)
# resp.json()
# {'status': 'ok'}

## all items
params = set_data(username="jakim", created_at="2020-01-01", all_items=True)
resp = requests.get("{0}/items".format(base_url), auth=auth, params=params)
# resp.json()
# {'detail': 'No items found'}

## create item
data = set_data(username="jakim", todo="Watch Parasite")
resp = requests.post("{0}/item".format(base_url), auth=auth, data=json.dumps(data))
# resp.json()
# {
#     "item": {
#         "todo": "Watch Parasite",
#         "username": "jakim",
#         "created_at": "2020-01-05T21:47:49Z",
#         "updated_at": "2020-01-05T21:47:49Z",
#     }
# }


# will be used for query/delete
keys = {
    "username": resp.json()["item"]["username"],
    "created_at": resp.json()["item"]["created_at"],
}

## update item
new_item = {k: v for k, v in resp.json()["item"].items() if k in ["username", "created_at"]}
new_item.update({"todo": "Watch Frozen 2"})

resp = requests.patch("{0}/item".format(base_url), auth=auth, data=json.dumps(new_item))
# resp.json()
# {
#     "item": {
#         "todo": "Watch Frozen 2",
#         "username": "jakim",
#         "created_at": "2020-01-05T21:47:49Z",
#         "updated_at": "2020-01-05T21:48:39Z",
#     }
# }

## get item
resp = requests.get("{0}/items".format(base_url), auth=auth, params=set_data(**keys))
# resp.json()
# {
#     "item": {
#         "todo": "Watch Frozen 2",
#         "username": "jakim",
#         "created_at": "2020-01-05T21:47:49Z",
#         "updated_at": "2020-01-05T21:48:39Z",
#     }
# }

## delete item
resp = requests.delete("{0}/item".format(base_url), auth=auth, params=set_data(**keys))
# resp.json()
# {"status": "deleted"}

