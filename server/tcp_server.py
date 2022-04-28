
import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4457
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        print(data)
        data = data.split("@")
        print(data)
        cmd = data[0]
        files = os.listdir(SERVER_DATA_PATH)

        if cmd == "list":
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "logout":
            break
        elif cmd == "help":
            data = "OK@"
            data += "list: List all the files from the server.\n"
            data += "logout: Disconnect from the server.\n"
            data += "help: List all the commands."

            conn.send(data.encode(FORMAT))

        elif cmd == "file":
            filename = data[1]
            if filename in files:
                with open(os.path.join(SERVER_DATA_PATH, filename), 'rb') as file:
                    for send_data in file.readlines():
                        conn.send(send_data)
                        print("Sending file")
                    print("file sent")
            else:
                conn.send(("Error@File not found").encode(FORMAT))
        else:
            conn.send("Error@Command invalid".encode(FORMAT))

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()


def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
