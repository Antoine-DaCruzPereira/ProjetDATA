import os
import folium
import pandas as pd
import branca.colormap as cm
import sqlite3

# Chemin d'accès à la base de données (gardé pour la connexion)
# NOTE: Le chemin relatif nécessite que le script soit exécuté dans un contexte spécifique
# où 'data/database/velib.db' est accessible.
# Pour simplifier, nous utilisons le chemin tel qu'il est défini dans le code original
# mais il peut nécessiter des ajustements en fonction de l'environnement d'exécution.
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                       "..", # Remonte à src
                                       "..", # Remonte à ProjetDATA
                                       "data", "database", "velib.db"))

def get_db_connection():
    """Fonction utilitaire pour établir la connexion SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Erreur CRITIQUE de connexion à la base de données : {e}")
        print(f"Vérifiez le chemin : {DB_PATH}")
        return None

def Map_Int():
    """Crée une carte Folium interactive des stations Vélib' et l'enregistre en HTML."""
    
    conn = get_db_connection()
    if conn is None:
         print("Création de carte annulée : Connexion à la base de données impossible.")
         return

    # Requête pour récupérer les données de station avec la dernière disponibilité
    query = """
    SELECT 
        s.nom_station,
        s.latitude,
        s.longitude,
        s.capacite_station,
        d.velos_disponibles,
        d.actualisation_donnee
    FROM stations AS s
    JOIN disponibilites AS d 
        ON s.identifiant_station = d.identifiant_station
    WHERE
        s.capacite_station IS NOT NULL AND 
        d.velos_disponibles IS NOT NULL
    ORDER BY d.actualisation_donnee DESC
    LIMIT 1000 
    """
    df_map = pd.read_sql_query(query, conn)
    conn.close()

    if df_map.empty:
        print("Aucune donnée de station à afficher sur la carte. Carte non créée.")
        return
    
    # --- Traitement des données pour la carte ---
    
    # Calcul du taux d'occupation (capé entre 0 et 100%)
    df_map['taux_occupation'] = (df_map['velos_disponibles'] / df_map['capacite_station']) * 100
    df_map["taux_occupation"] = df_map["taux_occupation"].clip(0, 100)

    # Création de la carte Folium centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12, tiles='OpenStreetMap')

    # Définition de la colormap (Vert=Disponible, Rouge=Occupé)
    colormap = cm.LinearColormap(colors=['green', 'yellow', 'red'], vmin=0, vmax=100, caption='Taux d\'occupation (%)')
    colormap.add_to(m)

    # Ajout des marqueurs circulaires
    for _, row in df_map.iterrows():
        # Extrait l'heure pour l'affichage dans le popup
        maj_time = row['actualisation_donnee'].split(' ')[1].split('+')[0] if pd.notna(row['actualisation_donnee']) else "N/A"
        
        popup_html = f"""
        <b>{row['nom_station']}</b><br>
        Capacité : {row['capacite_station']} bornettes<br>
        Vélos dispo : {row['velos_disponibles']}<br>
        Taux d’occupation : <b>{row['taux_occupation']:.1f} %</b><br>
        Dernière maj : {maj_time}
        """
        
        # Création du marqueur avec couleur basée sur le taux d'occupation
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color=colormap(row['taux_occupation']),
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)

    # --- Enregistrement de la carte ---
    
    # Définition du chemin de sortie
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/velib_occupation_map.html"))
    
    # Création des répertoires si nécessaire
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Enregistrement de la carte
    m.save(output_path)
    print(f"Carte Folium interactive enregistrée dans : {output_path}")

# Appel de la fonction pour exécuter la création de la carte
if __name__ == '__main__':
    Map_Int()