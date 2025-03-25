import socket

host = '127.0.0.1'  # A szerver IP címe
port = 12345  # A szerver portja

# Kliens létrehozása
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

#uzenet kuldese a szervernejk
while True:
    command = input("Enter command: ")  
    client_socket.sendall(command.encode())  #parancsot elkuldi a szervernek

    #ha exit akkor bezarpm
    if command.lower() == 'exit':
        print("Closing connection...")
        break

    
    response = client_socket.recv(1024)
    print(f"Server response: {response.decode()}")

client_socket.close()  #bezar
