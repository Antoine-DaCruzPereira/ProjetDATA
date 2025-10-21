"""
Point d'entrée principal du dashboard Vélib.
"""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components.header import create_header
from src.components.footer import create_footer
from src.components.navbar import create_navbar
from src.pages.home import create_home_page
from src.utils.get_data import fetch_velib_data
from src.utils.clean_data import clean_velib_data
from config import REFRESH_INTERVAL

def init_dashboard():
    """Initialise l'application dashboard."""
    # Initialisation de l'application avec Bootstrap pour un design responsive
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
        ]
    )

    # Layout principal de l'application
    app.layout = html.Div([
        # Store pour l'URL
        dcc.Location(id='url', refresh=False),
        
        # Composants principaux
        create_header(),
        create_navbar(),
        
        # Contenu principal qui changera selon la route
        html.Div(id='page-content', className='container-fluid mt-3'),
        
        create_footer(),
        
        # Intervalle pour le rafraîchissement automatique des données
        dcc.Interval(
            id='refresh-interval',
            interval=REFRESH_INTERVAL * 1000,  # Conversion en millisecondes
            n_intervals=0
        )
    ])

    # Callback pour la gestion des routes
    @app.callback(
        dash.Output('page-content', 'children'),
        [dash.Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/' or pathname is None:
            return create_home_page()
        # Ajouter d'autres routes ici au besoin
        return html.Div([
            html.H1("404 - Page non trouvée"),
            html.P(f"La page {pathname} n'existe pas.")
        ])

    # Callback pour le rafraîchissement automatique des données
    @app.callback(
        dash.Output('refresh-interval', 'disabled'),
        [dash.Input('refresh-interval', 'n_intervals')]
    )
    def refresh_data(n):
        if n:  # Ne pas exécuter au premier chargement
            try:
                raw_file = fetch_velib_data(force_download=True)
                if raw_file:
                    clean_velib_data(raw_file)
            except Exception as e:
                print(f"Erreur lors du rafraîchissement des données : {e}")
        return False  # Garder l'intervalle actif

    return app

def main():
    """Fonction principale."""
    # Premier téléchargement et nettoyage des données
    try:
        print("Initialisation des données...")
        raw_file = fetch_velib_data()
        if raw_file:
            clean_velib_data(raw_file)
    except Exception as e:
        print(f"Erreur lors de l'initialisation des données : {e}")
        print("Le dashboard démarrera quand même, mais sans données initiales.")

    # Initialisation et lancement du dashboard
    app = init_dashboard()
    print("Démarrage du dashboard...")
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    main()
