from dash import html

def create_navbar(current_page="home"):
    if current_page == "home":
        # Sur la home page : navigation complète
        return html.Nav([], style={"padding": "10px", "background-color": "#333", "color": "#fff"})
    else:
        # Sur une page de graphe : seulement retour à l'accueil
        return html.Nav([
            html.A("Home", href="/")
        ], style={"padding": "10px", "background-color": "#333", "color": "#fff"})
