# main.py
from src.utils.Download_CSV import download_velib_csv

if __name__ == "__main__":
    print("=== Téléchargement du CSV Vélib en cours... ===")
    download_velib_csv()
    print("=== Téléchargement terminé ! ===")
    