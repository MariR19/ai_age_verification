import signal
import threading
from flask import Flask, request, jsonify
import os

from Worker import worker
import encoder
import settings

config = None

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process():
    print("new connection")

    data = request.get_json()

    face_encoded = bytes.fromhex(data['face'])
    passport_encoded = bytes.fromhex(data['passport'])
    face_shape = tuple(data['face_shape'])
    passport_shape = tuple(data['passport_shape'])

    key = config.get('Network', 'key').encode()
    face = encoder.decode(face_encoded, key, face_shape)
    passport = encoder.decode(passport_encoded, key, passport_shape)

    # обработка изображений
    response = worker.start_job(config, face, passport)

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
            # Флаг для остановки новых соединений
            os.kill(os.getpid(), signal.SIGTERM)
            break
        else:
            print("Неизвестная команда")


def server_run():
    app.run()


if __name__ == "__main__":
    config = settings.Settings('settings.ini')

    console_thread = threading.Thread(target=handle_console)
    console_thread.start()

    server_thread = threading.Thread(target=server_run)
    server_thread.start()

    console_thread.join()
    server_thread.join()
    print("Server shutdown")

