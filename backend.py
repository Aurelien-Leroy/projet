import socket
import threading
import json
from datetime import datetime

# Variables globales pour stocker les informations reçues
connected_clients_data = []  # Stocke les infos machines + scan réseau
server_running = False

# Fonction pour démarrer le serveur qui écoute les clients
def start_server(host='127.0.0.1', port=12345):
    global server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_running = True
    print(f"Serveur en attente de connexions sur {host}:{port}...")

    while server_running:
        client_socket, addr = server_socket.accept()
        print(f"Connexion reçue de {addr}")
        data = client_socket.recv(4096).decode()  # On reçoit les infos du client
        
        # Obtenir le nom de la machine à partir de l'adresse IP
        try:
            machine_name = socket.gethostbyaddr(addr[0])[0]
        except socket.herror:
            machine_name = "Nom de machine inconnu"
        
        # Exemple de données reçues (à adapter selon votre format réel)
        client_info = {
            "Utilisateur": machine_name,
            "Nom": machine_name,
            "IP": addr[0],
            "version": "Starting Nmap 7.95 ( https://nmap.org )",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"),
            "Host": data
        }
        
        connected_clients_data.append(client_info)
        client_socket.sendall("Message bien reçu".encode())
        client_socket.close()

# Fonction pour sauvegarder les données dans un fichier JSON
def save_data_to_json(filename='connected_clients_data.json'):
    with open(filename, 'w') as json_file:
        json.dump({"items": connected_clients_data}, json_file, indent=4)
    print(f"Données sauvegardées dans {filename}")

# Thread pour lancer le serveur en parallèle
def run_server():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

if __name__ == '__main__':
    run_server()  # Démarre le serveur
    input("Appuyez sur Entrée pour arrêter le serveur et sauvegarder les données...\n")
    server_running = False
    save_data_to_json()  # Sauvegarde les données avant de quitter
