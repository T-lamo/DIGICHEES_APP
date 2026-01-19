






# def test_addition():
#     assert 2 + 2 == 4

from .conftest import client
from fastapi.testclient import TestClient

def test_conditionnement(client: TestClient):
    response = client.get("/conditionnements/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)


def test_create_conditionnement(client):
    payload = {
        "libelle": "Boîte carton",
        "description": "Conditionnement test"
    }

    response = client.post("/conditionnements/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["libelle"] == "Boîte carton"
    assert "id" in data


def test_list_conditionnements(client):
    for i in range(3):
        client.post("/conditionnements/", json={
            "libelle": f"Cond {i}",
            "description": "Test"
        })

    response = client.get("/conditionnements/?limit=2&offset=0")

    assert response.status_code == 200
    data = response.json()

    # assert "items" in data
    # assert len(data["items"]) == 2

