from dash import html

def create_navbar(current_page="home"):
    if current_page == "home":
        # Aucune navigation par la navbar sur la page d'accueil
        return html.Nav([], style={"padding": "15px 30px","backgroundColor": "#1A2A40","color": "white","display": "flex","justifyContent": "space-between","alignItems": "center","boxShadow": "0 2px 5px rgba(0,0,0,0.1)"})
    else:
        # Sur une page de graphe : seulement retour à l'accueil
        return html.Nav([
            html.A("🏠 Home",href="/",style={"color": "white","textDecoration": "none","fontSize": "18px","fontWeight": "bold","transition": "0.3s"})
        ], style={"padding": "15px 30px","backgroundColor": "#0074D9","color": "white","display": "flex","justifyContent": "space-between","alignItems": "center","boxShadow": "0 2px 5px rgba(0,0,0,0.1)"})


