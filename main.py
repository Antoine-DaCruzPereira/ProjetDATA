# main.py
from dash import Dash, html, dcc, Input, Output
import dash
from src.pages import home, carte
from src.components.navbar import create_navbar
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

app = Dash(__name__, use_pages=False)
app.title = "A Determiner plus tard"

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
        return create_navbar("graph")

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
