from pydantic import BaseModel, Field, field_validator
from typing import Optional, Tuple
from datetime import datetime

class VelibStation(BaseModel):
    identifiant_station: str = Field(..., alias="Identifiant station")
    nom_station: str = Field(..., alias="Nom station")
    station_en_fonctionnement: bool = Field(..., alias="Station en fonctionnement")
    capacite_station: int = Field(..., alias="Capacité de la station", ge=0)
    bornettes_libres: int = Field(..., alias="Nombre bornettes libres", ge=0)
    velos_disponibles: int = Field(..., alias="Nombre total vélos disponibles", ge=0)
    velos_mecaniques: int = Field(..., alias="Vélos mécaniques disponibles", ge=0)
    velos_electriques: int = Field(..., alias="Vélos électriques disponibles", ge=0)
    borne_paiement: bool = Field(..., alias="Borne de paiement disponible")
    retour_possible: bool = Field(..., alias="Retour vélib possible")
    actualisation_donnee: datetime = Field(..., alias="Actualisation de la donnée")
    coordonnees_geographiques: Tuple[float, float] = Field(..., alias="Coordonnées géographiques")
    commune: Optional[str] = Field(None, alias="Nom communes équipées")
    code_insee: Optional[str] = Field(None, alias="Code INSEE communes équipées")

    # Convertir certains champs
    @field_validator("station_en_fonctionnement", "borne_paiement", "retour_possible", mode="before")
    def to_bool(cls, v):
        if isinstance(v, str):
            v = v.strip().lower()
            return v in ["true", "1", "oui", "yes", "y"]
        return bool(v)

    @field_validator("coordonnees_geographiques",mode="before")
    def parse_coords(cls, v):
        if isinstance(v, str):
            parts = v.replace("(", "").replace(")", "").split(",")
            try:
                return (float(parts[0]), float(parts[1]))
            except Exception:
                raise ValueError("Coordonnées invalides")
        return v

    @field_validator("actualisation_donnee", mode="before")
    def parse_datetime(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError("Format de date invalide")
        return v
    
if __name__ == "__main__":
    data = {
        "Identifiant station": "12345",
        "Nom station": "République",
        "Station en fonctionnement": "Oui",
        "Capacité de la station": 25,
        "Nombre bornettes libres": 10,
        "Nombre total vélos disponibles": 15,
        "Vélos mécaniques disponibles": 5,
        "Vélos électriques disponibles": 10,
        "Borne de paiement disponible": "Non",
        "Retour vélib possible": "1",
        "Actualisation de la donnée": "2025-10-21T19:42:00",
        "Coordonnées géographiques": "(48.867, 2.362)",
        "Nom communes équipées": "Paris",
        "Code INSEE communes équipées": "75011",
        "station_opening_hours": None
    }

    station = VelibStation(**data)
    print(station)