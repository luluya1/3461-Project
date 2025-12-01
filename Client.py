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

# 4. Start a background thread to continuously:
     # - Receive incoming messages from the server
     # - Display received messages to the user

def background_thread():
     while True:
        data = clientSocket.recv(1024)

        if not data:
            print("Server disconnected/Error occurred")
            clientSocket.close()

        print("\nFrom Server:", data.decode())


thread = threading.Thread(target=background_thread, daemon=True)
thread.start()

# 5. In the main thread, repeatedly:
     # - Accept user input from the keyboard
     # - Send the typed message to the server
while True:
    message = input("Input Message: ")
    clientSocket.send(message.encode())


# 6. If the server disconnects or an error occurs, close the connection

clientSocket.close()  # close the socket

