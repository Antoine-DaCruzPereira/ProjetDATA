from dash import html
from src.components.footer import create_footer

layout = html.Div([
    html.H1("Histogramme des velos mécaniques en Région parisienne", style={"textAlign": "center"}),
    
    html.Div([
        html.Iframe(
            srcDoc=open("./assets/hist_velos_mecaniques.html", "r").read(),
            style={"width": "100%", "height": "600px", "border": "none"}
        )
    ], style={"padding": "20px"}),

    create_footer()
])