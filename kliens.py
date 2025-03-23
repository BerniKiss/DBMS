from socket import *

serverName = 'localhost'  
serverPort = 12000        


clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    message = input('Enter message (or "exit" to quit): ')
    
  
    clientSocket.send(message.encode())
    
    if message.lower() == 'exit':
        print('Exiting...')
        break
    
 
    modifiedMessage = clientSocket.recv(1024).decode()
    print('From server:', modifiedMessage)

# Kapcsolat lezárása
clientSocket.close()
