# server.py
import socket

def start_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serveur en attente de connexions sur {host}:{port}...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion reçue de {addr}")
        message = client_socket.recv(1024).decode()
        print(f"Message reçu: {message}")
        client_socket.sendall("Message bien reçu".encode())
        client_socket.close()

if __name__ == "__main__":
    start_server()