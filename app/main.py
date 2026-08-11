import json
from pathlib import Path
from typing import Any, Dict, List
from fastapi import FastAPI, HTTPException, status
from app.schemas.schemas import ItemCreate, ItemPatch, ItemUpdate

app = FastAPI(
    title="API MLOps",
    description="API REST pour la gestion et la consultation du catalogue d'outils MLOps (Projet M1 DSIA).",
    version="1.1.0",
)

DATA_FILE_PATH = Path(__file__).parent / "data.json"


# --- Fonctions Utilitaires ---

def load_data() -> Dict[str, List[Dict[str, Any]]]:
    """Charge les données depuis le fichier data.json."""
    if not DATA_FILE_PATH.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Le fichier de données data.json est introuvable.",
        )
    try:
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la lecture du fichier data.json.",
        )


def save_data(data: Dict[str, List[Dict[str, Any]]]) -> None:
    """Sauvegarde les données dans le fichier data.json."""
    try:
        with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la sauvegarde dans data.json : {str(e)}",
        )


# --- Endpoints GET ---

@app.get("/", status_code=status.HTTP_200_OK, summary="Message d'accueil")
def read_root() -> Dict[str, str]:
    """Route d'accueil. Retourne un message de bienvenue et la version de l'API."""
    return {
        "message": "Bienvenue sur l'API FastAPI MLOps",
        "version": "1.1.0",
    }


@app.get("/health", status_code=status.HTTP_200_OK, summary="État de santé de l'API")
def get_health() -> Dict[str, str]:
    """Route de vérification du fonctionnement de l'API."""
    return {"status": "ok"}


@app.get("/items", status_code=status.HTTP_200_OK, summary="Obtenir tous les éléments")
def get_items() -> Dict[str, List[Dict[str, Any]]]:
    """Retourne la liste complète de tous les éléments enregistrés dans le fichier JSON."""
    return load_data()


@app.get("/items/{item_id}", status_code=status.HTTP_200_OK, summary="Obtenir un élément par son identifiant")
def get_item_by_id(item_id: int) -> Dict[str, Any]:
    """Retourne un élément spécifique selon son identifiant unique."""
    data = load_data()
    items = data.get("items", [])
    for item in items:
        if item.get("id") == item_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Aucun enregistrement trouvé avec l'identifiant id={item_id}.",
    )


# --- Endpoint POST (Création) ---

@app.post("/items", status_code=status.HTTP_201_CREATED, summary="Ajouter un nouvel élément")
def create_item(item_input: ItemCreate) -> Dict[str, Any]:
    """Créer et ajouter un nouvel outil dans le catalogue JSON."""
    data = load_data()
    items = data.get("items", [])

    # Calcul automatique d'un nouvel identifiant unique
    new_id = max([item["id"] for item in items], default=0) + 1

    new_item = {"id": new_id, **item_input.model_dump()}
    items.append(new_item)
    data["items"] = items

    save_data(data)
    return new_item


# --- Endpoint PUT (Remplacement complet) ---

@app.put("/items/{item_id}", status_code=status.HTTP_200_OK, summary="Remplacer complètement un élément")
def update_item_full(item_id: int, item_input: ItemUpdate) -> Dict[str, Any]:
    """Remplacer l'intégralité d'un élément existant par son identifiant."""
    data = load_data()
    items = data.get("items", [])

    for idx, item in enumerate(items):
        if item.get("id") == item_id:
            updated_item = {"id": item_id, **item_input.model_dump()}
            items[idx] = updated_item
            data["items"] = items
            save_data(data)
            return updated_item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Aucun enregistrement trouvé avec l'identifiant id={item_id}.",
    )


# --- Endpoint PATCH (Modification partielle) ---

@app.patch("/items/{item_id}", status_code=status.HTTP_200_OK, summary="Modifier partiellement un élément")
def update_item_partial(item_id: int, item_input: ItemPatch) -> Dict[str, Any]:
    """Modifier uniquement les champs spécifiés d'un élément existant."""
    data = load_data()
    items = data.get("items", [])

    for idx, item in enumerate(items):
        if item.get("id") == item_id:
            update_data = item_input.model_dump(exclude_unset=True)
            if not update_data:
                return item

            items[idx].update(update_data)
            data["items"] = items
            save_data(data)
            return items[idx]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Aucun enregistrement trouvé avec l'identifiant id={item_id}.",
    )


# --- Endpoint DELETE (Suppression) ---

@app.delete("/items/{item_id}", status_code=status.HTTP_200_OK, summary="Supprimer un élément")
def delete_item(item_id: int) -> Dict[str, Any]:
    """Supprimer définitivement un élément du catalogue JSON par son identifiant."""
    data = load_data()
    items = data.get("items", [])

    for idx, item in enumerate(items):
        if item.get("id") == item_id:
            deleted_item = items.pop(idx)
            data["items"] = items
            save_data(data)
            return {"message": f"Élément id={item_id} supprimé avec succès.", "deleted_item": deleted_item}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Aucun enregistrement trouvé avec l'identifiant id={item_id}.",
    )
