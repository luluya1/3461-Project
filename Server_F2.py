from sys import set_coroutine_origin_tracking_depth
import threading
from socket import *


# 1. Create a TCP server socket and bind it to an IP address and port
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) #creating a server side socket
serverSocket.bind(('',serverPort)) # bind() method associates a server socket with a specific address and port on the local machine

# 2. Start listening for incoming client connections
serverSocket.listen(1) #this line means server listens for the TCP connection req.
print('The server is ready to receive') # printing to confirm that TCP server is up and ready

# 3. Initialize an empty dictionary to store connected clients
connectedClients = {}
usernames = []

# 5. Client Handler (in each thread):
    # - Continuously receive messages from the assigned client
    # - For each received message, forward it to all other connected clients
    # - If the client disconnects, close the connection and remove it from the list

def background_thread(connectionSocket, addr):
    while True:
        try:
            sentence = connectionSocket.recv(1024).decode() #receives 'string' from client, and decodes it first
        except ConnectionResetError: #Chekcs if client disccoencted from ctrl C, for example
            print("Client Disconnected!")

            for u in usernames:
                socket = connectedClients.get(u)
                if socket == connectionSocket:
                    connectedClients.pop(u)
                    usernames.remove(u)

            connectionSocket.close() #connection closes 
            break
        
        if not sentence:
            print("Client disconnected/Error Occured")
            for u in usernames:
                socket = connectedClients.get(u)
                if socket == connectionSocket:
                    connectedClients.pop(u)
                    usernames.remove(u)
            connectionSocket.close() #connection closes 
            break


        if(sentence.startswith("@")):
            user = sentence.rsplit("|")
            num = usernames.count(user[0])
            if num >= 1:
                socket = connectedClients.get(user[0])
                socket.send(sentence.encode()) #FIXME
            else:
                s = "Client not found"
                connectionSocket.send(s.encode())
        else:
            s = "Missing @username; please use the correct format"
            connectionSocket.send(s.encode())


        #for c in connectedClients:
        #   c.send(sentence.encode()) # sends back to the client

    connectionSocket.close()

# 4. while server is running do
    #Accept a new client connection
    #Add the client to the list of active clients
    #Start a new thread to handle communication with that client
    #end while
while True: #always welcoming
    connectionSocket, addr = serverSocket.accept() #When a client knocks on this door, the program invokes the method for serverSocket,
    s = "Input username: "
    connectionSocket.send(s.encode())
    username = connectionSocket.recv(1024).decode() #receives 'string' from client, and decodes it first

    connectedClients.update({username: connectionSocket})
    usernames.append(username)
    print(usernames)

    thread = threading.Thread(target=background_thread, args=(connectionSocket, addr), daemon=True)
    thread.start()

