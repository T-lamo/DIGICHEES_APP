from .conftest import client
from fastapi.testclient import TestClient


def test_get_list_objet(client: TestClient):
    response = client.get("/objets/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_limited_list_objets(client):
    for i in range(3):
        client.post("/objets/", json={
        "libobj": "Haltère Réglable 20kg",
        "tailleobj": "45x15x15 cm",
        "puobj": "79.50",
        "objetsobj": "20.0",
        "indispobj": 1,
        "o_imp": 4,
        "o_aff": 5,
        "o_cartp": 6,
        "points": 80,
        "o_ordre_aff": 2
    })

    response = client.get("/objets/?limit=2&offset=0")
    assert response.status_code == 200

    data = response.json()
    assert data["limit"] == 2
    assert len(data["data"]) == 2


def test_create_objet(client):
    payload = {
        "libobj": "Haltère Réglable 20kg",
        "tailleobj": "45x15x15 cm",
        "puobj": "79.50",
        "objetsobj": "20.0",
        "indispobj": 1,
        "o_imp": 4,
        "o_aff": 5,
        "o_cartp": 6,
        "points": 80,
        "o_ordre_aff": 2
    }

    response = client.post("/objets/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert "libobj" in data


def test_get_objet(client: TestClient):
    payload = {
        "libobj": "Haltère Réglable 20kg",
        "tailleobj": "45x15x15 cm",
        "puobj": "79.50",
        "objetsobj": "20.0",
        "indispobj": 1,
        "o_imp": 4,
        "o_aff": 5,
        "o_cartp": 6,
        "points": 80,
        "o_ordre_aff": 2
    }

    response = client.post("/objets/", json=payload)
    assert response.status_code == 201

    response = client.get("/objets/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_objet(client: TestClient):
    payload = {
        "libobj": "Haltère Réglable 20kg",
        "tailleobj": "45x15x15 cm",
        "puobj": "79.50",
        "objetsobj": "20.0",
        "indispobj": 1,
        "o_imp": 4,
        "o_aff": 5,
        "o_cartp": 6,
        "points": 80,
        "o_ordre_aff": 2
    }

    response = client.post("/objets/", json=payload)
    assert response.status_code == 201

    payload = {"indispobj":5}
    response = client.patch("/objets/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert float(data["indispobj"]) == 5

def test_delete_objet(client: TestClient):
    payload = {
        "libobj": "Haltère Réglable 20kg",
        "tailleobj": "45x15x15 cm",
        "puobj": "79.50",
        "objetsobj": "20.0",
        "indispobj": 1,
    }

    response = client.post("/objets/", json=payload)
    assert response.status_code == 201

    response = client.delete("/objets/1")
    assert response.status_code == 204

