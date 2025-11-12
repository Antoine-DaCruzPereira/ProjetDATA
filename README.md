# ProjetDATA
Projet de data E4 DSIA Paris de Antoine & Soen à l'ESIEE
# 🚴‍♂️ 

## 📝 Description

Ce projet a pour objectif de visualiser et analyser l'état des stations Vélib' à Paris.Il utilise des données mises à jour régulièrement, stockées dans une base de données SQLite crée par nous , pour ensuite  générer des graphes et cartes interactives  et des des disponibilités.

---

## ✨ Fonctionnalités Clés

* **Acquisition des Données :** Utilisation de fichiers CSV pour initialiser une base de données SQLite (`velib.db`).
* **Analyse de la Disponibilité :** Calcul du taux d'occupation, du nombre de vélos disponibles (mécaniques et électriques).
* **Visualisation Cartographique :** Génération d'une carte interactive (Folium ) (`velib_occupation_map.html`) montrant la position et le taux d'occupation des stations.
* **Visualisations Statistiques :** Création d'histogrammes dynamiques pour diverses métriques (capacité, vélos disponibles, taux d'occupation).
* **Nettoyage Automatique :** Suppression des anciennes visualisations HTML avant la génération des nouvelles.

---

## 🚀 Installation

### Prérequis

Assurez-vous d'avoir Python 3 installé.

### Environnement Python

1.  Clonez le dépôt :
    ```bash
    git clone [https://github.com/votre-nom-utilisateur/ProjetDATA.git](https://github.com/votre-nom-utilisateur/ProjetDATA.git)
    cd ProjetDATA
    ```

2.  Installez les dépendances nécessaires avec le fichier (`requirements.txt`):
    ```bash
    pip install -r requirements.txt
    ```

### Structure du Projet

Le projet suit la structure suivante :
<pre>
 ProjetDATA
├── 📁 .vscode
├── 📁 assets
│   ├── bar_stations_non_fonctionnelles.html
│   ├── hist_capacite_station.html
│   ├── hist_taux_occupation_moyen.html
│   ├── hist_velos_disponibles.html
│   ├── hist_velos_electriques.html
│   ├── hist_velos_mecaniques.html
│   ├── scatter_capacite_vs_velos_disponibles.html
│   └── velib_occupation_map.html
├── 📁 data
│   ├── 📁 cleandata
        ├──velib_disponibilite_clean.csv
│   ├── 📁 database
        ├──velib.db
│   └── 📁 rawdata
        ├──velib_disponibilite.csv
├── 📁 images
├── 📁 src
│   ├── 📁 components
        ├──__init__.py
        ├──footer.py     
        ├──navbar.py       
│   ├── 📁 pages
        ├──capacite_station.py
        ├──capacite_vs_velos_disponibles.py
        ├──carte_position.py
        ├──home.py
        ├──station_non_fonctionnelles.py
        ├──taux_occupation_moyen.py
        ├──velos_disponibles.py
        ├──velos_electriques.py
        ├──velos_mecaniques.py
│   └── 📁 utils
        ├──__init__.py
        ├──CleanData_CSV.py
        ├──Create_DataBase.py
        ├──Download_CSV.py
        ├──Histogramme.py
        ├──Map.py
        ├──velib_station.py
├── .gitignore
├── config.py
├── main.py
├── README.md
└── requirements.txt
</pre>