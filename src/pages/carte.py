from dash import html

layout = html.Div([
    html.H1("Carte"),
    html.Iframe(
        srcDoc=open("./assets/velib_occupation_map.html", "r").read(),
        style={"width": "100%", "height": "600px", "border": "none"}
    )
])