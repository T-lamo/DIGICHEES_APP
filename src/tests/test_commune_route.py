from .conftest import client
from fastapi.testclient import TestClient


def test_get_list_commune(client: TestClient):
    response = client.get("/communes/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_limited_list_communes(client):
    payload = {
          "code": "75",
          "nom": "Paris",
          "ordre_aff": 1
        }
    client.post("/departements/", json=payload)
    for i in range(3):
        client.post("/communes/", json={
          "code_departement": 1,
          "cp": f"750{i}0",
          "nom": "Paris"
        })

    response = client.get("/communes/?limit=2&offset=0")
    assert response.status_code == 200

    data = response.json()
    assert data["limit"] == 2
    assert len(data["data"]) == 2


def test_create_commune(client):
    payload = {
          "code": "75",
          "nom": "Paris",
          "ordre_aff": 1
        }
    client.post("/departements/", json=payload)
    payload = {
          "code_departement": 1,
          "cp": "75000",
          "nom": "Paris"
        }

    response = client.post("/communes/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert float(data["cp"]) == 75000
    assert "id" in data


def test_get_commune(client: TestClient):
    test_create_commune(client)
    response = client.get("/communes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_commune(client: TestClient):
    test_create_commune(client)

    payload = {"cp":"75011"}
    response = client.patch("/communes/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert float(data["cp"]) == 75011

def test_delete_commune(client: TestClient):
    test_create_commune(client)

    response = client.delete("/communes/1")
    assert response.status_code == 204
