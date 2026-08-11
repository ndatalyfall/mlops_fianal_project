from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    nom: str = Field(..., description="Nom de l'outil MLOps")
    categorie: str = Field(..., description="Catégorie de l'outil MLOps")
    prix: float = Field(..., ge=0, description="Prix de l'outil en euros")
    description: Optional[str] = Field(None, description="Description détaillée de l'outil")
    statut: Optional[str] = Field("Production", description="Statut de maturité (ex: Production, Beta, Test)")


class ItemPatch(BaseModel):
    """Schéma pour la modification partielle d'un élément."""
    nom: Optional[str] = Field(None, description="Nom de l'outil MLOps")
    categorie: Optional[str] = Field(None, description="Catégorie de l'outil MLOps")
    prix: Optional[float] = Field(None, ge=0, description="Prix de l'outil en euros")
    description: Optional[str] = Field(None, description="Description détaillée de l'outil")
    statut: Optional[str] = Field(None, description="Statut de maturité (ex: Production, Beta, Test)")


class ItemCreate(ItemBase):
    """Schéma pour la création d'un nouvel élément."""
    pass


class ItemUpdate(ItemBase):
    """Schéma pour la mise à jour complète d'un élément."""
    pass