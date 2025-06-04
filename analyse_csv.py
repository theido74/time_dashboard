import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Lire le fichier CSV
fichier = 'time_board.csv'
df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])
df_tri = df.sort_values(by='Duration', ascending=False, ignore_index=True)


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

    # Créer un dictionnaire pour stocker le temps total par projet et par utilisateur
    temps_par_projet_utilisateur = {}

    # Récupérer les utilisateurs associés aux adresses MAC
    liste_authorite = find_user(fichier_utilisateurs)

    # Parcourir chaque ligne du DataFrame
    for index, row in df.iterrows():
        projet = row['Directory']
        temps = row['Duration']
        mac_address = row['MAC Address']

        # Obtenir le nom de l'utilisateur à partir de l'adresse MAC
        utilisateur = liste_authorite.get(mac_address, "Inconnu")

        # Créer une clé unique pour le projet et l'utilisateur
        key = (projet, utilisateur)
        
        if key not in temps_par_projet_utilisateur:
            temps_par_projet_utilisateur[key] = 0
        temps_par_projet_utilisateur[key] += temps

    # Convertir le dictionnaire en DataFrame
    df_tpp = pd.DataFrame(list(temps_par_projet_utilisateur.items()), columns=['Projet et Utilisateur', 'Temps'])
    df_tpp_final = df_tpp.sort_values(by='Temps', ascending=False, ignore_index=True)
    
    return list(df_tpp_final['Projet et Utilisateur'][0:5])

def top_5():# Tri du DataFrame par 'Duration' et affichage
    df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])
    df_final = df.sort_values(by='Duration', ascending=False, ignore_index=True)
    return list(df_final['Directory'][0:5])


def _24h():
    # Charger le DataFrame à partir du fichier CSV
    fichier = 'time_board.csv'
    df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])   
    
    # Convertir la colonne 'Entry Time' en datetime
    df['Entry Time'] = pd.to_datetime(df['Entry Time'], errors='coerce')
    
    # Filtrer les entrées qui ont eu lieu dans les dernières 24 heures
    df_24h = df[df['Entry Time'] >= datetime.datetime.now() - datetime.timedelta(days=1)]
    
    programme_utilisation = {}
    
    # Calculer le temps total par projet
    for index, row in df_24h.iterrows():
        projet = row['Directory']
        temps = row['Duration']  # Supposons que 'Duration' est en secondes
        if projet not in programme_utilisation:
            programme_utilisation[projet] = 0
        programme_utilisation[projet] += temps
    
    counter = {}

    # Compter le temps d'utilisation pour chaque programme
    for projet, temps in programme_utilisation.items():
        counter[projet] = counter.get(projet, 0) + temps
    
    if counter:
        top5_projet = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Convertir le temps en heures et minutes
        resultats = []
        for projet, total_temps in top5_projet:
            heures = total_temps // 3600  # Conversion en heures
            minutes = (total_temps % 3600) // 60  # Récupération des minutes
            resultats.append(f"{projet}: {heures}h {minutes}m")  # Formatage du résultat
            
        return resultats  # Retourner les projets et leur temps

    return []  # Retourner une liste vide si aucun projet n'est trouvé


def _72h():
    df_72h = df[df['Entry Time']] <= datetime.datetime.now() - datetime.timedelta(days=3)
    df_72h = df.sort_values(by='Duration', ascending=False, ignore_index=True)
    return df_72h
    
def semaine():
    df_semaine = df[df['Entry Time']] <= datetime.datetime.now() - datetime.timedelta(days=7)
    df_semaine = df.sort_values(by='Duration', ascending=False, ignore_index=True)
    return df_semaine


def mois(mois_choisi):
    fichier = 'time_board.csv'
    df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])   
    
    mois_dict = {
        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04', 
        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08', 
        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
    }
    
    if mois_choisi in mois_dict:
        # Filtrer les entrées du mois choisi
        df_mois = df[df['Entry Time'].str.contains(f'-{mois_dict[mois_choisi]}-')]
        df_mois = df_mois.sort_values(by='Duration', ascending=False, ignore_index=True)

        folder_utilisation = {}
        for index, row in df_mois.iterrows():
            projet = row['Directory']
            temps = row['Duration']  # Supposons que 'Duration' est en secondes
            if projet not in folder_utilisation:
                folder_utilisation[projet] = 0
            folder_utilisation[projet] += temps

        # Convertir le temps total en heures et minutes
        resultats = []
        for projet, total_temps in folder_utilisation.items():
            heures = total_temps // 3600  # Conversion en heures
            minutes = (total_temps % 3600) // 60  # Récupération des minutes
            resultats.append({
                'Projet et Utilisateur': projet,
                'Temps': f"{heures}h {minutes}m"  # Formatage du temps
            })

        return resultats  # Retourner les résultats sous forme de liste de dictionnaires

    return []  # Retourner une liste vide si le mois n'est pas trouvé





def find_by_program():
    # Lire le fichier CSV
    df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])

    # Liste des programmes à filtrer
    programmes = ['Visual Studio', 'Mozilla', 'Thunar', 'Telegram']
    pattern = '|'.join(programmes)
    
    # Filtrer le DataFrame pour les programmes spécifiés
    df_programme = df[df['Directory'].str.contains(pattern, case=False, na=False)]
    df_programme = df_programme.sort_values(by='Duration', ascending=False, ignore_index=True)
    
    
    # Dictionnaire pour stocker le temps total par projet
    programme_utilisation = {}
    
    # Calculer le temps total par projet
    for index, row in df_programme.iterrows():
        projet = row['Directory']
        temps = row['Duration']
        programme_utilisation[projet] = programme_utilisation.get(projet, 0) + temps

    # Dictionnaire pour compter le temps d'utilisation pour chaque programme
    counter = {programme: 0 for programme in programmes}
    
    # Compter le temps d'utilisation pour chaque programme
    for projet, temps in programme_utilisation.items():
        for programme in programmes:
            if programme in projet:
                counter[programme] += temps
                break  # Sortir de la boucle une fois le programme trouvé

    # Préparer le résultat pour l'affichage
    result = {}
    for programme, temps in counter.items():
        heures = temps // 3600
        minutes = (temps % 3600) // 60
        result[programme] = f"{heures}h {minutes}m"

    # Création du graphique
    plt.bar(counter.keys(), counter.values(), color=['blue', 'orange', 'green', 'red'])
    plt.xlabel('Programmes')
    plt.ylabel('Temps d\'utilisation (en secondes)')
    plt.title('Temps d\'utilisation des programmes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/fig1.png')
    # Trouver le programme avec le temps d'utilisation le plus élevé
    # if counter:
    #     top_program = max(counter, key=counter.get)
    #     top_time = counter[top_program]
    #     return top_program, top_time  # Retourner le programme et son temps




def find_directory():
    df = pd.read_csv(fichier, header=None, names=['Directory', 'Entry Time', 'Exit Time', 'Duration', 'MAC Address'])
    directory = ['Thunar','Documents', 'Téléchargement','Bureau']
    pattern = '|'.join(directory)
    df_directory = df[df['Directory'].str.contains(pattern,case=False, na=False)]
    df_directory = df_directory.sort_values(by='Duration', ascending=False, ignore_index=True)

    folder_utilisation = {}
    for index, row in df_directory.iterrows():
        projet = row['Directory']
        temps = row['Duration']
        if projet not in folder_utilisation:
            folder_utilisation[projet] = 0
        folder_utilisation[projet] += temps

    counter = {}
    
    # Compter le temps d'utilisation pour chaque programme
    for projet, temps in folder_utilisation.items():
        if projet in counter:
            counter[projet] = counter.get(projet, 0) + temps
        else:
            counter[projet] = temps
    
    if counter:
        top_folder = max(counter, key=counter.get)
        top_time = counter[top_folder]
        return top_folder, top_time  # Retourner le programme et son temps


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

   
    return temps_en_heures_minutes  # Renvoie la liste des temps formatés


print(find_by_program())