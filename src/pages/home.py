from dash import html
from src.components.footer import create_footer

layout = html.Div([
    html.H1("Accueil", style={"textAlign": "center", "margin-bottom": "40px"}),

    html.Div([
        html.A(
            html.Button("Voir la Carte", style={"padding": "20px", "margin": "10px", "font-size": "18px"}),
            href="/carte"
        ),
    ], style={"display": "flex", "justify-content": "center"}),

    create_footer()
])