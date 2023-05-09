import socket


def main():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 12345))
    print("connected\n")

    data = "hello, server"
    client_socket.send(data.encode())
    print("data sent\n")
    responce = client_socket.recv(1024)

    print(responce.decode())
    client_socket.close()


if __name__ == "__main__":
    main()
