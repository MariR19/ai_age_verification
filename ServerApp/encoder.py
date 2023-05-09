from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import numpy as np


# Шифруют данные с использованием ключа AES-128, например, b'0123456789abcdef'
def encode(array, key):
    # Перевод массива в набор байтов
    data = array.tobytes()
    # Создание шифра алгоритмом AES CBC
    cipher = AES.new(key, AES.MODE_CBC)
    # Шифрование данных
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data


# Расшифровывает данные с помощью ключа AES-128 и исходной формы изображения
def decode(encrypted_array, key, shape):
    # Создание шифра
    cipher = AES.new(key, AES.MODE_CBC)
    # Расшифровка данных
    data = unpad(cipher.decrypt(encrypted_array), AES.block_size)
    # Преобразование набора байтов в массив нужного формата
    array = np.frombuffer(data, dtype=np.uint8)
    array = array.reshape(shape)
    return array
