from dash import html

def create_footer():
    return html.Footer(
        html.P("© 2025 Projet Data | DCP Antoine & Soen", style={"textAlign": "center", "margin": "20px 0"})
    )
