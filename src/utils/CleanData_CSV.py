import os
import pandas as pd
from pydantic import ValidationError
from src.utils.velib_station import VelibStation

def remove_empty_columns(df):
    """
    Détecte et supprime les colonnes entièrement vides d'un DataFrame.
    Une colonne est considérée comme vide si elle ne contient que des valeurs None, NaN ou chaînes vides.
    
    Args:
        df (pd.DataFrame): Le DataFrame à nettoyer
        
    Returns:
        pd.DataFrame: Le DataFrame sans les colonnes vides
        list: La liste des colonnes supprimées
    """
    # Vérifie chaque colonne pour trouver celles qui sont entièrement vides
    empty_mask = df.isna().all()  # Trouve les colonnes où tout est NaN
    empty_or_none_mask = df.isnull().all()  # Trouve les colonnes où tout est NaN ou None
    
    # Pour les colonnes de type string, vérifie aussi les chaînes vides
    string_columns = df.select_dtypes(include=['object']).columns
    for col in string_columns:
        if not empty_mask[col] and not empty_or_none_mask[col]:
            # Si la colonne n'est pas déjà marquée comme vide, vérifie les chaînes vides
            if df[col].fillna('').str.strip().eq('').all():
                empty_mask[col] = True

    # Liste des colonnes à supprimer
    empty_columns = df.columns[empty_mask].tolist()
    
    if empty_columns:
        return df.drop(columns=empty_columns), empty_columns
    
    return df, []

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
        print(f"Ancien fichier nettoyé supprimé : {cleandata_path}")

    # --- Lecture du fichier  ---
    df = pd.read_csv(rawdata_path, sep=';', dtype={
        'Identifiant station': str,
        'Code INSEE communes équipées': str
    })
    # Remplacer les NaN par None pour les colonnes optionnelles
    optional_columns = ['station_opening_hours', 'Nom communes équipées', 'Code INSEE communes équipées']
    for col in optional_columns:
        df[col] = df[col].where(pd.notna(df[col]), None)
        # Convertir explicitement les valeurs NaN en None
        df[col] = df[col].astype(object).replace({pd.NA: None, pd.NaT: None, float('nan'): None})
    
    # Supprimer les colonnes entièrement vides
    df, removed_columns = remove_empty_columns(df)

    valid_rows = []
    invalid_count = 0

    # --- Validation et filtrage des lignes ---
    for idx, row in df.iterrows():
        try:
            # Validation avec Pydantic
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
        # Création du DataFrame nettoyé
        clean_df = pd.DataFrame(valid_rows)
        
        # Détection et suppression automatique des colonnes vides
        clean_df, removed_columns = remove_empty_columns(clean_df)
        if removed_columns:
            print("Colonnes automatiquement supprimées car vides :", ", ".join(removed_columns))
        
        # Sauvegarde du fichier
        clean_df.to_csv(cleandata_path, index=False)
        print(f"Fichier nettoyé : {cleandata_path}")
        print(f"Lignes traitées : {len(df)} → {len(valid_rows)} conservées")
    else:
        print("Aucune donnée valide trouvée, aucun fichier créé.")

if __name__ == "__main__":
    clean_velib_csv()
