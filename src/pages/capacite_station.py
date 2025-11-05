from dash import html
from src.components.footer import create_footer

layout = html.Div([
    html.H1("Histogramme sur la capacité des stations en Région parisienne", style={"textAlign": "center"}),
    
    html.Div([
        html.Iframe(
            srcDoc=open("./assets/hist_capacite_station.html", "r").read(),
            style={"width": "100%", "height": "600px", "border": "none"}
        )
    ], style={"padding": "20px"}),

    create_footer()
])