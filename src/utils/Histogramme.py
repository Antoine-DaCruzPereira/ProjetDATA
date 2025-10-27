import os
import sqlite3
from typing import Optional
import pandas as pd
import plotly.express as px


def create_histograms(output_dir: Optional[str] = None) -> None:
    """
    Génère quelques histogrammes descriptifs à partir des données de la base SQLite
    et enregistre les graphiques au format HTML interactif.

    Args:
        output_dir: Dossier cible pour les fichiers HTML. S'il est omis, les
            histogrammes sont stockés dans ``images/histograms`` à la racine.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    db_path = os.path.join(project_root, "data", "database", "velib.db")

    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"Base de données introuvable : {db_path}. "
            "Exécutez d'abord le pipeline (main.py) pour la générer."
        )

    output_dir = output_dir or os.path.join(project_root, "images", "histograms")
    os.makedirs(output_dir, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        stations_df = pd.read_sql_query(
            """
            SELECT capacite_station
            FROM stations
            WHERE capacite_station IS NOT NULL
            """,
            conn,
        )
        disponibilites_df = pd.read_sql_query(
            """
            SELECT
                velos_disponibles,
                velos_mecaniques,
                velos_electriques,
                bornettes_libres
            FROM disponibilites
            """,
            conn,
        )

    stations_df["capacite_station"] = pd.to_numeric(
        stations_df["capacite_station"], errors="coerce"
    )
    stations_df = stations_df.dropna(subset=["capacite_station"])

    for column in [
        "velos_disponibles",
        "velos_mecaniques",
        "velos_electriques",
        "bornettes_libres",
    ]:
        disponibilites_df[column] = pd.to_numeric(
            disponibilites_df[column], errors="coerce"
        )
    disponibilites_df.dropna(how="all", inplace=True)

    hist_specs = [
        {
            "df": stations_df,
            "column": "capacite_station",
            "title": "Distribution des capacités des stations",
            "file": "hist_capacite_station.html",
            "x_title": "Capacité de la station (nombre de bornettes)",
        },
        {
            "df": disponibilites_df,
            "column": "velos_disponibles",
            "title": "Distribution du total de vélos disponibles",
            "file": "hist_velos_disponibles.html",
            "x_title": "Nombre de vélos disponibles",
        },
        {
            "df": disponibilites_df,
            "column": "velos_electriques",
            "title": "Distribution des vélos électriques disponibles",
            "file": "hist_velos_electriques.html",
            "x_title": "Nombre de vélos électriques disponibles",
        },
        {
            "df": disponibilites_df,
            "column": "velos_mecaniques",
            "title": "Distribution des vélos mécaniques disponibles",
            "file": "hist_velos_mecaniques.html",
            "x_title": "Nombre de vélos mécaniques disponibles",
        },
    ]

    for spec in hist_specs:
        clean_df = spec["df"].dropna(subset=[spec["column"]])
        if clean_df.empty:
            print(f"Aucune donnée disponible pour {spec['column']}, histogramme ignoré.")
            continue

        fig = px.histogram(
            clean_df,
            x=spec["column"],
            nbins=40,
            title=spec["title"],
            opacity=0.85,
            template="plotly_white",
        )
        fig.update_layout(
            bargap=0.05,
            xaxis_title=spec["x_title"],
            yaxis_title="Nombre d'observations",
        )
        target_path = os.path.join(output_dir, spec["file"])
        fig.write_html(target_path, include_plotlyjs="cdn")
        print(f"Histogramme sauvegardé : {target_path}")


if __name__ == "__main__":
    create_histograms()
