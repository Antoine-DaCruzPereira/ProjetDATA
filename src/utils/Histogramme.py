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

    output_dir = output_dir or os.path.join(project_root, "assets")
    os.makedirs(output_dir, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        stations_df = pd.read_sql_query(
            """
            SELECT identifiant_station, nom_station, capacite_station
            FROM stations
            WHERE capacite_station IS NOT NULL
            """,
            conn,
        )
        disponibilites_df = pd.read_sql_query(
            """
            SELECT
                identifiant_station,
                velos_disponibles,
                velos_mecaniques,
                velos_electriques,
                bornettes_libres
            FROM disponibilites
            """,
            conn,
        )
        etats_df = pd.read_sql_query(
            """
            SELECT identifiant_station, station_en_fonctionnement
            FROM etats
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
    etats_df["station_en_fonctionnement"] = pd.to_numeric(
        etats_df["station_en_fonctionnement"], errors="coerce"
    )

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

    disponibilites_cap_df = disponibilites_df.dropna(subset=["velos_disponibles"]).merge(
        stations_df, on="identifiant_station", how="inner"
    )
    disponibilites_cap_df = disponibilites_cap_df[
        disponibilites_cap_df["capacite_station"] > 0
    ]

    if not disponibilites_cap_df.empty:
        scatter_fig = px.scatter(
            disponibilites_cap_df,
            x="capacite_station",
            y="velos_disponibles",
            opacity=0.7,
            title="Capacité vs vélos disponibles",
            labels={
                "capacite_station": "Capacité de la station",
                "velos_disponibles": "Vélos disponibles",
            },
        )
        scatter_path = os.path.join(
            output_dir, "scatter_capacite_vs_velos_disponibles.html"
        )
        scatter_fig.write_html(scatter_path, include_plotlyjs="cdn")
        print(f"Graphique sauvegardé : {scatter_path}")

        occupation_df = disponibilites_cap_df.copy()
        occupation_df["taux_occupation"] = (
            occupation_df["velos_disponibles"] / occupation_df["capacite_station"]
        )
        occupation_df = occupation_df.dropna(subset=["taux_occupation"])

        if not occupation_df.empty:
            occupation_mean = (
                occupation_df.groupby(
                    ["identifiant_station", "nom_station"], as_index=False
                )["taux_occupation"]
                .mean()
                .assign(taux_occupation_pct=lambda df: df["taux_occupation"] * 100)
            )
            occupation_fig = px.histogram(
                occupation_mean,
                x="taux_occupation_pct",
                nbins=40,
                title="Distribution du taux d’occupation moyen",
                labels={"taux_occupation_pct": "Taux d’occupation moyen (%)"},
                template="plotly_white",
            )
            occupation_fig.update_layout(
                bargap=0.05,
                yaxis_title="Nombre de stations",
            )
            occupation_path = os.path.join(
                output_dir, "hist_taux_occupation_moyen.html"
            )
            occupation_fig.write_html(occupation_path, include_plotlyjs="cdn")
            print(f"Histogramme sauvegardé : {occupation_path}")

    status_counts = (
        etats_df.dropna(subset=["station_en_fonctionnement"])
        .assign(
            statut=lambda df: df["station_en_fonctionnement"].map(
                {1: "Stations en fonctionnement", 0: "Stations non fonctionnelles"}
            )
        )
        .dropna(subset=["statut"])
        .groupby("statut")
        .size()
        .reset_index(name="nombre")
    )

    if not status_counts.empty:
        status_fig = px.bar(
            status_counts,
            x="statut",
            y="nombre",
            title="Répartition des stations en fonctionnement",
            labels={"statut": "Statut", "nombre": "Nombre d’observations"},
            text_auto=True,
        )
        status_path = os.path.join(
            output_dir, "bar_stations_non_fonctionnelles.html"
        )
        status_fig.write_html(status_path, include_plotlyjs="cdn")
        print(f"Graphique sauvegardé : {status_path}")


if __name__ == "__main__":
    create_histograms()
