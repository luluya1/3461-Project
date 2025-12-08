from socket import *
import threading

serverName = "127.0.0.1"  # or local host
serverPort = 12000        # un-reserved port

# 1. Create a TCP client socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# 2. Connect to the server using the server's IP address and port
clientSocket.connect((serverName, serverPort))  # TCP connection established

# 3. Display the clients local address and port information
local_address, local_port = clientSocket.getsockname()
print(f"Server's local address: {local_address}, Port: {local_port}")

# 4. Input the username from the user and send it to the server
data = clientSocket.recv(1024)          #"Input Username: "
print(data.decode()) #TEST
username = input()
clientSocket.send(username.encode())
errorMsg = data.decode().split().pop(0)      #msg from user. May be an error message, hence...

while(errorMsg == "Error: "):
    username = input()
    clientSocket.send(username.encode())
    
    
print(f"Your username is set to: {username}") #TEST

# 5. Start a background thread to continuously:
     # - Receive incoming messages from the server
     # - Display received messages to the user

def background_thread():
     while True:
        data = clientSocket.recv(1024)

        if not data:
            print("Server disconnected/Error occurred")
            clientSocket.close()

        print(data.decode())


thread = threading.Thread(target=background_thread, daemon=True)
thread.start()

# 6. In the main thread, repeatedly:
     # - Accept user input from the keyboard
     # - To send a priv message, type in the format @username message
     # - Send the message to the server for delivery to the target user
while True:
    message = input("\nInput Message: ")
    clientSocket.send(f"{message}".encode())


clientSocket.close()  # close the socket

