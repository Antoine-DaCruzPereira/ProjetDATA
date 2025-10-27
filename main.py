# main.py
from src.pages.première_page import create_home_layout
from src.utils.Download_CSV import download_velib_csv
from src.utils.CleanData_CSV import clean_velib_csv
from src.utils.Create_DataBase import create_velib_database

def init_data():
    """Initialise les données nécessaires au dashboard"""
    print("\n=== 1. Téléchargement du CSV Vélib ===")
    print("--------------------------------------")
    download_velib_csv()

    print("\n=== 2. Nettoyage et validation du CSV ===")
    print("----------------------------------------")
    clean_velib_csv()

    print("\n=== 3. Création de la base de données ===")
    print("----------------------------------------")
    create_velib_database()

    print("\n=== Pipeline de données terminé avec succès ! ===\n")

if __name__ == "__main__":
    # Initialisation des données
    init_data()