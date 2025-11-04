import sqlite3
import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import os
import folium
import branca.colormap as cm
from io import StringIO

# --- Configuration et Connexion BDD ---

# Chemin vers votre base de données (gardez-le global)
# Chemin relatif basé sur la structure PROJETDATA/data/database/velib.db
DB_PATH = os.path.join(os.path.dirname(__file__), "data/database/velib.db")

def get_db_connection():
    """Fonction utilitaire pour établir la connexion SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Erreur CRITIQUE de connexion à la base de données : {e}")
        print(f"Vérifiez le chemin : {DB_PATH}")
        return None

# --- Fonctions de Préparation des Données ---

def get_station_options():
    """Récupère la liste des stations pour peupler le dcc.Dropdown."""
    conn = get_db_connection()
    if conn is None:
        return [], None
    
    query = "SELECT identifiant_station, nom_station FROM stations ORDER BY nom_station"
    df_stations = pd.read_sql_query(query, conn)
    conn.close()
    
    options = [
        {'label': row['nom_station'], 'value': row['identifiant_station']}
        for _, row in df_stations.iterrows()
    ]
    
    default_value = options[0]['value'] if options else None
    
    return options, default_value

station_options, default_station_id = get_station_options()

def get_kpi_data():
    """Récupère les totaux les plus récents pour les cartes KPI.
    Utilise une fonction de fenêtre SQL pour garantir la dernière observation pour chaque station."""
    conn = get_db_connection()
    if conn is None:
        return 0, 0, 0
    
    # Nouvelle requête pour trouver la disponibilité la plus récente de chaque station
    query_kpis = """
    WITH LastDispo AS (
        SELECT 
            identifiant_station,
            velos_electriques,
            velos_mecaniques,
            -- Utilisation de ROW_NUMBER() pour marquer l'enregistrement le plus récent par station
            ROW_NUMBER() OVER(
                PARTITION BY identifiant_station 
                ORDER BY actualisation_donnee DESC
            ) as rn
        FROM disponibilites
        WHERE velos_electriques IS NOT NULL AND velos_mecaniques IS NOT NULL
    )
    SELECT 
        SUM(total_elec) AS total_elec, 
        SUM(total_meca) AS total_meca
    FROM (
        SELECT 
            SUM(velos_electriques) AS total_elec,
            SUM(velos_mecaniques) AS total_meca
        FROM LastDispo
        WHERE rn = 1
        GROUP BY identifiant_station
    )
    """
    
    try:
        df_kpis = pd.read_sql_query(query_kpis, conn)
        conn.close()
    except Exception as e:
        # En cas d'erreur SQL, cela peut signifier que la fonction de fenêtre n'est pas supportée
        # Retourne 0 et imprime l'erreur pour le débogage
        print(f"Erreur lors de l'exécution de la requête KPI (Utilisation de ROW_NUMBER) : {e}")
        conn.close()
        return 0, 0, 0

    if df_kpis.empty or df_kpis['total_elec'].isnull().all():
        return 0, 0, 0

    total_elec = df_kpis['total_elec'].iloc[0] if pd.notna(df_kpis['total_elec'].iloc[0]) else 0
    total_meca = df_kpis['total_meca'].iloc[0] if pd.notna(df_kpis['total_meca'].iloc[0]) else 0
    total_general = total_elec + total_meca
    
    return int(total_general), int(total_meca), int(total_elec)


# --- Initialisation de l'Application Dash ---

# Ajout de suppress_callback_exceptions=True pour gérer le routage multipage
app = dash.Dash(__name__, title='Dashboard VéliB', suppress_callback_exceptions=True)

# --- Définition des Layouts de Page ---

# Affiche un message d'erreur si la BDD n'a pas pu être chargée
initial_message = "Chargement des données VéliB..."
if not station_options:
    initial_message = "ERREUR : Impossible de charger la liste des stations. Vérifiez la connexion à la BDD."

# Définition des options pour le sélecteur d'histogramme
HISTOGRAM_OPTIONS = [
    {'label': 'Capacité Totale des Stations', 'value': 'capacite_station'},
    {'label': 'Vélos Disponibles (Méca. vs Élec.)', 'value': 'velos_types'},
    {'label': 'Vélos Mécaniques Disponibles', 'value': 'velos_mecaniques'},
    {'label': 'Vélos Électriques Disponibles', 'value': 'velos_electriques'},
]

def create_kpi_card(title, value, color, icon):
    """Génère un composant Div (carte KPI)."""
    return html.Div(
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'backgroundColor': 'white',
            'width': '30%',
            'minWidth': '180px',
            'margin': '10px',
        },
        children=[
            html.Div(icon, style={'fontSize': '3em', 'color': color, 'marginBottom': '10px'}),
            html.H3(title, style={'fontSize': '1.1em', 'color': '#555', 'textAlign': 'center'}),
            html.P(f"{value:,}".replace(",", " "), style={'fontSize': '2.5em', 'fontWeight': 'bold', 'color': color}),
        ]
    )

def serve_layout_page_home():
    """Layout pour la page d'accueil (KPIs)."""
    total_general, total_meca, total_elec = get_kpi_data()

    if total_general == 0 and station_options:
        kpi_message = "Les totaux de vélos les plus récents sont indisponibles. Affichez la carte pour la dernière heure d'actualisation connue."
    elif not station_options:
        kpi_message = "ERREUR : Impossible d'établir la connexion à la base de données."
    else:
        kpi_message = f"Statistiques Basées sur la Dernière Mise à Jour ({total_general:,} Vélos Totaux)".replace(",", " ")

    return html.Div([
        html.H1(
            "Vue d'Ensemble VéliB",
            style={'textAlign': 'center', 'color': '#333', 'marginBottom': '20px'}
        ),
        html.P(kpi_message, style={'textAlign': 'center', 'color': '#555', 'marginBottom': '40px'}),

        html.Div(
            style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'space-around',
                'maxWidth': '900px',
                'margin': '0 auto'
            },
            children=[
                create_kpi_card("Total Général", total_general, '#4B0082', '🚲'),
                create_kpi_card("Vélos Mécaniques", total_meca, '#8A2BE2', '⚙️'),
                create_kpi_card("Vélos Électriques", total_elec, '#DAA520', '⚡'),
            ]
        ),
        html.Div([
            dcc.Link('Voir l\'Évolution Détaillée par Station →', href='/evolution-station', style={
                'textDecoration': 'none',
                'padding': '10px 20px',
                'borderRadius': '5px',
                'backgroundColor': '#8A2BE2',
                'color': 'white',
                'fontWeight': 'bold',
                'marginTop': '40px',
                'display': 'inline-block'
            })
        ], style={'textAlign': 'center'})
    ])


def serve_layout_page_evolution():
    """Layout pour l'évolution par station (anciennement page d'accueil)."""
    return html.Div([
        html.H1(
            "Évolution de la Disponibilité par Station",
            style={'textAlign': 'center', 'color': '#333', 'marginBottom': '30px'}
        ),
        html.Div([
            html.Label("Sélectionnez une station :", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='station-dropdown',
                options=station_options,
                value=default_station_id,
                placeholder="Choisir une station...",
                disabled=not station_options,
                style={'width': '100%'}
            ),
        ], style={'width': '80%', 'maxWidth': '600px', 'margin': '0 auto 40px auto'}),
        dcc.Graph(
            id='station-graph',
            style={'height': '600px'},
            figure={'data': [], 'layout': {'title': initial_message}}
        ),
    ])


def serve_layout_page_distribution():
    """Layout pour la page des histogrammes (Distribution globale) avec sélecteur."""
    
    return html.Div([
        html.H1("Analyse Globale des Stations VéliB", style={'textAlign': 'center', 'color': '#333', 'marginBottom': '30px'}),
        
        # Sélecteur d'Histogramme
        html.Div([
            html.Label("Sélectionnez le graphique à afficher :", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='histogram-selector',
                options=HISTOGRAM_OPTIONS,
                value=HISTOGRAM_OPTIONS[0]['value'],  # Valeur par défaut: Capacité
                clearable=False,
                style={'width': '100%'}
            ),
        ], style={'width': '80%', 'maxWidth': '800px', 'margin': '0 auto 40px auto'}),
        
        # Conteneur pour l'histogramme dynamique
        dcc.Graph(
            id='dynamic-histogram',
            style={'height': '600px'}
        ),
    ])

def serve_layout_page_map():
    """Layout pour la page Carte (Carte Folium interactive)."""
    
    conn = get_db_connection()
    if conn is None:
         return html.Div(html.H2("ERREUR : Connexion à la base de données impossible.", style={'color': 'red', 'textAlign': 'center'}))

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
        return html.Div(html.H2("Aucune donnée de station à afficher sur la carte.", style={'textAlign': 'center'}))
    
    # Calcul du taux d'occupation et gestion des NaN/erreurs (important pour Folium)
    df_map['taux_occupation'] = (df_map['velos_disponibles'] / df_map['capacite_station']) * 100
    df_map["taux_occupation"] = df_map["taux_occupation"].clip(0, 100)

    # Création de la carte Folium centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12, tiles='OpenStreetMap')

    # Définition de la colormap (Vert=Disponible, Rouge=Occupé)
    colormap = cm.LinearColormap(colors=['green', 'yellow', 'red'], vmin=0, vmax=100, caption='Taux d\'occupation (%)')
    colormap.add_to(m)

    # Ajout des marqueurs circulaires
    for _, row in df_map.iterrows():
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

    # Sauvegarder la carte Folium dans une chaîne HTML en mémoire
    map_html = m._repr_html_()

    # Intégration dans un Iframe Dash
    return html.Div([
        html.H1("Carte Interactive des Stations VéliB (Folium)", style={'textAlign': 'center', 'color': '#333', 'marginBottom': '20px'}),
        html.Div(
            html.Iframe(
                srcDoc=map_html,
                style={
                    "width": "100%", 
                    "height": "800px", 
                    "border": "1px solid #ccc",
                    "borderRadius": "8px"
                }
            ),
            style={'margin': '0 auto', 'width': '95%'}
        )
    ])


# --- Définition du Layout PRINCIPAL (Routage) ---

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    # Composant pour lire l'URL
    dcc.Location(id='url', refresh=False),
    
    # Barre de navigation simple
    html.Div([
        dcc.Link('Accueil (KPIs)', href='/', style={'marginRight': '20px', 'textDecoration': 'none', 'padding': '8px 15px', 'borderRadius': '5px', 'backgroundColor': '#EEE', 'border': '1px solid #CCC'}),
        dcc.Link('Évolution par Station', href='/evolution-station', style={'marginRight': '20px', 'textDecoration': 'none', 'padding': '8px 15px', 'borderRadius': '5px', 'backgroundColor': '#EEE', 'border': '1px solid #CCC'}),
        dcc.Link('Distribution Globale', href='/distribution', style={'marginRight': '20px', 'textDecoration': 'none', 'padding': '8px 15px', 'borderRadius': '5px', 'backgroundColor': '#EEE', 'border': '1px solid #CCC'}),
        dcc.Link('Carte des Stations (Folium)', href='/map', style={'textDecoration': 'none', 'padding': '8px 15px', 'borderRadius': '5px', 'backgroundColor': '#EEE', 'border': '1px solid #CCC'}),
    ], style={'textAlign': 'center', 'paddingBottom': '20px', 'marginBottom': '20px'}),
    
    # Conteneur pour le contenu de la page
    html.Div(id='page-content')
])


# --- Callbacks de Routage et de Contenu ---

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """Callback pour changer de page en fonction de l'URL."""
    if pathname == '/evolution-station':
        return serve_layout_page_evolution()
    elif pathname == '/distribution':
        return serve_layout_page_distribution()
    elif pathname == '/map':
        return serve_layout_page_map()
    elif pathname == '/':
        return serve_layout_page_home()
    else:
        # Page d'erreur 404
        return html.Div([
            html.H1("404: Page non trouvée", style={'textAlign': 'center'}),
            html.P(f"L'URL {pathname} n'existe pas.", style={'textAlign': 'center'})
        ])


# Callback pour l'ÉVOLUTION PAR STATION

@app.callback(
    Output('station-graph', 'figure'),  # Mise à jour du graphique de la page HOME
    [Input('station-dropdown', 'value')] 
)
def update_station_data(selected_station_id):
    if selected_station_id is None:
        return {'data': [], 'layout': {'title': "Sélectionnez une station pour afficher les données."}} 

    conn = get_db_connection()
    if conn is None:
        return {'data': [], 'layout': {'title': "ERREUR : Connexion à la base de données impossible."}}

    # Requête paramétrée sécurisée
    query = """
    SELECT 
        s.nom_station,
        d.velos_disponibles,
        d.velos_mecaniques,
        d.velos_electriques,
        d.actualisation_donnee AS date_heure
    FROM stations AS s
    JOIN disponibilites AS d 
        ON s.identifiant_station = d.identifiant_station
    WHERE 
        s.identifiant_station = ? AND 
        d.velos_mecaniques IS NOT NULL AND 
        d.velos_electriques IS NOT NULL
    ORDER BY d.actualisation_donnee DESC
    LIMIT 100
    """
    
    df_station = pd.read_sql_query(query, conn, params=(selected_station_id,))
    conn.close()
    
    if df_station.empty:
        return px.bar(title=f"Aucune donnée trouvée pour la station {selected_station_id}")

    station_name = df_station['nom_station'].iloc[0]

    # Aplatir les données pour Plotly.express
    df_flat = pd.melt(
        df_station,
        id_vars=['date_heure'],
        value_vars=['velos_mecaniques', 'velos_electriques'],
        var_name='Type de Vélo',
        value_name='Nombre de Vélos'
    )
    
    fig = px.bar(
        df_flat.sort_values('date_heure'),
        x='date_heure', 
        y='Nombre de Vélos', 
        color='Type de Vélo', # Sépare les barres par type
        title=f"Évolution des Vélos Disponibles à la station : {station_name}",
        labels={
            'date_heure': 'Heure d\'Observation', 
            'Nombre de Vélos': 'Nombre de Vélos Disponibles'
        },
        barmode='stack', # Pour empiler les vélos mécaniques et électriques
        template='plotly_white'
    )
    
    fig.update_layout(xaxis_title="Heure d'Observation", yaxis_title="Vélos Disponibles (Total)")
    
    return fig

# Callback pour la PAGE DISTRIBUTION (Histogramme dynamique)
@app.callback(
    Output('dynamic-histogram', 'figure'),
    [Input('histogram-selector', 'value')] 
)
def update_dynamic_histogram(selected_metric):
    conn = get_db_connection()
    if conn is None:
        return {'data': [], 'layout': {'title': "ERREUR : Connexion à la base de données impossible."}}

    # 1. Traitement pour les métriques de disponibilité (velos_mecaniques / velos_electriques)
    if selected_metric in ['velos_mecaniques', 'velos_electriques']:
        column = selected_metric
        
        # Requête pour récupérer toutes les données de la colonne spécifique
        query = f"""
        SELECT {column} AS metric
        FROM disponibilites
        WHERE {column} IS NOT NULL
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return px.bar(title=f"Aucune donnée trouvée pour {selected_metric}")
            
        fig = px.histogram(
            df, 
            x='metric', 
            nbins=30, 
            title=f'Distribution de la métrique : {selected_metric.replace("_", " ").title()}',
            labels={'metric': selected_metric.replace("_", " ").title()},
            template='plotly_white',
            color_discrete_sequence=['#8A2BE2']
        )
        # CHANGEMENT DE LA LÉGENDE Y pour être plus explicite
        fig.update_layout(
            xaxis_title="Vélos Disponibles",
            yaxis_title="Nombre de Vélos par Station" # Mise à jour de l'étiquette Y
        )
        return fig

    # 2. Traitement pour la Capacité Totale (capacite_station)
    elif selected_metric == 'capacite_station':
        query = "SELECT capacite_station FROM stations WHERE capacite_station IS NOT NULL AND capacite_station > 0"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return px.bar(title="Aucune donnée de capacité trouvée.")
        
        fig = px.histogram(
            df, 
            x='capacite_station', 
            nbins=20, 
            title='Distribution des Capacités Totales des Stations',
            labels={'capacite_station': 'Capacité Totale (Nombre de Bornettes)'},
            template='plotly_white',
            color_discrete_sequence=['#4B0082']
        )
        # CHANGEMENT DE LA LÉGENDE Y
        fig.update_layout(
            xaxis_title='Capacité Totale (Nombre de Bornettes)',
            yaxis_title="Nombre de Stations"
        )
        return fig
        
    # 3. Traitement pour les types de vélos superposés (velos_types)
    elif selected_metric == 'velos_types':
        query = """
        SELECT 
            velos_mecaniques, 
            velos_electriques
        FROM disponibilites
        WHERE 
            velos_mecaniques IS NOT NULL AND 
            velos_electriques IS NOT NULL
        """
        df_dispo = pd.read_sql_query(query, conn)
        conn.close()

        if df_dispo.empty:
             return px.bar(title="Aucune donnée de vélos trouvée.")
             
        df_flat = pd.melt(
            df_dispo, 
            value_vars=['velos_mecaniques', 'velos_electriques'],
            var_name='Type de Vélo', 
            value_name='Nombre de Vélos'
        )
        
        fig = px.histogram(
            df_flat,
            x='Nombre de Vélos',
            color='Type de Vélo', 
            title="Distribution des Vélos Mécaniques et Électriques Disponibles",
            barmode='overlay',
            nbins=40,
            opacity=0.7,
            log_y=True,
            labels={'Nombre de Vélos': 'Nombre de Vélos Disponibles par Station'},
            color_discrete_map={
                'velos_mecaniques': '#8A2BE2', 
                'velos_electriques': '#DAA520'
            },
            template='plotly_white'
        )
        # CHANGEMENT DE LA LÉGENDE Y (maintenu en Log Scale)
        fig.update_layout(xaxis_title="Nombre de Vélos Disponibles", yaxis_title="Fréquence des Observations (Échelle Logarithmique)")
        return fig

    # Cas par défaut si aucune métrique n'est sélectionnée (ne devrait pas arriver)
    return {'data': [], 'layout': {'title': "Sélectionnez une métrique pour visualiser la distribution."}}


# --- Lancement du Serveur ---

if __name__ == '__main__':
    app.run(debug=True)