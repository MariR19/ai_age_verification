import cv2 as cv
import json
import requests
import time

import settings
import encoder


# Отправка запроса
def send_request(url, face, face_shape, passport, passport_shape):
    # Запись данных в json
    data = {
        'face': face.hex(),
        'passport': passport.hex(),
        'face_shape': face_shape,
        'passport_shape': passport_shape
    }
    data_json = json.dumps(data)

    # формирование заголовка для того, чтобы сервер прочитал json
    headers = {'Content-Type': 'application/json'}

    # Отправка запроса
    response = requests.post(f'{url}/process', data=data_json, headers=headers)
    # извлечение json с результатом из полученного ответа

    return response.json()


# Загружает фотографии в виде массива numpy
def load_photos(face_path, passport_path):
    print(face_path)
    try:
        face = cv.imread(face_path)
        passport = cv.imread(passport_path)
        return face, passport
    except Exception:
        return None, None


def main():
    # start_time = time.time()  # debug - расчет времени работы

    # Извлечение настроек
    config = settings.Settings('settings_client.ini')
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
    response = send_request(url, face_encoded, face.shape, passport_encoded, passport.shape)

    # Вывод результата
    print(response)

    # Вывод затраченного времени
    # end_rime = time.time()
    # print(f"Работа выполнена за {end_rime-start_time} секунд")


if __name__ == "__main__":
    main()
