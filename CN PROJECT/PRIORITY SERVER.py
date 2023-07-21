#sending priority message


import socket
import threading
import queue

def handle_client(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Assuming the message format is "priority:message"
            priority, message = data.decode().split(':', 1)

            # Process the message based on priority
            if priority == '0':
                print("[High Priority] ", message)
            elif priority == '1':
                print("[Medium Priority] ", message)
            elif priority == '2':
                print("[Low Priority] ", message)
            else:
                print("Invalid priority format!")

        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()

def main():
    # Server settings
    host = '127.0.0.1'
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print("Server listening on {}:{}".format(host, port))

    while True:
        try:
            client_socket, addr = server.accept()
            print("Accepted connection from {}:{}".format(addr[0], addr[1]))

            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        except KeyboardInterrupt:
            print("Server shutdown.")
            break

if __name__ == "__main__":
    main()
