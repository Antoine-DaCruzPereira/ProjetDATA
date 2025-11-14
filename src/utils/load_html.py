from dash import html
import os

def load_html_asset(filename: str, width="100%", height="600px") -> html.Iframe:

    asset_path = os.path.join("assets", filename)
    
    if not os.path.exists(asset_path):
        # Si le fichier n'existe pas, on renvoie une iframe avec un message
        content = f"<h3 style='color:red;text-align:center;'>Le fichier {filename} n'a pas encore été généré.</h3>"
        return html.Iframe(
            srcDoc=content,
            style={"width": "100%", "height": "600px", "border": "none"}
        )
    
    # Si le fichier existe, on le sert via src (Dash sert automatiquement le dossier assets)
    return html.Iframe(
        src=f"/assets/{filename}",
        style={"width": "100%", "height": "600px", "border": "none"}
    )
