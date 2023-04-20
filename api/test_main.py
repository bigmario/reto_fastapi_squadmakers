from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_joke():
    response = client.get("/joke", headers={"Accept": "application/json"})
    assert response.status_code == 200


def test_get_joke_wrong_type():
    response = client.get("/joke/chick", headers={"Accept": "application/json"})
    assert response.status_code == 400
    assert response.json() == {"detail": 'Joke type must be "Chuck" o "Dad"'}


def test_get_joke_chuck_type():
    response = client.get("/joke/chuck", headers={"Accept": "application/json"})
    assert response.status_code == 200


def test_get_joke_dad_type():
    response = client.get("/joke/dad", headers={"Accept": "application/json"})
    assert response.status_code == 200


#######
# Math
#######


def test_lcm_good():
    response = client.get("/lcm?numbers=1,2,3", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.json() == {"lcm": 6}


def test_lcm_bad_pass_wrong_separator():
    response = client.get("/lcm?numbers=1,2-3", headers={"Accept": "application/json"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "List must contain only integers and be separated by commas (,)"
    }


def test_lcm_bad_pass_letters():
    response = client.get("/lcm?numbers=1,2,A", headers={"Accept": "application/json"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "List must contain only integers and be separated by commas (,)"
    }


def test_plus_one_good():
    response = client.get(
        "/plus-one?number=123",
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == {"result": 124}


def test_plus_one_bad_format():
    response = client.get(
        "/plus-one?number=bad", headers={"Accept": "application/json"}
    )
    assert response.status_code == 422
