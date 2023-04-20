from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_joke():
    """
    Assert status code 200 in fetching jokes
    """
    response = client.get("/joke", headers={"Accept": "application/json"})
    assert response.status_code == 200


def test_get_joke_wrong_type():
    """
    Assert bad type of joke
    """
    response = client.get("/joke/chick", headers={"Accept": "application/json"})
    assert response.status_code == 400
    assert response.json() == {"detail": 'Joke type must be "Chuck" o "Dad"'}


def test_get_joke_chuck_type():
    """
    Assert status code 200 in fetching Chuck jokes
    """
    response = client.get("/joke/chuck", headers={"Accept": "application/json"})
    assert response.status_code == 200


def test_get_joke_dad_type():
    """
    Assert status code 200 in fetching Dad jokes
    """
    response = client.get("/joke/dad", headers={"Accept": "application/json"})
    assert response.status_code == 200


#######
# Math
#######


def test_lcm_good():
    """
    Assert status code 200 and correct LCM
    """
    response = client.get("/lcm?numbers=1,2,3", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.json() == {"lcm": 6}


def test_lcm_bad_pass_wrong_separator():
    """
    Assert status code 400 and incorrect separator in integer list
    """
    response = client.get("/lcm?numbers=1,2-3", headers={"Accept": "application/json"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "List must contain only integers and be separated by commas (,)"
    }


def test_lcm_bad_pass_letters():
    """
    Assert status code 400 and incorrect items in integer list
    """
    response = client.get("/lcm?numbers=1,2,A", headers={"Accept": "application/json"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "List must contain only integers and be separated by commas (,)"
    }


def test_plus_one_good():
    """
    Assert status code 200 and correct addition
    """
    response = client.get(
        "/plus-one?number=123",
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == {"result": 124}


def test_plus_one_bad_format():
    """
    Assert status code 422 for incorrect input (only integers)
    """
    response = client.get(
        "/plus-one?number=bad", headers={"Accept": "application/json"}
    )
    assert response.status_code == 422
