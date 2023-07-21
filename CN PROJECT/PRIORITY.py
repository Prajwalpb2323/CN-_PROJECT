#sending priority message
import socket

def send_message(priority, message):
    # Client settings
    host = '192.168.48.234'
    port = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        # Send the message with the specified priority
        client.sendall(f"{priority}:{message}".encode())
        print("Message sent successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        client.close()

if __name__ == "__main__":
    while True:
        try:
            priority = int(input("Enter priority (0 - High, 1 - Medium, 2 - Low): "))
            if priority not in [0, 1, 2]:
                print("Invalid priority. Please enter a valid priority.")
                continue
            message = input("Enter your message: ")
            send_message(priority, message)
        except KeyboardInterrupt:
            print("Client shutdown.")
            break
