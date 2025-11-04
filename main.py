# main.py
import os
from dash import Dash, html, dcc, Input, Output
import dash
from src.pages import home, carte
from src.utils.Download_CSV import download_velib_csv
from src.utils.CleanData_CSV import clean_velib_csv
from src.utils.Create_DataBase import create_velib_database
from src.utils.Histogramme import create_histograms 

def init_data():
    """Initialise les données nécessaires au dashboard"""
    print("\n=== 1. Téléchargement du CSV Vélib ===")
    print("--------------------------------------")
    download_velib_csv()

    print("\n=== 2. Nettoyage et validation du CSV ===")
    print("----------------------------------------")
    clean_velib_csv()

    print("\n=== 3. Création de la base de données ===")
    print("----------------------------------------")
    create_velib_database()

    print("\n=== Pipeline de données terminé avec succès ! ===\n")

app = Dash(__name__, use_pages=False)  # Pas besoin d'auto-pages ici
app.title = "Dashboard Multi-Page"

# Layout principal avec navigation
app.layout = html.Div([
    html.Nav([
        html.A("Accueil", href="/", style={"margin-right": "20px"}),
        html.A("Carte", href="/carte", style={"margin-right": "20px"}),
    ]),
    html.Hr(),
    dcc.Location(id="url"),
    html.Div(id="page-content")
])

# Callback pour gérer la navigation
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/carte":
        return carte.layout
    else:
        return html.Div([html.H1("Page non trouvée")])


if __name__ == "__main__":
    # Initialisation des données
    init_data()
    app.run(debug=True)
