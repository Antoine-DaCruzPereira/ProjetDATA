from dash import html
from src.components.footer import create_footer
from src.utils.load_html import load_html_asset

layout = html.Div([
    html.H1("Carte de Position des Vélib en Région parisienne", style={"textAlign": "center"}),
    
    html.Div([
        
        load_html_asset("velib_occupation_map.html", height="600px"),
       
    ], style={"padding": "20px"}),

    create_footer()
])
