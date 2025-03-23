import socket

host = '127.0.0.1'  # A szerver IP címe
port = 12345  # A szerver portja

# Kliens létrehozása
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Üzenet küldése a szervernek
while True:
    command = input("Enter command: ")  # Parancs beírása
    client_socket.sendall(command.encode())  # Parancs elküldése a szervernek

    # Ha a parancs 'exit', akkor zárjuk be a kapcsolatot
    if command.lower() == 'exit':
        print("Closing connection...")
        break

    # Válasz fogadása a szervertől
    response = client_socket.recv(1024)
    print(f"Server response: {response.decode()}")

client_socket.close()  # Kliens bezárása
