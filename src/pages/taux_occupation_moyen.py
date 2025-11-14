from dash import html
from src.components.footer import create_footer
from src.utils.load_html import load_html_asset


layout = html.Div([
    html.H1("Histogramme du taux d'occupation moyen en Région parisienne", style={"textAlign": "center"}),
    
    html.Div([
        
        load_html_asset("hist_taux_occupation_moyen.html", height="500px"),

    ], style={"padding": "20px"}),

    create_footer()
])