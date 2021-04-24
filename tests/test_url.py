import requests


def test_url(request):
    url = request.config.getoption("--url")
    status_code = int(request.config.getoption("--status_code"))

    response = requests.get(url)

    assert response.status_code == status_code
