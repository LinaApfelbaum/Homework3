import pytest
import requests
from jsonschema import validate

dog_api_base_url = "https://dog.ceo/api"
breeds = requests.get(
    dog_api_base_url + "/breeds/list/all").json()["message"].keys()
test_breeds = list(breeds)[0:3]


def test_get_breeds_list():
    response = requests.get(dog_api_base_url + "/breeds/list/all")
    schema = {
        "type": "object",
        "properties": {
                "status": {"type": "string"},
                "message": {
                    "type": "object",
                    "patternProperties": {
                        "": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                },
        },
        "required": ["status", "message"]
    }

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_get_random_image():
    response = requests.get(dog_api_base_url + "/breeds/image/random")
    schema = {
        "type": "object",
        "properties": {
                "status": {"type": "string"},
                "message": {"type": "string"},
        },
        "required": ["status", "message"]
    }

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200
    assert "images.dog.ceo" in response.json()["message"]


@pytest.mark.parametrize("breed", test_breeds)
def test_get_by_breed(breed):
    response = requests.get(dog_api_base_url + "/breed/" + breed + "/images")
    schema = {
        "type": "object",
        "properties": {
                "status": {"type": "string"},
                "message": {
                    "type": "array",
                    "items": {"type": "string"}
                },
        },
        "required": ["status", "message"]
    }

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200


def test_get_by_sub_breed():
    response = requests.get(dog_api_base_url + "/breed/hound/list")
    schema = {
        "type": "object",
        "properties": {
                "status": {"type": "string"},
                "message": {
                    "type": "array",
                    "items": {"type": "string"}
                },
        },
        "required": ["status", "message"]
    }

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200


@pytest.mark.parametrize("breed", ["akita", "boxer", "borzoi"])
def test_get_random_image_by_breed(breed):
    response = requests.get(
        dog_api_base_url + "/breed/" + breed + "/images/random")
    image_url = response.json()["message"]
    image_response = requests.get(image_url)
    assert "image/" in image_response.headers["Content-Type"]
    assert image_response.status_code == 200
