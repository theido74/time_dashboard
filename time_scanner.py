import subprocess
import csv
import time
from datetime import datetime
import uuid  

def log_directory_visit(directory, entry_time, exit_time, duration, mac_address):
    with open('/home/leprechaun/Documents/time_scanner/time_board.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([directory, entry_time.strftime('%Y-%m-%d %H:%M:%S'), exit_time.strftime('%Y-%m-%d %H:%M:%S'), duration, mac_address])
        print(f"Visite enregistrée pour {directory} de {entry_time.strftime('%H:%M:%S')} à {exit_time.strftime('%H:%M:%S')} (Durée: {duration} secondes)")

def get_active_window_title():
    try:
        title = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname']).decode('utf-8').strip()
        return title
    except subprocess.CalledProcessError:
        return None

def get_mac_address():
    # Obtenir l'adresse MAC de l'interface réseau
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    return mac

def monitor_directories():
    visited_directories = {}
    mac_address = get_mac_address()  # Récupérer l'adresse MAC au démarrage

    while True:
        window_title = get_active_window_title()
        if window_title:
            directory = window_title  # On prend le titre tel quel
            current_time = datetime.now()

            if directory not in visited_directories:
                visited_directories[directory] = current_time
                print(f"Entrée dans {directory} à {current_time.strftime('%H:%M:%S')}")
            else:
                continue

        for dir in list(visited_directories.keys()):
            if dir != window_title and dir in visited_directories:
                entry_time = visited_directories[dir]
                exit_time = current_time
                duration = int((exit_time - entry_time).total_seconds())
                log_directory_visit(dir, entry_time, exit_time, duration, mac_address)  # Passer l'adresse MAC
                del visited_directories[dir]

        time.sleep(1)

if __name__ == "__main__":
    print("Surveillance des ouvertures de dossiers...")
    monitor_directories()

