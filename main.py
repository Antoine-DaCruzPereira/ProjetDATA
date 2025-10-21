# main.py
from src.utils.Download_CSV import download_velib_csv
from src.utils.CleanData_CSV import clean_velib_csv

if __name__ == "__main__":
    print("=== Téléchargement du CSV Vélib en cours... ===")
    download_velib_csv()
    print("=== Téléchargement terminé ! ===")

    print("=== Nettoyage et validation du CSV en cours... ===")
    clean_velib_csv()
    print("=== Données nettoyées et enregistrées avec succès ! ===")
