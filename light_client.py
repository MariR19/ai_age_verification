import socket
import cv2 as cv
import json
import requests
import time

import settings
import encoder


def send_request(url, port, face, face_shape, passport, passport_shape):
    data = {
        'face': face.hex(),
        'passport': passport.hex(),
        'face_shape': face_shape,
        'passport_shape': passport_shape
    }
    data_json = json.dumps(data)
    headers = {'Content-Type': 'application/json'}

    response = requests.post(f'{url}/process', data=data_json, headers=headers)
    return response.json()


# Загружает фотографии в виде массива numpy
def load_photos(face_path, passport_path):
    try:
        face = cv.imread(face_path)
        passport = cv.imread(passport_path)
        return face, passport
    except Exception:
        return None, None


def main():
    start_time = time.time()
    # Извлечение настроек
    config = settings.Settings('settings.ini')
    path = config.get('PATH')
    output = config.get('Output')
    network = config.get('Network')

    # Загрузка изображений
    face, passport = load_photos(path['source_face_photo'], path['source_passport_photo'])
    if (face is None) or (passport is None):
        print(output['error_loading_images'])
        return

    # Шифрование изображений
    cipher_key = network['key'].encode()
    face_encoded = encoder.encode(face, cipher_key)
    passport_encoded = encoder.encode(passport, cipher_key)

    # Отправка запроса на обработку
    url = network['server_url']
    port = int(network['server_port'])
    response = send_request(url, port, face_encoded, face.shape, passport_encoded, passport.shape)

    print(response)
    end_rime = time.time()
    print(f"Работа выполнена за {end_rime-start_time} секунд")


if __name__ == "__main__":
    main()
