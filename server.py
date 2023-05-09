import socket

def main():
    server_socket = socket.socket()
    server_socket.bind(('localhost', 12345))
    print("socket bind, waiting for connections\n")
    server_socket.listen(1)

    client_socket, client_address = server_socket.accept()
    print(f'got connection from socket {client_socket} with address {client_address}\n')
    data = client_socket.recv(1024)
    print("got data\n")
    response = f"Received:{data.decode()}"
    client_socket.send(response.encode())
    print('response sent')

    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
