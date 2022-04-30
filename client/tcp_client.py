
import socket
import os
import sys

# IP = socket.gethostbyname(socket.gethostname())
# PORT = 4457
IP = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
CLIENT_DATA_PATH = "client_data"
BUFFER_SIZE = 4096


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    data = client.recv(SIZE).decode(FORMAT)
    res, msg = data.split("@")

    if res == "DISCONNECTED":
        print(f"[SERVER]: {msg}")

    elif res == "OK":
        print(f"{msg}")

    # data = input("> ")
    # data = data.split(" ")
    cmd = sys.argv[3]

    if cmd == "help":
        client.send(cmd.encode(FORMAT))
        data = client.recv(SIZE).decode(FORMAT)
        res, msg = data.split("@")
        print(msg)

    elif cmd == "list":
        client.send(cmd.encode(FORMAT))
        data = client.recv(SIZE).decode(FORMAT)
        res, msg = data.split("@")
        print(msg)

    elif cmd == "file":
        filename = sys.argv[4]
        send_data = f"{cmd}@{filename}"
        client.send(send_data.encode(FORMAT))
        asn = client.recv(SIZE).decode(FORMAT)
        if asn == "FNF":
            print("File not found!")
        else:
            with open(os.path.join(CLIENT_DATA_PATH, filename), 'wb') as file:
                while True:
                    filedata = client.recv(BUFFER_SIZE)
                    if not filedata:
                        break
                    file.write(filedata)
            print(f"File {filename} received")

    else:
        print("[ERROR - invalid command]")

    client.close()
    print("[Disconnected from the server.]")


if __name__ == "__main__":
    main()
