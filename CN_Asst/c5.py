import socket


def main():
    host = '127.0.0.1'
    port = 8080

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    player_name = input("Enter your name: ")
    client.send(player_name.encode())

    try:
        while True:
            player_num_msg = client.recv(1024).decode()
            print(player_num_msg)

            if player_num_msg.startswith("You are in the waiting list."):
                client.close()
                return

            choice = input()
            if choice.upper() == "QUIT":
                client.close()

            client.send(choice.encode())
            winner_status = client.recv(1024).decode()
            print(winner_status)
            continue_game_status = client.recv(1024).decode()
            print(continue_game_status)
            will_continue = input()
            if will_continue == "QUIT":
                break
            if will_continue == "YES":
                client.send(will_continue.encode())
                continue

    except ConnectionAbortedError:
        print("The server closed the connection as there are more players.")

    client.close()


if __name__ == "__main__":
    main()