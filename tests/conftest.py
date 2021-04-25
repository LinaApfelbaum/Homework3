import json
import pathlib


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="https://ya.ru/"
    )

    parser.addoption(
        "--status_code",
        default="200"
    )


def pytest_generate_tests(metafunc):
    if "user_id" in metafunc.fixturenames:
        data_path = str(pathlib.Path(__file__).parent.absolute()) + \
            '/data/invalid_users.json'
        with open(data_path, "r") as json_file:
            invalid_users = json.load(json_file)

        metafunc.parametrize("user_id", invalid_users)
