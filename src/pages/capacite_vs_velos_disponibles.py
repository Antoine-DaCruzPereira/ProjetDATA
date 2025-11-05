from dash import html
from src.components.footer import create_footer

layout = html.Div([
    html.H1("", style={"textAlign": "center"}),
    
    html.Div([
        html.Iframe(
            srcDoc=open("./assets/scatter_capacite_vs_velos_disponibles.html", "r").read(),
            style={"width": "100%", "height": "600px", "border": "none"}
        )
    ], style={"padding": "20px"}),

    create_footer()
])