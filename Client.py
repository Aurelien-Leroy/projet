import socket
import platform
import subprocess
import time

def get_machine_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"Nom: {hostname}, IP: {ip_address}"
    except Exception as e:
        return f"Erreur lors de la récupération des informations de la machine: {str(e)}"

def scan_network():
    try:
        print("Scan du réseau en cours...")
        result = subprocess.run(["nmap", "192.168.1.1/28"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Erreur lors du scan réseau: {str(e)}"

def start_client(host='127.0.0.1', port=12345):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        machine_info = get_machine_info()
        network_scan = scan_network()
        data = f"{machine_info}\n{network_scan}"

        client_socket.sendall(data.encode())
        response = client_socket.recv(1024).decode()
        print(f"Réponse du serveur: {response}")

        client_socket.close()
    except Exception as e:
        print(f"Erreur de connexion: {str(e)}")

if __name__ == "__main__":
    while True:
        start_client()
        time.sleep(30)
