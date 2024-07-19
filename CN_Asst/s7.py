import socket
import threading
import signal

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
BUFFER_SIZE = 2048
clients = {}
client_public_keys = {}
clients_lock = threading.Lock()

def handle_client(client_socket, client_address):
    client_name= ""
    try:
        print(f"New connection from {client_address}")
        client_name = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Client name: {client_name}")
        public_key = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Public key: {public_key}")
        with clients_lock:
            clients[client_name] = client_socket
            client_public_keys[client_name] = public_key
        cli = f"{client_name} connected."
        broadcast(cli.encode())
        broadcast_clients()
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if message == 'quit':
                handle_quit_message(client_name)
                break
            elif message.startswith('send'):
                handle_send_message(client_name, message[4:])
            else:
                # Decrypt the encrypted message received from the client
                decrypted_message = decrypt_message(message, client_name)
                broadcast(f"{client_name}: {decrypted_message}".encode())
                # broadcast(message.encode())
    except ConnectionResetError:
        print(f"Connection reset by {client_name}")
        handle_quit_message(client_name)
    finally:
        if client_name in clients:
            with clients_lock:
                clients.pop(client_name, None)
                client_public_keys.pop(client_name, None)
            # broadcast(f"{client_name} disconnected.".encode())
            broadcast_clients()
        client_socket.close()
        print(f"Connection closed with {client_address}")

def handle_quit_message(client_name):
    if client_name in clients:
        with clients_lock:
            clients.pop(client_name)
            client_public_keys.pop(client_name)
        broadcast_clients()

def handle_send_message(sender_name, message):
    if ':' in message:
        recipient_name, message_content = message.split(':', 1)
        if recipient_name in clients:
            recipient_socket = clients[recipient_name]
            try:
                recipient_socket.sendall(f"{sender_name}: {message_content}".encode())
            except Exception as e:
                print(f"Error sending message to {recipient_name}: {e}")
        else:
            print(f"Recipient {recipient_name} not found.")
    else:
        print(f"Invalid message format from {sender_name}")

def broadcast(message):
    # with clients_lock:
        for client_socket in clients.client
            client_socket.sendall(message)

def broadcast_clients():
    # with clients_lock:
        message = str(client_public_keys)
        for client_socket in clients.values():
            # print(f"msg received":{message})
            # try:
                client_socket.sendall(message.encode())
            # except Exception as e:
                # print(f"Error broadcasting to client: {e}")

def handle_keyboard_interrupt(sig, frame):
    print("Keyboard interrupt received. Shutting down the server...")
    for client_socket in clients.values():
        client_socket.close()
    exit(0)

def main():
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
