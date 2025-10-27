# main.py
from src.pages.première_page import create_home_layout
from src.utils.Download_CSV import download_velib_csv
from src.utils.CleanData_CSV import clean_velib_csv
from src.utils.Create_DataBase import create_velib_database
from src.utils.Histogramme import create_histograms 

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

<<<<<<< HEAD
if __name__ == "__main__":
    # Initialisation des données
    init_data()
=======
    print("\n=== Génération des histogrammes ===")
    print("----------------------------------------")
    create_histograms()

    print("\n=== Génération des histogrammes terminée ! ===\n")
    
>>>>>>> c117eaa9aed5bad1f7cf8673d29f93192d3c29e7
