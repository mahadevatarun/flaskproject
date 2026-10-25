from pathlib import Path

import pytest

from app import create_app


@pytest.fixture
def client():
    # a fresh app for every test, so tests never affect each other
    return create_app().test_client()


def add(client, name="Pen", price=10):
    return client.post("/products", json={"name": name, "price": price})


def test_health_reports_version(client):
    body = client.get("/health").get_json()
    expected = (Path(__file__).parent / "VERSION").read_text().strip()
    assert body["status"] == "ok"
    assert body["version"] == expected


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"MiniShop" in response.data


def test_list_starts_empty(client):
    assert client.get("/products").get_json() == []


def test_add_and_list(client):
    response = add(client)
    assert response.status_code == 201
    assert response.get_json()["id"] == 1
    assert len(client.get("/products").get_json()) == 1


def test_add_requires_name_and_price(client):
    assert client.post("/products", json={"name": "Pen"}).status_code == 400
    assert client.post("/products", json={"price": 5}).status_code == 400


def test_add_rejects_bad_values(client):
    assert add(client, name="  ", price=5).status_code == 400
    assert add(client, name="Pen", price=-1).status_code == 400
    assert add(client, name="Pen", price="free").status_code == 400


def test_update_price(client):
    add(client)
    response = client.put("/products/1", json={"price": 20})
    assert response.status_code == 200
    assert response.get_json()["price"] == 20


def test_update_rejects_bad_price(client):
    add(client)
    assert client.put("/products/1", json={"price": -5}).status_code == 400


def test_update_missing_product(client):
    assert client.put("/products/99", json={"price": 1}).status_code == 404


def test_delete(client):
    add(client)
    assert client.delete("/products/1").status_code == 204
    assert client.get("/products").get_json() == []


def test_delete_missing_product(client):
    assert client.delete("/products/99").status_code == 404
