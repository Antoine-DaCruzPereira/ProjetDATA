from dash import html
from src.components.footer import create_footer

layout = html.Div([
    html.H1("Carte", style={"textAlign": "center"}),
    
    html.Div([
        html.Iframe(
            srcDoc=open("./assets/velib_occupation_map.html", "r").read(),
            style={"width": "100%", "height": "600px", "border": "none"}
        )
    ], style={"padding": "20px"}),

    create_footer()
])