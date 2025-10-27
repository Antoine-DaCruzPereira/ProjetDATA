import os
import folium
import pandas as pd
import branca.colormap as cm
import sqlite3


#Charger le fichier CSV nettoyé
#csv_clean=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/cleandata/velib_disponibilite_clean.csv"))
#df = pd.read_csv(csv_clean,sep=';')

#Charger la base de données
db_path = os.path.join(os.path.dirname(__file__), "../../data/database/velib.db")
conn = sqlite3.connect(db_path)

#recupérer les coordonnées
#df['latitude'] = df['Coordonnées géographiques'].apply(lambda x: float(x.split(',')[0].replace('(','')))
#df['longitude'] = df['Coordonnées géographiques'].apply(lambda x: float(x.split(',')[1].replace(')','')))
query = """
SELECT 
    s.identifiant_station,
    s.nom_station,
    s.latitude,
    s.longitude,
    s.capacite_station,
    d.velos_disponibles
FROM stations AS s
JOIN disponibilites AS d 
    ON s.identifiant_station = d.identifiant_station
"""
df = pd.read_sql_query(query, conn)
conn.close()


#Recuperer le taux d'occupation
df['taux_occupation'] = (df['velos_disponibles'] / df['capacite_station'])*100
df["taux_occupation"] = df["taux_occupation"].clip(0, 100)

#Centrer la carte sur Paris
m=folium.Map(location=[48.8566, 2.3522], zoom_start=12,tiles='OpenStreetMap')

#Couleur des differentes
colormap = cm.LinearColormap(colors=['green', 'yellow', 'red'], vmin=0, vmax=100, caption='Taux d\'occupation (%)')
colormap.add_to(m)

#Ajouter les sations sur la carte 
#for _,row in df.iterrows():
#    popup_text = f"Station: {row['Nom de la station']}<br>Taux d'occupation: {row['taux_occupation']:.2f}%"
#    folium.CircleMarker(
#        location=[row['latitude'], row['longitude']],
#        radius=6,
#        color=colormap(row['taux_occupation']),
#        fill=True,
#       fill_opacity=0.7,
#        popup=folium.Popup(popup_text, max_width=300)
 #   ).add_to(m)

for _, row in df.iterrows():
    popup_html = f"""
    <b>{row['nom_station']}</b><br>
    Capacité : {row['capacite_station']} bornettes<br>
    Vélos dispo : {row['velos_disponibles']}<br>
    Taux d’occupation : {row['taux_occupation']:.1f} %
    """
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=1,
        color="red",
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(
            f"<b>{row['nom_station']}</b><br>Capacité : {row['capacite_station']} bornettes",
            max_width=250
        )
    ).add_to(m)


#Enregister la carte 
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../images/maps/velib_occupation_map.html"))
os.makedirs(os.path.dirname(output_path), exist_ok=True)
m.save(output_path)

print(f"Carte enregistrée dans : {output_path}")