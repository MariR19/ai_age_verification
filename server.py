import sys
import socket
import threading

# Создание сокета
server_socket = socket.socket()
server_socket.bind(('localhost', 12344))
print("socket bind, waiting for connections\n")
server_socket.listen(1)

exit_flag = False  # Флаг остановки принятия новых соединений


# Обработка консольного ввода
def handle_console():
    # Объявление глобального флага для всех потоков
    global exit_flag
    while True:
        # Ввод команды
        print("Введите команду")
        command = input().lower()
        # Обработка команды
        if command == 'выход':
            print("Ожидание закрытий всех соединений")
            # Флаг для остановки новых соединений
            exit_flag = True
            # Закрытие сокета
            server_socket.close()
            break
        else:
            print("Неизвестная команда")


# Запуск обработки данных
def handle_client(client_socket):
    print("Новое соединение")
    data = client_socket.recv(1024)
    client_socket.send("Server got the message".encode())
    client_socket.close()
    print("Соединение закрыто")


def main():
    # Запуск процесса обработки консольных команд
    console_thread = threading.Thread(target=handle_console)
    console_thread.start()

    # ожидание подключения клиентов, пока сервер не будет остановлен
    while not exit_flag:
        try:
            client_socket, client_address = server_socket.accept()
        except OSError:
            break
        # Запуск обработки клиента
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

    console_thread.join()
    print("Завершение работы")


if __name__ == "__main__":
    main()
