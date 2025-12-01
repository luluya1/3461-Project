import threading
from socket import *

# 1. Create a TCP server socket and bind it to an IP address and port
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket
serverSocket.bind(('',serverPort)) # bind() method associates a server socket with a specific address and port on the local machine

# 2. Start listening for incoming client connections
serverSocket.listen(1) #this line means server listens for the TCP connection req.
print('The server is ready to receive') # printing to confirm that TCP server is up and ready

# 3. Initialize an empty list to store connected clients
connectedClients = []

# 4. while server is running do
    #Accept a new client connection
    #Add the client to the list of active clients
    #Start a new thread to handle communication with that client
    #end while

def background_thread():
    while True:
        sentence = connectionSocket.recv(1024).decode() #receives 'string' from client, and decodes it first

        for c in connectedClients:
            c.send(sentence.encode()) # sends back to the client

        if not sentence:
            print("Server disconnected/Error Occured") # 6. If the server disconnects or an error occurs, close the connection
            break
        print("From Server:", sentence)
    

while True: #always welcoming
    connectionSocket, addr = serverSocket.accept() #When a client knocks on this door, the program invokes the method for serverSocket,
    connectedClients.append(connectionSocket)
    
    thread = threading.Thread(target=background_thread, daemon=True)
    thread.start()
    #which creates a new socket in the server, called , dedicated to this particular client.
    connectionSocket.close() #connection closes 
