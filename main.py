# main.py
from dash import Dash, html, dcc, Input, Output
import dash

from config import chemin_home,chemin_carte_position,chemin_velos_disponibles,chemin_velos_electriques,chemin_velos_mecaniques,chemin_capacite_station,chemin_taux_occupation_moyen,chemin_station_non_fonctionnelles,chemin_capacite_vs_disponibles


from src.utils.get_data import download_velib_csv
from src.utils.CleanData_CSV import clean_velib_csv
from src.utils.Create_DataBase import create_velib_database
from src.utils.Histogramme import create_histograms 
from src.utils.Map import Map_Int
from src.pages import carte_position, home
from src.pages import velos_disponibles
from src.pages import velos_electriques
from src.pages import velos_mecaniques
from src.pages import capacite_station
from src.pages import taux_occupation_moyen
from src.pages import station_non_fonctionnelles
from src.pages import capacite_vs_velos_disponibles
from src.components.navbar import create_navbar

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

    print("\n=== 4. Création des histogrammes ===")
    print("----------------------------------------")
    create_histograms()

    print("\n=== 5. Création de la Map ===")
    print("----------------------------------------")
    Map_Int()

    print("\n=== Pipeline de données terminé avec succès ! ===\n")

app = Dash(__name__, use_pages=False)
app.title = "Paris_velib_Dashboard"

# Layout principal avec navigation
app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="navbar-container"),
    html.Div(id="page-content")
])

# Callback pour gérer la navigation
@app.callback(
    Output("navbar-container", "children"),
    Input("url", "pathname")
)
def update_navbar(pathname):
    if pathname == "/":
        return create_navbar("home")
    else:
        return create_navbar("other")

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == chemin_home:
        return home.layout
    elif pathname == chemin_carte_position:
        return carte_position.layout
    elif pathname == chemin_velos_disponibles:
        return velos_disponibles.layout
    elif pathname == chemin_velos_electriques:
        return velos_electriques.layout
    elif pathname == chemin_velos_mecaniques:
        return velos_mecaniques.layout
    elif pathname == chemin_capacite_station:
        return capacite_station.layout
    elif pathname == chemin_taux_occupation_moyen:
        return taux_occupation_moyen.layout
    elif pathname == chemin_station_non_fonctionnelles:
        return station_non_fonctionnelles.layout
    elif pathname == chemin_capacite_vs_disponibles:
        return capacite_vs_velos_disponibles.layout
    else:
        return html.Div([html.H1("Page non trouvée")])

if __name__ == "__main__":
    # Initialisation des données
    init_data()
    app.run(debug=True)
