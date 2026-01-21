from .conftest import client
from fastapi.testclient import TestClient


def test_get_list_departement(client: TestClient):
    response = client.get("/departements/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_limited_list_departements(client):
    for i in range(3):
        client.post("/departements/", json={
          "code": f"7{i}",
          "nom": "Paris",
          "ordre_aff": 1+i
        })

    response = client.get("/departements/?limit=2&offset=0")
    assert response.status_code == 200

    data = response.json()
    assert data["limit"] == 2
    assert len(data["data"]) == 2


def test_create_departement(client):
    payload = {
          "code": "75",
          "nom": "Paris",
          "ordre_aff": 1
        }

    response = client.post("/departements/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert float(data["code"]) == 75
    assert "id" in data


def test_get_departement(client: TestClient):
    test_create_departement(client)

    response = client.get("/departements/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_departement(client: TestClient):
    test_create_departement(client)

    payload = {"code":"74"}
    response = client.patch("/departements/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert float(data["code"]) == 74

def test_delete_departement(client: TestClient):
    test_create_departement(client)

    response = client.delete("/departements/1")
    assert response.status_code == 204
