import pytest
import requests

base_url = "https://jsonplaceholder.typicode.com"


@pytest.mark.parametrize("post_id", [1, 2])
def test_delete_post(post_id):
    response = requests.delete(base_url + "/posts/" + str(post_id))
    assert response.status_code == 200


def test_update_post():
    data = {"title": "new_title"}
    response = requests.put(base_url + "/posts/1", json=data)
    assert response.json() == {
        "title": "new_title",
        "id": 1
    }


def test_create_post():
    data = {"title": "new_title"}
    response = requests.post(base_url + "/posts", json=data)
    assert response.json() == {
        "title": "new_title",
        "id": 101
    }


def test_patch_post():
    data = {"userId": 500}
    response = requests.patch(base_url + "/posts/1", json=data)
    response_json = response.json()
    assert response_json["id"] == 1
    assert response_json["userId"] == 500


def test_get_invalid_user_id(user_id):
    response = requests.get(base_url + "/users/" + str(user_id))
    assert response.status_code == 404
    assert response.json() == {}
