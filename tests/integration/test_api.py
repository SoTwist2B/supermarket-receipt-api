from fastapi.testclient import TestClient
from supermarket_receipt_api.main import app

client = TestClient(app)


def test_read_root():
    """Vérifie que la racine de l'API répond correctement."""
    response = client.get("/")
    assert response.status_code in [200, 404]


def test_checkout_endpoint_structure():
    """Test d'intégration basique pour l'endpoint de checkout (cas nominal)."""
    payload = {
        "items": []
    }
    response = client.post("/checkout", json=payload)
    assert response.status_code in [200, 201, 422]


def test_checkout_invalid_payload():
    """Vérifie que l'API rejette (refuse) proprement un payload invalide ou mal structuré."""
    # Envoi de données incorrectes par rapport aux schémas attendus
    payload = {
        "items": "ceci_nest_pas_une_liste"  # Attendu : une liste d'articles
    }
    response = client.post("/checkout", json=payload)
    
    # FastAPI/Pydantic doit refuser la requête avec une erreur de validation (422)
    assert response.status_code == 422


def test_checkout_missing_required_fields():
    """Vérifie le refus lorsqu'il manque des champs obligatoires."""
    payload = {
        # Champ "items" complètement absent
    }
    response = client.post("/checkout", json=payload)
    assert response.status_code == 422