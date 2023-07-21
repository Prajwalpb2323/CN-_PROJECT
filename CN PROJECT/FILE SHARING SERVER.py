import socket
import os
import threading

# Server configuration
server_ip = '192.168.48.234'  # Replace with your server's IP address
server_port = 12345    # Replace with your desired server port

def start_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the server IP and port
    server_socket.bind((server_ip, server_port))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")
    
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        
        # Handle the client connection on a new thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def handle_client(client_socket, client_address):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        
        if not data:
            # No data received, client closed the connection
            break
        
        if data.strip().lower() == 'bye':
            # Client wants to exit
            client_socket.send("Goodbye".encode('utf-8'))
            break
        
        if data.strip().lower() == 'file':
            # Client wants to send a file
            receive_file(client_socket)
            continue
        
        # Print the received message
        print(f"Message from {client_address[0]}:{client_address[1]}: {data}")
    
    # Close the client connection
    client_socket.close()

def receive_file(client_socket):
    # Receive the file name
    file_name = client_socket.recv(1024).decode('utf-8')
    print(f"Receiving file: {file_name}")
    
    # Determine the file size
    file_size = int(client_socket.recv(1024).decode('utf-8'))
    
    # Receive and save the file data
    received_bytes = 0
    with open(file_name, 'wb') as file:
        while received_bytes < file_size:
            # Receive data in chunks of 4096 bytes
            chunk = client_socket.recv(4096)
            file.write(chunk)
            received_bytes += len(chunk)
    
    print(f"File received: {file_name}")

if __name__ == "__main__":
    start_server()