from .conftest import client
from fastapi.testclient import TestClient


def test_get_list_role(client: TestClient):
    response = client.get("/roles/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_limited_list_roles(client):
    roles = [
    {
        "librole": "Admin"
    },
    {
        "librole": "Operateur_colis"
    },
    {
        "librole": "Operateur_stock"
    }
]
    for role in roles:
        client.post("/roles/", json=role)

    response = client.get("/roles/?limit=2&offset=0")
    assert response.status_code == 200

    data = response.json()
    assert data["limit"] == 2
    assert len(data["data"]) == 2


def test_create_role(client):
    payload = {
        "librole": "Admin"
    }

    response = client.post("/roles/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["librole"] == "Admin"
    assert "id" in data

def test_create_bad_role(client):
    payload = {
        "librole": "Courtier"
    }

    response = client.post("/roles/", json=payload)

    assert response.status_code == 422


def test_get_role(client: TestClient):
    test_create_role(client)

    response = client.get("/roles/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_role(client: TestClient):
    test_create_role(client)

    payload = {
        "librole": "Operateur_colis"
    }
    response = client.patch("/roles/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["librole"] == "Operateur_colis"

def test_delete_role(client: TestClient):
    test_create_role(client)

    response = client.delete("/roles/1")
    assert response.status_code == 204
