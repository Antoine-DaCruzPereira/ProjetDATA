from dash import html
from src.components.footer import create_footer

layout = html.Div([
    html.H1("Dashboard sur les vélib en Région parisienne", style={"textAlign": "center", "margin-bottom": "40px"}),

    html.Div([
        html.A(
            html.Button("Carte Position", style={"padding": "15px 25px","margin": "10px","fontSize": "18px","borderRadius": "12px","border": "none","backgroundColor": "#0074D9","color": "white","cursor": "pointer","transition": "0.3s",}),
            href="/carte-positions"
        ),
        html.A(
            html.Button("Histogramme des vélib disponnibles", style={"padding": "15px 25px","margin": "10px","fontSize": "18px","borderRadius": "12px","border": "none","backgroundColor": "#0074D9","color": "white","cursor": "pointer","transition": "0.3s",}),
            href="/velos-disponibles"
        ),
        html.A(
            html.Button("Histogramme des vélib électriques", style={"padding": "15px 25px","margin": "10px","fontSize": "18px","borderRadius": "12px","border": "none","backgroundColor": "#0074D9","color": "white","cursor": "pointer","transition": "0.3s",}),
            href="/velos-electriques"
        ),
        html.A(
            html.Button("Histogramme des vélib mécaniques", style={"padding": "15px 25px","margin": "10px","fontSize": "18px","borderRadius": "12px","border": "none","backgroundColor": "#0074D9","color": "white","cursor": "pointer","transition": "0.3s",}),
            href="/velos-mecaniques"
        )
        
    ], style={"display": "flex", "justify-content": "center"}),

    html.Div([
        html.A(
            html.Button("Histogramme de la capacité des stations", style={"padding": "15px 25px","margin": "10px","fontSize": "18px","borderRadius": "12px","border": "none","backgroundColor": "#0074D9","color": "white","cursor": "pointer","transition": "0.3s",}),
            href="/capacite-station"
        ),
        html.A(
            html.Button("Histogramme du taux d'occupation moyen", style={"padding": "15px 25px","margin": "10px","fontSize": "18px","borderRadius": "12px","border": "none","backgroundColor": "#0074D9","color": "white","cursor": "pointer","transition": "0.3s",}),
            href="/taux-occupation"
        ),
        html.A(
            html.Button("Station non fonctionnelles", style={"padding": "15px 25px","margin": "10px","fontSize": "18px","borderRadius": "12px","border": "none","backgroundColor": "#0074D9","color": "white","cursor": "pointer","transition": "0.3s",}),
            href="/stations-non-fonctionnelles"
        ),
        html.A(
            html.Button("Capacité vs Vélos Disponible", style={"padding": "15px 25px","margin": "10px","fontSize": "18px","borderRadius": "12px","border": "none","backgroundColor": "#0074D9","color": "white","cursor": "pointer","transition": "0.3s",}),
            href="/capacite-vs-disponibles"
        ),
    ], style={"display": "flex", "flexGrow": 1, "justify-content": "center"}),

    create_footer()
], style={"backgroundColor": "#f5f7fa","color": "#333","fontFamily": "Arial, sans-serif","minHeight": "100vh","display": "flex","flexDirection": "column","alignItems": "center",})


