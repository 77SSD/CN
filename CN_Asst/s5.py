import socket
import threading


def handle_client(player_conns):
    addr1, conn1 = player_conns[0]
    addr2, conn2 = player_conns[1]

    try:
        name1 = conn1.recv(1024).decode()
        name2 = conn2.recv(1024).decode()

        while True:
            conn1.send(f"[{name1}], please choose: rock, paper, or scissors: ".encode())
            choice1 = conn1.recv(1024).decode()
            print(f"[{name1}] choice: {choice1}")

            conn2.send(f"{name2}, please choose: rock, paper, or scissors: ".encode())
            choice2 = conn2.recv(1024).decode()
            print(f"[{name2}] choice: {choice2}")

            result = calculate_winner(choice1, choice2)
            print(f"Result: {result}")
            conn1.send(f"Result: {result}".encode())
            conn2.send(f"Result: {result}".encode())

            conn1.send("Do you want to continue? (YES/QUIT)".encode())
            response1 = conn1.recv(1024).decode()

            conn2.send("Do you want to continue? (YES/QUIT)".encode())
            response2 = conn2.recv(1024).decode()

            if response1.upper() == "QUIT" or response2.upper() == "QUIT":
                break
            else:
                continue

    except ConnectionResetError:
        print("Connection reset by peer.")
    finally:
        conn1.close()
        conn2.close()
        return



# Server setup
HOST = '127.0.0.1'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)
print(f"Listening at port {PORT}...")

clients = []
waiting_list = []

while True:
    conn, addr = server.accept()
    if len(clients) < 2:
        clients.append((addr, conn))

    if len(clients) > 2:
        waiting_list.append((addr, conn))
        print("[WARNING] More than 2 clients connected. They are being put in the waiting list.")
        conn.send("You are in the waiting list.".encode())
        conn.close()

    if len(clients) == 2:
        threading.Thread(target=handle_client, args=(clients,)).start()
        clients = []
        continue

    for addr, conn in waiting_list:
        conn.send("You can enroll to play now.".encode())