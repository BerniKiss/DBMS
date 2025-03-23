import socket
import os
import re
from server_files.database_op import create_database  # Importáljuk a függvényt

# Szerver beállításai
HOST = '127.0.0.1'
PORT = 12345

def parse_command(command):
    """ Felismeri az SQL parancsokat """
    command = command.strip().lower()

    if match := re.match(r'create database (\w+)', command):
        return "create_database", match.group(1)
    else:
        return None, None

def handle_client(client_socket):
    """ Kezeli a kliens által küldött parancsokat """
    with client_socket:
        client_socket.sendall(b"Simple DB Server Ready. Send commands:\n")

        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            if data.lower() == "exit":
                client_socket.sendall(b"Goodbye!\n")
                break

            command_type, argument = parse_command(data)
            if command_type == "create_database":
                status = create_database(argument)
                response = f"Database '{argument}' created successfully!" if status == 0 else f"Database '{argument}' already exists."
            else:
                response = "Invalid command."

            client_socket.sendall(response.encode() + b"\n")

def main():
    """ Indítja a szervert """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server is listening on {HOST}:{PORT}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            handle_client(client_socket)

if __name__ == "__main__":
    main()
