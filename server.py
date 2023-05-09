import sys
import socket
import threading
import io
import numpy as np

from Worker import worker
import encoder
import settings

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
def handle_client(client_socket, config):
    print("Новое соединение")

    # Прием длинны данных
    face_length = int.from_bytes(client_socket.recv(4), 'big')
    client_socket.send(b'1')
    face_shape_length = int.from_bytes(client_socket.recv(4), 'big')
    client_socket.send(b'1')
    passport_length = int.from_bytes(client_socket.recv(4), 'big')
    client_socket.send(b'1')
    passport_shape_length = int.from_bytes(client_socket.recv(4), 'big')
    client_socket.send(b'1')
    print("Длинна пришла")
    # Прием байтов данных
    face_encoded = client_socket.recv(face_length)
    client_socket.send(b'1')
    face_shape_bytes = client_socket.recv(face_shape_length)
    client_socket.send(b'1')
    print("форма лица пришла")
    passport_encoded = client_socket.recv(passport_length)
    client_socket.send(b'1')
    passport_shape_bytes = client_socket.recv(passport_shape_length)
    client_socket.send(b'1')
    print("форма паспорта пришла")


    print(face_shape_bytes)
    print(face_length)

    # преобразование кортежей
    face_shape = tuple(face_shape_bytes.decode('utf-8'))
    passport_shape = tuple(passport_shape_bytes.decode('utf-8'))

    # Расшифровка данных
    face = encoder.decode(face_encoded, config['Network']['key'], face_shape)
    passport = encoder.decode(passport_encoded, config['Network']['key'],passport_shape)

    # обработка изображений
    response = worker.start_job(config, face, passport)

    # отправка результата
    client_socket.send(response.encode())
    client_socket.close()
    print("Соединение закрыто")


def main():
    config = settings.Settings('settings.ini')

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
        client_thread = threading.Thread(target=handle_client, args=(client_socket,config))
        client_thread.start()

    console_thread.join()
    print("Завершение работы")


if __name__ == "__main__":
    main()
