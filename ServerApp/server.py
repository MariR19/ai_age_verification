import signal
import threading
from flask import Flask, request, jsonify
import os

from Worker import worker
import encoder
import settings

config = None  # настройки сервера

# Инициализация Flask
app = Flask(__name__)


# Эндпоинт для обработки данных
@app.route('/process', methods=['POST'])
def process():

    print("new connection")

    # получение json с данными
    data = request.get_json()

    # Извлечение данных из json
    face_encoded = bytes.fromhex(data['face'])
    passport_encoded = bytes.fromhex(data['passport'])
    face_shape = tuple(data['face_shape'])
    passport_shape = tuple(data['passport_shape'])

    # извлечение ключа шифрования из настроек
    key = config.get('Network', 'key').encode()

    # Расшифровка данных
    face = encoder.decode(face_encoded, key, face_shape)
    passport = encoder.decode(passport_encoded, key, passport_shape)

    # обработка изображений
    response = worker.start_job(config, face, passport)

    # Возврат json с результатом
    return jsonify(response)


# Обработка консольного ввода
def handle_console():
    while True:
        # Ввод команды
        print("Введите команду")
        command = input().lower()
        # Обработка команды
        if command == 'выход':
            print("Завершение работы")
            # сигнал SIGTERM для текущего процесса
            os.kill(os.getpid(), signal.SIGTERM)
            break
        else:
            print("Неизвестная команда")


# Запуск сервера Flask
def server_run():
    app.run()


if __name__ == "__main__":
    # извлечение настроек
    config = settings.Settings('../settings.ini')

    # запуск потока обработки консольных команд
    console_thread = threading.Thread(target=handle_console)
    console_thread.start()

    # запуск сервера в многопоточном режиме
    server_thread = threading.Thread(target=server_run)
    server_thread.start()

    # ожидание завершения потоков
    console_thread.join()
    server_thread.join()

    print("Server shutdown")

