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
    
    print(f"Fichier source : {rawdata_path}")
    
    # Suppression de l'ancien fichier clean s'il existe
    if os.path.exists(cleandata_path):
        os.remove(cleandata_path)

    # --- Lecture du fichier brut ---
    df = pd.read_csv(rawdata_path, sep=';', dtype={
        'Identifiant station': str,
        'Code INSEE communes équipées': str
    })
    # Remplacer les NaN par None pour station_opening_hours et autres colonnes optionnelles
    optional_columns = ['station_opening_hours', 'Nom communes équipées', 'Code INSEE communes équipées']
    for col in optional_columns:
        df[col] = df[col].where(pd.notna(df[col]), None)
        # Convertir explicitement les valeurs NaN en None
        df[col] = df[col].astype(object).replace({pd.NA: None, pd.NaT: None, float('nan'): None})

    valid_rows = []
    invalid_count = 0

    # --- Validation et filtrage des lignes ---
    for idx, row in df.iterrows():
        try:
            # Validation via Pydantic
            record = VelibStation(**row.to_dict())
            valid_rows.append(record.model_dump(by_alias=True))
        except ValidationError as e:
            print(f"Erreur de validation à la ligne {idx+1}:")
            print(str(e))
            invalid_count += 1
        except Exception as e:
            print(f"Erreur inattendue à la ligne {idx+1}:")
            print(str(e))
            invalid_count += 1

    # --- Sauvegarde dans le répertoire cleandata ---
    if valid_rows:
        clean_df = pd.DataFrame(valid_rows)
        clean_df.to_csv(cleandata_path, index=False)
        print(f"Fichier nettoyé : {cleandata_path}")
        print(f"Lignes traitées : {len(df)} → {len(valid_rows)} conservées")
    else:
        print("Aucune donnée valide trouvée, aucun fichier créé.")

if __name__ == "__main__":
    clean_velib_csv()
