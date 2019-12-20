import os
import json
import requests
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

api_host = os.getenv("API_HOST", "simple-todo.jaehyeon.me")
api_base_path = os.getenv("API_BASE_PATH", "api")
aws_region = os.getenv("AWS_REGION", "ap-southeast-2")
base_url = "https://{0}/{1}".format(api_host, api_base_path)

auth = BotoAWSRequestsAuth(aws_host=api_host, aws_region=aws_region, aws_service="execute-api")


def set_items_url(base_url: str, username: str = "JAKIM", created_at: str = "2019-01-01"):
    return "{0}/items?username={1}&created_at={2}".format(base_url, username, created_at)


resp = requests.get(base_url)
resp = requests.get(base_url, auth=auth)

resp = requests.get(set_items_url(base_url))
resp = requests.get(set_items_url(base_url), auth=auth)
