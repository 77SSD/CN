import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import ast

# Global dictionary to store client names and public keys
client_dict = {}

def main():
    # Server details
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 9999

    # Client name and public key
    client_name = input("Enter your name: ")
    public_key = RSA.generate(2048)

    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server")

        # Send client name and public key to server
        client_socket.send(client_name.encode())
        client_socket.send(public_key.public_bytes())

        # Start receiving broadcasted dictionary from server
        recv_dict_thread = threading.Thread(target=receive_dict_broadcast, args=(client_socket,))
        recv_dict_thread.start()

        # Send and receive messages
        while True:
            recipient = input("Enter recipient's name: ")
            message = input("Enter your message: ")

            # Encrypt message with recipient's public key and send to server
            if recipient != client_name and recipient in client_dict:
                cipher = PKCS1_OAEP.new(client_dict[recipient])
                encrypted_message = cipher.encrypt(message.encode())
                client_socket.send(f"{recipient}:{encrypted_message}".encode())
            else:
                print("Recipient not found or invalid.")

            # Receive messages from server
            data = client_socket.recv(1024)
            sender, encrypted_message = data.decode().split(":", 1)
            if sender in client_dict:
                cipher = PKCS1_OAEP.new(public_key)
                decrypted_message = cipher.decrypt(ast.literal_eval(encrypted_message))
                print(f"Received message from {sender}: {decrypted_message.decode()}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def receive_dict_broadcast(client_socket):
    global client_dict
    while True:
        data = client_socket.recv(1024)
        if data:
            client_dict = ast.literal_eval(data.decode())
            print("Updated client dictionary:", client_dict)

if __name__ == "__main__":
    main()
