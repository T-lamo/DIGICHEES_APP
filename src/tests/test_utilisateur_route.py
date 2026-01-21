from .conftest import client
from fastapi.testclient import TestClient


def test_get_list_utilisateur(client: TestClient, auth_headers: dict):
    response = client.get("/utilisateurs/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_limited_list_utilisateurs(client, auth_headers: dict):
    client.post("/roles/", json={"librole": "Admin"})
    for i in range(3):
        client.post("/utilisateurs/", json={
        "nom_utilisateur": "Martin",
        "prenom_utilisateur": "Sophie",
        "username": f"smartin{i}",
        "couleur_fond_utilisateur": 5,
        "date_insc_utilisateur": "2024-02-20",
        "disabled": "false",
        "password": "Sophie2024@",
        "roles_ids": [1]
    })

    response = client.get("/utilisateurs/?limit=2&offset=0", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["limit"] == 2
    assert len(data["data"]) == 2

def test_create_utilisateur(client):
    payload = {
        "librole": "Admin"
    }
    response = client.post("/roles/", json=payload)
    assert response.status_code == 201

    payload = {
        "nom_utilisateur": "Martin",
        "prenom_utilisateur": "Sophie",
        "username": "smartin",
        "couleur_fond_utilisateur": 5,
        "date_insc_utilisateur": "2024-02-20",
        "disabled": "false",
        "password": "Sophie2024@",
        "roles_ids": [1]
    }
    response = client.post("/utilisateurs/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data

def test_get_utilisateur(client: TestClient, auth_headers: dict):

    test_create_utilisateur(client)

    response = client.get("/utilisateurs/1", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_utilisateur(client: TestClient, auth_headers: dict):
    test_create_utilisateur(client)

    payload = {"couleur_fond_utilisateur":6}
    response = client.patch("/utilisateurs/1", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert float(data["couleur_fond_utilisateur"]) == 6

def test_delete_utilisateur(client: TestClient, auth_headers: dict):
    test_create_utilisateur(client)

    response = client.delete("/utilisateurs/1", headers=auth_headers)
    assert response.status_code == 204
