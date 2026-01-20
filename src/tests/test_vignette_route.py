from .conftest import client
from fastapi.testclient import TestClient


def test_get_list_vignette(client: TestClient):
    response = client.get("/vignettes/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_limited_list_vignettes(client):
    for i in range(3):
        client.post("/vignettes/", json={
    "min": 18 + i,
    "value": 30 + i
})

    response = client.get("/vignettes/?limit=2&offset=0")
    assert response.status_code == 200

    data = response.json()
    assert data["limit"] == 2
    assert len(data["data"]) == 2


def test_create_vignette(client):
    payload = {
                "min": 18,
                "value": 30
            }

    response = client.post("/vignettes/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert float(data["value"]) == 30
    assert "id" in data


def test_get_vignette(client: TestClient):
    payload = {
                "min": 18,
                "value": 30
            }

    response = client.post("/vignettes/", json=payload)
    assert response.status_code == 201

    response = client.get("/vignettes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_vignette(client: TestClient):
    payload = {
                "min": 18,
                "value": 30
            }

    response = client.post("/vignettes/", json=payload)
    assert response.status_code == 201

    payload = {"min":20}
    response = client.patch("/vignettes/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert float(data["min"]) == 20

def test_delete_vignette(client: TestClient):
    payload = {
                "min": 18,
                "value": 30
            }

    response = client.post("/vignettes/", json=payload)
    assert response.status_code == 201

    response = client.delete("/vignettes/1")
    assert response.status_code == 204
