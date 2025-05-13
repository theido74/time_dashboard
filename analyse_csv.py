import pandas as pd
import os
import datetime

# Lire le fichier CSV
fichier = 'time_board.csv'
df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])

# Fichier pour stocker les utilisateurs associés aux adresses MAC
fichier_utilisateurs = 'utilisateurs_mac.csv'

def find_user(fichier_utilisateurs):
    # Charger les utilisateurs existants depuis le fichier, s'il existe
    if os.path.exists(fichier_utilisateurs):
        df_utilisateurs = pd.read_csv(fichier_utilisateurs)
        liste_authorite = dict(zip(df_utilisateurs['MAC Address'], df_utilisateurs['Utilisateur']))
    else:
        liste_authorite = {}
    
    # Demander les utilisateurs pour les adresses MAC non enregistrées
    for mac in df['MAC Address'].unique():
        if mac not in liste_authorite:
            utilisateur = input(f'Qui est l\'utilisateur de cet appareil? {mac} : ')
            liste_authorite[mac] = utilisateur

    # Enregistrer les utilisateurs dans le fichier
    df_utilisateurs = pd.DataFrame(list(liste_authorite.items()), columns=['MAC Address', 'Utilisateur'])
    df_utilisateurs.to_csv(fichier_utilisateurs, index=False)

    return liste_authorite

def projet_par_mac(df):
    # Créer un dictionnaire pour stocker les adresses MAC et leurs projets associés
    projets_par_mac = {}
    for mac in df['MAC Address'].unique():
        # Filtrer le DataFrame pour obtenir les lignes correspondant à l'adresse MAC
        lignes_mac = df[df['MAC Address'] == mac]
        
        # Obtenir la liste des projets associés à cette adresse MAC
        projets = lignes_mac['Directory'].unique()
        
        # Stocker les projets dans le dictionnaire
        projets_par_mac[mac] = projets
    
    return projets_par_mac

def temps_par_projet_et_user(fichier_utilisateurs):
    df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])

    # Créer un dictionnaire pour stocker le temps total par projet et par adresse MAC
    temps_par_projet_mac = {}

    # Parcourir chaque ligne du DataFrame
    for index, row in df.iterrows():
        projet = row['Directory']
        temps = row['Duration']
        mac_address = row['MAC Address']

        # Créer une clé unique pour le projet et l'adresse MAC
        key = (projet, mac_address)
        
        if key not in temps_par_projet_mac:
            temps_par_projet_mac[key] = 0
        temps_par_projet_mac[key] += temps

    # Récupérer les utilisateurs associés aux adresses MAC
    liste_authorite = find_user(fichier_utilisateurs)

    df_tpp = pd.DataFrame(list(temps_par_projet_mac.items()), columns=['Projet et MAC Address', 'Temps'])
    df_tpp_final = df_tpp.sort_values(by='Temps', ascending=False, ignore_index=True)
    print(list(df_tpp_final['Directory et MAC Address'][0:3]))


    return list(df_tpp_final['Projet et MAC Address'][0:3])



df_tri = df.sort_values(by='Duration', ascending=False, ignore_index=True)



def top_5():# Tri du DataFrame par 'Duration' et affichage
    df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])
    df_final = df.sort_values(by='Duration', ascending=False, ignore_index=True)
    return list(df_final['Directory'][0:5])

def _24h():
    df_24h = df[df['Entry Time']] <= datetime.datetime.now() - datetime.timedelta(days=1)
    df_24h = df.sort_values(by='Duration', ascending=False, ignore_index=True)
    return df_24h

def _72h():
    df_72h = df[df['Entry Time']] <= datetime.datetime.now() - datetime.timedelta(days=3)
    df_72h = df.sort_values(by='Duration', ascending=False, ignore_index=True)
    return df_72h
    
def semaine():
    df_semaine = df[df['Entry Time']] <= datetime.datetime.now() - datetime.timedelta(days=7)
    df_semaine = df.sort_values(by='Duration', ascending=False, ignore_index=True)
    return df_semaine

def mois(df):
    mois = {
        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04', 
        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08', 
        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
    }
    
    mois_choisi = input('Quel mois analyser ? ').lower()
    
    if mois_choisi in mois:
        # Filtrer le DataFrame pour le mois choisi
        df_mois = df[df['Entry Time'].str.contains(f'-{mois[mois_choisi]}-')]
        
        # Trier le DataFrame filtré par 'Duration'
        df_mois = df_mois.sort_values(by='Duration', ascending=False, ignore_index=True)
        
        return df_mois
    else:
        print("Mois invalide. Veuillez entrer un mois valide.")
        return None

def find_by_program():
    programme=['time_scanner']
    pattern = '|'.join(programme)
    df_programme = df[df['Directory'].str.contains(pattern,case=False, na=False)]
    print(df_programme.sort_values(by='Duration', ascending=False, ignore_index=True))
    return df_programme

def find_directory():
    directory = ['Thunar']
    pattern = '|'.join(directory)
    df_directory = df[df['Directory'].str.contains(pattern,case=False, na=False)]
    print(df_directory.sort_values(by='Duration', ascending=False, ignore_index=True))
    return df_directory


def temps_total_user():
    # Charger les données à chaque appel de la fonction
    df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])
    temps_total = {}
    
    for index, row in df.iterrows():
        user = row['MAC Address']  # Remplacez 'MAC Address' par le nom de la colonne qui identifie l'utilisateur
        temps = row['Duration']
        
        if user not in temps_total:
            temps_total[user] = 0
        
        temps_total[user] += temps

    # Convertir les temps totaux en heures et minutes
    temps_en_heures_minutes = []
    for total in temps_total.values():  # Itérer uniquement sur les valeurs
        heures = total // 3600  # Division entière pour obtenir les heures
        minutes = (total % 3600) // 60  # Reste de la division pour obtenir les minutes
        temps_en_heures_minutes.append(f"{heures}h {minutes}m")  # Ajouter le formatage à la liste

    # Affichage sans guillemets dans la console
    print('Temps total (en heures et minutes) :')
    for temps in temps_en_heures_minutes:
        print(temps)  # Affiche chaque temps

    return temps_en_heures_minutes  # Renvoie la liste des temps formatés



