"""
Fichier de configuration du projet.
"""

# Configuration des chemins
DATA_RAW_FILENAME = 'rawdata.csv'
DATA_CLEANED_FILENAME = 'cleaneddata.csv'

# Configuration du dashboard
REFRESH_INTERVAL = 5 * 60  # 5 minutes en secondes
DEFAULT_MAP_CENTER = {
    'lat': 48.8566,  # Paris
    'lon': 2.3522
}
DEFAULT_MAP_ZOOM = 11

# Configuration des couleurs
COLORS = {
    'Hors service': '#ff0000',
    'Presque vide': '#ffa500',
    'Normal': '#00ff00',
    'Presque plein': '#0000ff'
}

# Configuration de l'application
APP_TITLE = "Dashboard Vélib en Temps Réel"
APP_DESCRIPTION = """
Dashboard permettant de visualiser en temps réel la disponibilité 
des stations Vélib dans Paris et sa banlieue.
"""
