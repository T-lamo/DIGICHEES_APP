from fastapi.testclient import TestClient
from src.models import ConditionnementBase


def test_get_list_conditionnement(client):
    response = client.get("/conditionnements/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)
    print(data["data"])

def test_get_limited_list_conditionnements(client):
    for i in range(3):
        client.post("/conditionnements/", json={
        "libelle": "Montre Connectée",
        "poids": 5,
        "prix": "229.99",
        "ordreimp": 4
    })

    response = client.get("/conditionnements/?limit=2&offset=0")
    assert response.status_code == 200

    data = response.json()
    assert data["limit"] == 2
    assert len(data["data"]) == 2


def test_create_conditionnement(client):
    payload = {
        "libelle": "Montre Connectée",
        "poids": 5,
        "prix": "229.99",
        "ordreimp": 4
    }

    response = client.post("/conditionnements/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["libelle"] == "Montre Connectée"
    assert "id" in data


def test_get_conditionnement(client: TestClient):
    payload = {
        "libelle": "Montre Connectée",
        "poids": 5,
        "prix": "229.99",
        "ordreimp": 4
    }

    response = client.post("/conditionnements/", json=payload)
    assert response.status_code == 201

    response = client.get("/conditionnements/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_conditionnement(client: TestClient):
    payload = {
        "libelle": "Montre Connectée",
        "poids": 5,
        "prix": "229.99",
        "ordreimp": 4
    }

    response = client.post("/conditionnements/", json=payload)
    assert response.status_code == 201

    payload = {"libelle":"Montre"}
    response = client.patch("/conditionnements/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["libelle"] == "Montre"

def test_delete_conditionnement(client: TestClient):
    payload = {
        "libelle": "Montre Connectée",
        "poids": 5,
        "prix": "229.99",
        "ordreimp": 4
    }

    response = client.post("/conditionnements/", json=payload)
    assert response.status_code == 201

    response = client.delete("/conditionnements/1")
    assert response.status_code == 204