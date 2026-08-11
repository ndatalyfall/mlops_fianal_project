from fastapi.testclient import TestClient
from ../app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Bienvenue sur l'API FastAPI MLOps"
    assert "version" in data


def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 10


def test_get_item_by_id_success():
    response = client.get("/items/1")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert "nom" in item


def test_get_item_by_id_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_crud_lifecycle():
    # 1. POST (Création)
    new_item_payload = {
        "nom": "Outil de Test",
        "categorie": "Test et Validation",
        "prix": 15.5,
        "description": "Outil de test automatique des pipelines",
        "statut": "Beta"
    }
    post_res = client.post("/items", json=new_item_payload)
    assert post_res.status_code == 201
    created_item = post_res.json()
    created_id = created_item["id"]
    assert created_item["nom"] == "Outil de Test"

    # 2. GET par ID (Vérification)
    get_res = client.get(f"/items/{created_id}")
    assert get_res.status_code == 200
    assert get_res.json()["categorie"] == "Test et Validation"

    # 3. PUT (Remplacement complet)
    put_payload = {
        "nom": "Outil de Test Mis à Jour",
        "categorie": "Suite de Test",
        "prix": 20.0,
        "description": "Description mise à jour en français",
        "statut": "Production"
    }
    put_res = client.put(f"/items/{created_id}", json=put_payload)
    assert put_res.status_code == 200
    assert put_res.json()["nom"] == "Outil de Test Mis à Jour"
    assert put_res.json()["prix"] == 20.0

    # 4. PATCH (Modification partielle)
    patch_payload = {"prix": 25.99}
    patch_res = client.patch(f"/items/{created_id}", json=patch_payload)
    assert patch_res.status_code == 200
    assert patch_res.json()["prix"] == 25.99
    assert patch_res.json()["nom"] == "Outil de Test Mis à Jour"

    # 5. DELETE (Suppression)
    delete_res = client.delete(f"/items/{created_id}")
    assert delete_res.status_code == 200

    # 6. Vérification du retour 404 après suppression
    verify_delete = client.get(f"/items/{created_id}")
    assert verify_delete.status_code == 404
