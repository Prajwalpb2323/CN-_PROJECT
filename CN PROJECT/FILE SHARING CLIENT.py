import socket
import os
import threading

# Client configuration
server_ip = '192.168.48.234'  # Replace with your server's IP address
server_port = 12345      # Replace with your server's port

def start_client():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((server_ip, server_port))
    print(f"Connected to {server_ip}:{server_port}")
    
    while True:
        # Read user input
        message = input("Enter a message or 'file' to send a file: ")
        
        if message.lower() == 'file':
            # Client wants to send a file
            file_path = input("Enter the path of the file to send: ")
            if not os.path.exists(file_path):
                print("File not found!")
                continue
            
            send_file(client_socket, file_path)
            continue
        
        # Send the message to the server
        client_socket.send(message.encode('utf-8'))
        
        # Check if the user wants to exit
        if message.lower() == 'bye':
            break
        
    # Close the connection
    client_socket.close()


def send_file(client_socket, file_path):
    # Extract the file name from the path
    file_name = os.path.basename(file_path)
    print(f"Sending file: {file_name}")
    
    # Send the file name
    client_socket.send(file_name.encode('utf-8'))
    
    # Determine the file size
    file_size = os.path.getsize(file_path)
    client_socket.send(str(file_size).encode('utf-8'))
    
    # Send the file data in chunks
    sent_bytes = 0
    with open(file_path, 'rb') as file:
        while sent_bytes < file_size:
            # Read data from the file in chunks of 4096 bytes
            chunk = file.read(4096)
            client_socket.send(chunk)
            sent_bytes += len(chunk)
    
    print(f"File sent: {file_name}")
# Start the client
if __name__ == "__main__":
    start_client_thread = threading.Thread(target=start_client)
    start_client_thread.start()
