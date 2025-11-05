from dash import html
from src.components.footer import create_footer

layout = html.Div([
    html.H1("Dashboard sur les vlib en Région parisienne", style={"textAlign": "center", "margin-bottom": "40px"}),

    html.Div([
        html.A(
            html.Button("Carte Position", style={"padding": "20px", "margin": "10px", "font-size": "18px"}),
            href="/carte-positions"
        ),
        html.A(
            html.Button("Histogramme des vlib disponnibles", style={"padding": "20px", "margin": "10px", "font-size": "18px"}),
            href="/velos-disponibles"
        ),
        html.A(
            html.Button("Histogramme des vlib électriques", style={"padding": "20px", "margin": "10px", "font-size": "18px"}),
            href="/velos-electriques"
        ),
        html.A(
            html.Button("Histogramme des vlib mécaniques", style={"padding": "20px", "margin": "10px", "font-size": "18px"}),
            href="/velos-mecaniques"
        )
        
    ], style={"display": "flex", "justify-content": "center"}),

    html.Div([
        html.A(
            html.Button("Histogramme de la capacité des stations", style={"padding": "20px", "margin": "10px", "font-size": "18px"}),
            href="/capacite-station"
        ),
        html.A(
            html.Button("Histogramme du taux d'occupation moyen", style={"padding": "20px", "margin": "10px", "font-size": "18px"}),
            href="/taux-occupation"
        ),
        html.A(
            html.Button("Station non fonctionnelles", style={"padding": "20px", "margin": "10px", "font-size": "18px"}),
            href="/stations-non-fonctionnelles"
        ),
        html.A(
            html.Button("Capacité vs Vélos Disponible", style={"padding": "20px", "margin": "10px", "font-size": "18px"}),
            href="/capacite-vs-disponibles"
        ),
    ], style={"display": "flex", "justify-content": "center"}),

    create_footer()
])


