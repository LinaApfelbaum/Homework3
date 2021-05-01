import pytest
import requests

base_url = "https://api.openbrewerydb.org"
test_breweries = requests.get(base_url + "/breweries?per_page=2").json()


def test_get_breweries_list():
    response = requests.get(base_url + "/breweries")
    response_json = response.json()
    assert response_json[0]["id"] == 8034
    assert response.status_code == 200


@pytest.mark.parametrize("brewery_type", ["closed", "planning", "nano"])
def test_get_breweries_by_type(brewery_type):
    response = requests.get(base_url + "/breweries?by_type=" + brewery_type)
    response_json = response.json()
    assert response.status_code == 200
    for el in response_json:
        assert el["brewery_type"] == brewery_type


@pytest.mark.parametrize("brewery_id, name", [
    (test_breweries[0]["id"], test_breweries[0]["name"]),
    (test_breweries[1]["id"], test_breweries[1]["name"])
])
def test_get_single_brewery(brewery_id, name):
    response = requests.get(base_url + "/breweries/" + str(brewery_id))
    response_json = response.json()
    assert response_json["id"] == brewery_id
    assert response_json["name"] == name


@pytest.mark.parametrize("brewery_id, status_code, error_message", [
    (0, 404, "Couldn't find Brewery with 'id'=0"),
    (99999999999999999999999999, 404,
     "Couldn't find Brewery with an out of range value for 'id'")
])
def test_get_single_brewery_errors(brewery_id, status_code, error_message):
    response = requests.get(base_url + "/breweries/" + str(brewery_id))
    response_json = response.json()
    assert response.status_code == status_code
    assert response_json["message"] == error_message


def test_autocomplete():
    response = requests.get(
        base_url + "/breweries/autocomplete?query=nake%20River%20Brewing")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == [
        {
            "id": "14412",
            "name": "Snake River Brewing Co"
        }
    ]
