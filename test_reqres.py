import json

import requests
from jsonschema import validate

from schemas import post_users

url = "https://reqres.in/api/users"

payload = {"name": "morpheus", "job": "leader"}

response = requests.request("POST", url, data=payload)

print(response.text)


def test_schema_validate_from_file():
    response = requests.post("https://reqres.in/api/users", data={"name": "morpheus", "job": "master"})
    body = response.json()

    assert response.status_code == 201
    with open("post_users.json") as file:
        validate(body, schema=json.loads(file.read()))


def test_schema_validate_from_variable():
    response = requests.post("https://reqres.in/api/users", data={"name": "morpheus", "job": "master"})
    body = response.json()

    assert response.status_code == 201
    validate(body, schema=post_users)


def test_job_name_from_request_returns_in_response():
    job = "master"
    name = "morpheus"

    response = requests.post("https://reqres.in/api/users", json={"name": name, "job": job})
    body = response.json()

    assert body["name"] == name
    assert body["job"] == job


def test_get_users_returns_unique_users():
    response = requests.get(
        url="https://reqres.in/api/users",
        params={"page": 2, "per_page": 4},
        verify=False
    )
    ids = [element["id"] for element in response.json()["data"]]

    assert len(ids) == len(set(ids))