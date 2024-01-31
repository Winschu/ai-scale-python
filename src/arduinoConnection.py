import socket

# IP-Adresse und Port des Arduino
arduino_ip = '192.168.1.2'  # Beispiel-IP-Adresse, anpassen
arduino_port = 12345  # Beispiel-Port, anpassen

# Socket erstellen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbindung zum Arduino herstellen
server_socket.connect((arduino_ip, arduino_port))

while True:
    # Nachricht vom Arduino empfangen
    message_from_arduino = server_socket.recv(1024)

    # Wenn keine Nachricht mehr empfangen wird, die Schleife beenden
    if not message_from_arduino:
        break

    print("Nachricht vom Arduino:", message_from_arduino.decode())

    # Hier können Sie je nach Nachricht Aktionen durchführen
    if message_from_arduino.decode() == "LED einschalten":
        print("Aktion: LED einschalten")
        # Führen Sie hier den Code für das Einschalten der LED aus

    elif message_from_arduino.decode() == "LED ausschalten":
        print("Aktion: LED ausschalten")
        # Führen Sie hier den Code für das Ausschalten der LED aus

# Socket schließen
server_socket.close()
