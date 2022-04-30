
import os
import socket
import threading
import sys
from threading import Thread

# List of constants
IP = "localhost"
PORT = 4457 if sys.argv[1] == "" else int(sys.argv[1])
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
BUFFER_SIZE = 4096
# constant with the max size of the cache memory, this value in bytes is equivalent to 64mb
CACHE_MAXSIZE = 67108864

# Cache memory is created as a python dictionary, where the key is the filename and the value is the data of the file
cache = dict()

# Current size of the cache memory
cache_currentsize: int


def handle_client(conn, addr, lock):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        # List of all files inside the server_data directory
        files = os.listdir(SERVER_DATA_PATH)

        if cmd == "list":
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n[FILES INSIDE THE SERVER DIRECTORY]:\n"
                send_data += "\n".join(f for f in files)
                send_data += "\n[FILES IN CACHE]:\n"
                send_data += "\n".join(k for k in cache.keys())

            conn.send(send_data.encode(FORMAT))
            break

        elif cmd == "help":
            data = "OK@"
            data += "[HELP]"
            data += "list: List all the files from the server (on cache and on a server local directory).\n"
            data += "help: List all the commands.\n"
            data += "file: [HOST](default is localhost) [PORT](default is 4457) file [FILENAME] (to request a file from the server).\n"

            conn.send(data.encode(FORMAT))
            break

        elif cmd == "file":
            filename = data[1]
            if filename in files or filename in cache:
                conn.send(("OK@").encode(FORMAT))
                if filename in cache:
                    for data in cache[filename]:
                        conn.send(data)

                    print("file sent from cache")
                    break
                else:
                    lock.acquire()
                    with open(os.path.join(SERVER_DATA_PATH, filename), 'rb') as file:
                        while True:
                            bytes_read = file.read(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            conn.send(bytes_read)
                    print("file sent")

                    with open(os.path.join(SERVER_DATA_PATH, filename), 'rb') as file:
                        data = file.readlines()
                        dataSize = Size(data)

                        cache_currentsize = cacheCurrentSize(cache)

                        keys = []
                        if not dataSize > CACHE_MAXSIZE:
                            while (cache_currentsize+dataSize) > CACHE_MAXSIZE:
                                for k in cache:
                                    keys.append(k)

                                cache_currentsize -= Size(cache[keys[0]])
                                cache.pop(keys[0])
                                keys.pop(0)

                            cache.update({filename: data})

                            print("Adding file to cache")
                    lock.release()
                    break
            else:
                conn.send(("FNF@").encode(FORMAT))
                break

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()


def cacheCurrentSize(cache: dict):
    size = 0
    for key in cache:
        size += Size(cache[key])

    return size


def Size(data):
    size = 0
    for line in data:
        size += line.__sizeof__()

    return size


def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    lock = threading.Semaphore()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(conn, addr, lock))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
