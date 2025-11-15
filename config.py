#Configuration des chemin utilisé dans le projet
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
rawdata_path = os.path.join(project_root, "data", "rawdata", "velib_disponibilite.csv")
cleandata_dir = os.path.join(project_root, "data", "cleandata")
os.makedirs(cleandata_dir, exist_ok=True)
cleandata_path = os.path.join(cleandata_dir, "velib_disponibilite_clean.csv")
db_dir = os.path.join(project_root, "data", "database")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "velib.db")


chemin_home = "/"
chemin_carte_position = "/carte-positions"
chemin_velos_disponibles = "/velos-disponibles"
chemin_velos_electriques = "/velos-electriques"
chemin_velos_mecaniques = "/velos-mecaniques"
chemin_capacite_station = "/capacite-station"
chemin_taux_occupation_moyen = "/taux-occupation"
chemin_station_non_fonctionnelles = "/stations-non-fonctionnelles"
chemin_capacite_vs_disponibles = "/capacite-vs-disponibles"
