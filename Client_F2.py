from socket import *
import threading

serverName = "127.0.0.1"  # or local host
serverPort = 12000        # un-reserved port

# 1. Create a TCP client socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# 2. Connect to the server using the server's IP address and port
clientSocket.connect((serverName, serverPort))  # TCP connection established

# 3. Wait for the server to request a username
data = clientSocket.recv(1024)
print(data.decode())  # "Enter your username:" prob...

# 4. Input the username from the user and send it to the server
username = input("Username: ")
print(f"Your username is set to: {username}") #TEST
clientSocket.send(username.encode())

# 5. Start a background thread to continuously:
     # - Receive incoming messages from the server
     # - Display received messages to the user

def background_thread():
    while True:
        data = clientSocket.recv(1024)
        if not data:
            print("Server disconnected/Error Occured") # 6. If the server disconnects or an error occurs, close the connection
            break
        print("From Server:", data.decode())


thread = threading.Thread(target=background_thread, daemon=True)
thread.start()

# 6. In the main thread, repeatedly:
     # - Accept user input from the keyboard
     # - To send a priv message, type in the format @username message
     # - Send the message to the server for delivery to the target user
while True:
    message = input("Input Message: ")
    clientSocket.send(f"@{username}|{message}".encode())



# 7. If the server disconnects or an error occurs, close the connection

clientSocket.close()  # close the socket

