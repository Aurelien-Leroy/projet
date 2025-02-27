import socket
import threading
from flask import Flask, render_template

app = Flask(__name__)

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
        connected_clients_data.append(f"Client {addr}: {data}")
        client_socket.sendall("Message bien reçu".encode())
        client_socket.close()

# Thread pour lancer le serveur en parallèle
def run_server():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

# Route principale pour afficher le tableau de bord
@app.route('/')
def dashboard():
    # On affiche les données reçues des clients
    return render_template('dashboard.html', connected_clients_data=connected_clients_data)

if __name__ == '__main__':
    run_server()  # Démarre le serveur
    app.run(host='127.0.0.1', port=12345)