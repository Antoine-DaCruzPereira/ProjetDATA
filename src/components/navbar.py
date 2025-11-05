from dash import html

def create_navbar(current_page="home"):
    if current_page == "home":
        # Aucune navigation par la navbar sur la page d'accueil
        return html.Nav([], style={"padding": "20px", "background-color": "#333", "color": "#fff"})
    else:
        # Sur une page de graphe : seulement retour à l'accueil
        return html.Nav([
            html.A("Home", href="/", style={"color": "blue", "text-decoration": "underline", "font-size": "20px"})
        ], style={"padding": "10px", "background-color": "#333", "color": "#fff"})
