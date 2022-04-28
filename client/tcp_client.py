
import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4457
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
CLIENT_DATA_PATH = "client_data"
# BUFFER_SIZE = 4096


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        # client.send(cmd.encode(FORMAT))

        if cmd == "help":
            client.send(cmd.encode(FORMAT))
        elif cmd == "logout":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "list":
            client.send(cmd.encode(FORMAT))
        elif cmd == "file":
            filename = data[1]
            send_data = f"{cmd}@{filename}"
            client.send(send_data.encode(FORMAT))

            with open(os.path.join(CLIENT_DATA_PATH, filename), 'wb') as file:
                while True:
                    filedata = client.recv(SIZE)
                    if not filedata:
                        break
                    file.write(filedata)
            print(f"File {filename} received")
            break

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
