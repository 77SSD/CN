import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import threading
import signal
import sys
import ast

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
BUFFER_SIZE = 1024

key = RSA.generate(2048)
public_key = key.publickey().export_key()
private_key = key.export_key()

# Global variable to store the dictionary of client names and public keys
client_public_keys = {}

# Function to encrypt a message using recipient's public key
def encrypt_message(message, recipient_public_key):
    recipient_key = RSA.import_key(recipient_public_key)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    ciphertext = cipher_rsa.encrypt(message.encode())
    return ciphertext

# Function to decrypt a ciphertext using client's private key
def decrypt_message(ciphertext, private_key):
    key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(key)
    message = cipher_rsa.decrypt(ciphertext)
    return message.decode()


def send_data(client_socket):
    client_name = input("Enter your name: ")
    client_socket.send(client_name.encode())
    client_socket.send(public_key)
    prompt_message = "Enter 'quit' to quit the client or 'send' to send a message: "
    while True:
        server_message = client_socket.recv(BUFFER_SIZE).decode()
        if server_message:
            print(server_message)
        op = input(prompt_message)
        client_socket.send(op.encode())
        if op == 'quit':
            print("Disconnecting from the server...")
            client_socket.close()
            sys.exit(0)
        elif op == 'send':
            handle_send_message(client_socket)
            print(client_public_keys)
        else:
            print(f"Invalid option: {op}")


def handle_send_message(client_socket):
    while True:
        print("Available clients:")
        for client_name in client_public_keys:
            print("clients: ", client_name)
        recipient_name = input("Enter the recipient's name (or 'quit' to go back): ")
        if recipient_name == 'quit':
            break
        elif recipient_name in client_public_keys:
            # handle_send_message(client_socket, recipient_name)  # Call function to handle message sending
            recipient_name in client_public_keys:
            message_content = input(f"Enter the message for {recipient_name}: ")
            recipient_public_key = client_public_keys[recipient_name]
            encrypted_message = encrypt_message(message_content, recipient_public_key)
            client_socket.send(f"send{encrypted_message}".encode())  # Send the encrypted message
        else:
            print(f"Recipient {recipient_name} not found.")

def receive_updates(client_socket):
    global client_public_keys  # Access the global dictionary
    while True:
        try:
            server_message = client_socket.recv(BUFFER_SIZE)
            if not server_message:
                break  # No more updates to receive, break out of the loop
            decoded_message = server_message.decode()
            if decoded_message.startswith("{") and decoded_message.endswith("}"):
                client_public_keys = ast.literal_eval(decoded_message)  # Parse the string to dictionary
                print("Updated client dictionary:", client_public_keys)
            else:
                print(decoded_message)  # Print the broadcast message or received message
        except OSError as e:
            print("Error:", e)
            break

def handle_keyboard_interrupt(client_socket):
    print("Disconnecting from the server...")
    client_socket.send(b'keyboard_interrupt')
    client_socket.close()
    sys.exit(0)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Start a thread to send data to the server
    send_thread = threading.Thread(target=send_data, args=(client_socket,))
    send_thread.start()

    # Start a thread to receive updates from the server
    update_thread = threading.Thread(target=receive_updates, args=(client_socket,))
    update_thread.start()

    signal.signal(signal.SIGINT, lambda sig, frame: handle_keyboard_interrupt(client_socket))

    try:
        while True:
            pass
    except KeyboardInterrupt:
        handle_keyboard_interrupt(client_socket)

if __name__ == "__main__":
    main()
