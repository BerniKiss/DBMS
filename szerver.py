from socket import *


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)


serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


serverSocket.bind(('', serverPort))


serverSocket.listen(1)
print('The server is ready to receive')

while True:

    connectionSocket, addr = serverSocket.accept()
    

    sentence = connectionSocket.recv(1024).decode()
    
    if sentence.lower() == 'exit':  
        print('CLOSING SERVER...')
        connectionSocket.send('Server is shutting down'.encode()) 
        connectionSocket.close()
        break
    
  
    capitalizedSentence = sentence.upper()

    connectionSocket.send(sentence.encode())
    
   
    #connectionSocket.close()
