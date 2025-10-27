from dash import html, dcc

def create_home_layout():
    """
    Crée et retourne le layout de la page d'accueil
    """
    return html.Div([
        html.H2("Bienvenue sur le Dashboard Vélib"),
        html.P("Ce dashboard vous permet d'analyser les données des stations Vélib à Paris."),
        html.Div([
            html.Div([
                html.H3("Disponibilité"),
                html.P("Consultez la disponibilité en temps réel des Vélib."),
                dcc.Link("Voir les disponibilités →", href='/disponibilite')
            ], className='menu-card'),
            html.Div([
                html.H3("Statistiques"),
                html.P("Explorez les statistiques d'utilisation des Vélib."),
                dcc.Link("Voir les statistiques →", href='/statistiques')
            ], className='menu-card')
        ], className='menu-grid')
    ])
