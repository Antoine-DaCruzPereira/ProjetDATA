import os
import pandas as pd
from pydantic import ValidationError
from src.utils.velib_station import VelibStation

def clean_velib_csv():
    # --- Définition des chemins ---
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    rawdata_path = os.path.join(project_root, "data", "rawdata", "velib_disponibilite.csv")
    cleandata_dir = os.path.join(project_root, "data", "cleandata")
    os.makedirs(cleandata_dir, exist_ok=True)
    cleandata_path = os.path.join(cleandata_dir, "velib_disponibilite_clean.csv")

    # --- Lecture du fichier brut ---
    print(f"Lecture du fichier brut : {rawdata_path}")
    df = pd.read_csv(rawdata_path)
    print(f"Nombre total de lignes dans le CSV brut : {len(df)}")

    valid_rows = []
    invalid_count = 0

    # --- Validation et filtrage des lignes ---
    for _, row in df.iterrows():
        try:
            # Validation via Pydantic
            record = VelibStation(**row.to_dict())
            valid_rows.append(record.model_dump(by_alias=True))
        except ValidationError:
            invalid_count += 1
        except Exception:
            invalid_count += 1

    # --- Sauvegarde dans le répertoire cleandata ---
    print(f"Lignes valides conservées : {len(valid_rows)}")
    print(f"Lignes invalides supprimées : {invalid_count}")

    if valid_rows:
        clean_df = pd.DataFrame(valid_rows)
        clean_df.to_csv(cleandata_path, index=False)
        print(f"✅ Fichier nettoyé enregistré dans : {cleandata_path}")
    else:
        print("⚠️ Aucune donnée valide trouvée, aucun fichier créé.")

    # --- Récapitulatif final ---
    print("\n=== Résumé du nettoyage ===")
    print(f"Fichier source brut : {rawdata_path}")
    print(f"Fichier nettoyé      : {cleandata_path}")
    print(f"Lignes brutes        : {len(df)}")
    print(f"Lignes valides       : {len(valid_rows)}")
    print(f"Lignes supprimées    : {invalid_count}")
    print("=============================\n")

if __name__ == "__main__":
    clean_velib_csv()
