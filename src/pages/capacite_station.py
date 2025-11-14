from dash import html
from src.components.footer import create_footer
from src.utils.load_html import load_html_asset


layout = html.Div([
    html.H1("Histogramme sur la capacité des stations en Région parisienne", style={"textAlign": "center"}),
    
    html.Div([
        
        load_html_asset("hist_capacite_station.html", height="500px"),


    ], style={"padding": "20px"}),

    create_footer()
])