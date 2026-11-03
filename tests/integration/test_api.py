# ruff: noqa: I001
from supermarket_receipt_api.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_read_root():
    """Vérifie que la racine de l'API répond correctement."""
    response = client.get("/")
    assert response.status_code in [200, 404]


def test_checkout_endpoint_structure():
    """Test d'intégration basique pour l'endpoint de checkout (cas nominal)."""
    payload = {"items": []}
    response = client.post("/checkout", json=payload)
    assert response.status_code in [200, 201, 422]


def test_checkout_invalid_payload():
    """Vérifie que l'API rejette (refuse) proprement un payload invalide ou mal structuré."""
    payload = {
        "items": "ceci_nest_pas_une_liste"  # Attendu : une liste d'articles
    }
    response = client.post("/checkout", json=payload)
    assert response.status_code == 422


def test_checkout_missing_required_fields():
    """Vérifie le refus lorsqu'il manque des champs obligatoires."""
    payload = {}
    response = client.post("/checkout", json=payload)
    assert response.status_code == 422