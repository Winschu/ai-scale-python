import socket

host = '192.168.1.177'  # IP-Adresse des Arduino
port = 80  # Der Port, den der Arduino verwendet

# Socket erstellen
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbindung zum Arduino herstellen
client_socket.connect((host, port))

# Daten senden
message = "Hallo Arduino! Dies ist eine Testnachricht."
client_socket.sendall(message.encode())

# Socket schließen
client_socket.close()
