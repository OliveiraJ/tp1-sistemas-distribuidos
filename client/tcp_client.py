import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4457
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


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

        if cmd == "help":
            client.send(cmd.encode(FORMAT))
        elif cmd == "logout":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "list":
            client.send(cmd.encode(FORMAT))

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
