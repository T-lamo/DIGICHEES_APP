from .conftest import client
from fastapi.testclient import TestClient



def test_get_list_poids(client: TestClient):
    response = client.get("/poids/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_limited_list_poids(client):
    for i in range(3):
        client.post("/poids/", json={
              "min": i*2,
              "value": i*6
            })

    response = client.get("/poids/?limit=2&offset=0")
    assert response.status_code == 200

    data = response.json()
    assert data["limit"] == 2
    assert len(data["data"]) == 2


def test_create_poids(client):
    payload = {
              "min": 5,
              "value": 15
            }

    response = client.post("/poids/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert "min" in data
    assert "id" in data


def test_get_poids(client: TestClient):
    payload = {
              "min": 5,
              "value": 15
            }

    response = client.post("/poids/", json=payload)
    assert response.status_code == 201

    response = client.get("/poids/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_poids(client: TestClient):
    payload = {
              "min": 5,
              "value": 15
            }

    response = client.post("/poids/", json=payload)
    assert response.status_code == 201

    payload = {"min":"6"}
    response = client.patch("/poids/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert float(data["min"]) == 6

def test_delete_poids(client: TestClient):
    payload = {
              "min": 5,
              "value": 15
            }

    response = client.post("/poids/", json=payload)
    assert response.status_code == 201

    response = client.delete("/poids/1")
    assert response.status_code == 204

