# Configuration du dashboard
VELIB_API_URL = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel"
DATA_RAW_PATH = "data/raw/velib_disponibilite.csv"
DATA_CLEAN_PATH = "data/cleaned/velib_disponibilite_clean.csv"

# Configuration de l'interface
APP_TITLE = "Dashboard Vélib"
DEBUG_MODE = True

# Configuration des styles
COLORS = {
    'background': '#ffffff',
    'text': '#2c3e50',
    'primary': '#3498db',
    'secondary': '#2ecc71',
    'danger': '#e74c3c'
}

# Configuration des intervalles de mise à jour
UPDATE_INTERVAL = 300  # 5 minutes en secondes
