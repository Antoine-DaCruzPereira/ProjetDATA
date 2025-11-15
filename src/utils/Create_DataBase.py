import os
import pandas as pd
import sqlite3
from datetime import datetime
from config import cleandata_path, db_path

def create_velib_database():

    # Suppression de l'ancienne base de données si elle existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Ancienne base de données supprimée : {db_path}")

    # Lecture du fichier CSV nettoyé
    print(f"Lecture du fichier CSV : {cleandata_path}")
    df = pd.read_csv(cleandata_path)

    # Création de la connexion à la base de données
    print("Création de la base de données...")
    conn = sqlite3.connect(db_path)

    try:
        # Séparation des coordonnées géographiques
        df[['latitude', 'longitude']] = df['Coordonnées géographiques'].str.strip('()').str.split(',', expand=True).astype(float)
        
        # 1. Création et remplissage de la table communes
        print("Création de la table communes...")
        conn.execute("""
        CREATE TABLE communes (
            code_insee TEXT PRIMARY KEY,
            nom_commune TEXT NOT NULL
        )
        """)
        
        # Extraction des communes uniques
        communes_df = df[['Code INSEE communes équipées', 'Nom communes équipées']].dropna().drop_duplicates()
        communes_df.to_sql('communes', conn, if_exists='replace', index=False, 
                          dtype={'code_insee': 'TEXT PRIMARY KEY', 
                                'nom_commune': 'TEXT'})

        # 2. Création de la table stations
        print("Création de la table stations...")
        conn.execute("""
        CREATE TABLE stations (
            identifiant_station TEXT PRIMARY KEY,
            nom_station TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            capacite_station INTEGER NOT NULL,
            code_insee TEXT,
            FOREIGN KEY (code_insee) REFERENCES communes(code_insee)
        )
        """)

        # 3. Création de la table etats
        print("Création de la table etats...")
        conn.execute("""
        CREATE TABLE etats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifiant_station TEXT NOT NULL,
            actualisation_donnee TIMESTAMP NOT NULL,
            station_en_fonctionnement INTEGER NOT NULL,
            borne_paiement INTEGER NOT NULL,
            retour_possible INTEGER NOT NULL,
            FOREIGN KEY (identifiant_station) REFERENCES stations(identifiant_station)
        )
        """)

        # 4. Création de la table disponibilites
        print("Création de la table disponibilites...")
        conn.execute("""
        CREATE TABLE disponibilites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifiant_station TEXT NOT NULL,
            actualisation_donnee TIMESTAMP NOT NULL,
            bornettes_libres INTEGER NOT NULL,
            velos_disponibles INTEGER NOT NULL,
            velos_mecaniques INTEGER NOT NULL,
            velos_electriques INTEGER NOT NULL,
            FOREIGN KEY (identifiant_station) REFERENCES stations(identifiant_station)
        )
        """)

        # Préparation et insertion des données dans la table stations
        stations_data = df[[
            'Identifiant station', 'Nom station', 'latitude', 'longitude',
            'Capacité de la station', 'Code INSEE communes équipées'
        ]].drop_duplicates()
        
        stations_data.columns = [
            'identifiant_station', 'nom_station', 'latitude', 'longitude',
            'capacite_station', 'code_insee'
        ]
        
        stations_data.to_sql('stations', conn, if_exists='replace', index=False)

        # Préparation et insertion des données dans la table etats
        etats_data = df[[
            'Identifiant station', 'Actualisation de la donnée',
            'Station en fonctionnement', 'Borne de paiement disponible', 'Retour vélib possible'
        ]]
        
        etats_data.columns = [
            'identifiant_station', 'actualisation_donnee',
            'station_en_fonctionnement', 'borne_paiement', 'retour_possible'
        ]
        
        # Conversion des booléens en entiers
        bool_columns = ['station_en_fonctionnement', 'borne_paiement', 'retour_possible']
        for col in bool_columns:
            etats_data[col] = etats_data[col].astype(int)
            
        etats_data.to_sql('etats', conn, if_exists='replace', index=False)

        # Préparation et insertion des données dans la table disponibilites
        disponibilites_data = df[[
            'Identifiant station', 'Actualisation de la donnée',
            'Nombre bornettes libres', 'Nombre total vélos disponibles',
            'Vélos mécaniques disponibles', 'Vélos électriques disponibles'
        ]]
        
        disponibilites_data.columns = [
            'identifiant_station', 'actualisation_donnee',
            'bornettes_libres', 'velos_disponibles',
            'velos_mecaniques', 'velos_electriques'
        ]
        
        disponibilites_data.to_sql('disponibilites', conn, if_exists='replace', index=False)

        # Création des index pour optimiser les performances
        print("Création des index...")
        conn.execute("CREATE INDEX idx_stations_commune ON stations(code_insee)")
        conn.execute("CREATE INDEX idx_etats_station ON etats(identifiant_station)")
        conn.execute("CREATE INDEX idx_etats_date ON etats(actualisation_donnee)")
        conn.execute("CREATE INDEX idx_disponibilites_station ON disponibilites(identifiant_station)")
        conn.execute("CREATE INDEX idx_disponibilites_date ON disponibilites(actualisation_donnee)")

        print(f"Base de données créée avec succès : {db_path}")
        print(f"Nombre de stations importées : {len(stations_data)}")
        print(f"Nombre de communes : {len(communes_df)}")
        print(f"Nombre d'états enregistrés : {len(etats_data)}")
        print(f"Nombre de disponibilités enregistrées : {len(disponibilites_data)}")

    except Exception as e:
        print(f"Erreur lors de la création de la base de données : {str(e)}")
        raise

    finally:
        conn.close()

if __name__ == "__main__":
    create_velib_database()
