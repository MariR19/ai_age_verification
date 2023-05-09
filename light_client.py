import socket
import cv2 as cv

import settings
import encoder


def send_request(url, port, face, face_shape, passport, passport_shape):
    client_socket = socket.socket()
    client_socket.connect((url, port))
    print("connected\n")

    print(face_shape)
    print(client_socket.send(len(face_shape).to_bytes(4, 'big')))

    # отправка длинны данных
    client_socket.send(len(face).to_bytes(4, 'big'))
    client_socket.recv(1)
    client_socket.send(len(face_shape).to_bytes(4, 'big'))
    client_socket.recv(1)
    client_socket.send(len(passport).to_bytes(4, 'big'))
    client_socket.recv(1)
    client_socket.send(len(passport_shape).to_bytes(4, 'big'))
    client_socket.recv(1)

    # Отправка данных
    client_socket.send(face)
    client_socket.recv(1)
    client_socket.send(face_shape)
    client_socket.recv(1)
    client_socket.send(passport)
    client_socket.recv(1)
    client_socket.send(passport_shape)
    client_socket.recv(1)

    print("data sent\n")
    response = client_socket.recv(1024)
    client_socket.close()

    return response.decode()


# Загружает фотографии в виде массива numpy
def load_photos(face_path, passport_path):
    print(face_path)
    print(passport_path)
    try:
        face = cv.imread(face_path)
        passport = cv.imread(passport_path)
        return face, passport
    except Exception:
        return None, None


def main():
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
    response = send_request(url, port, face_encoded, str(face.shape).encode('utf-8'),
                            passport_encoded, str(passport.shape).encode('utf-8'))

    print(response)


if __name__ == "__main__":
    main()
