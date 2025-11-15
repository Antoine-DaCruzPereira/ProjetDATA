import os
import requests

def download_velib_csv():
    csv_url = "https://www.data.gouv.fr/api/1/datasets/r/0845c838-6f18-40c3-936f-da204107759a"

    # Chemin absolu basé sur la racine du projet
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    rawdata_dir = os.path.join(project_root, "data", "rawdata")
    os.makedirs(rawdata_dir, exist_ok=True)

    dest_path = os.path.join(rawdata_dir, "velib_disponibilite.csv")

    # Suppression de l'ancien fichier s'il existe
    if os.path.exists(dest_path):
        os.remove(dest_path)
        print(f"Suppression de l'ancien fichier : {dest_path}")

    print(f"Téléchargement du fichier depuis : {csv_url}")
    resp = requests.get(csv_url)
    resp.raise_for_status()

    with open(dest_path, "wb") as f:
        f.write(resp.content)

    print(f"Fichier enregistré dans : {dest_path}")

if __name__ == "__main__":
    download_velib_csv()