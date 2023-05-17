import cv2 as cv
import time

import settings
from Worker import worker


# Загружает фотографии в виде массива numpy
def load_photos(face_path, passport_path):
    try:
        face = cv.imread(face_path)
        passport = cv.imread(passport_path)
        return face, passport
    except Exception:
        return None, None


def main():
    # start_time = time.time()  # debug - расчет времени работы

    # Извлечение настроек
    config = settings.Settings('settings.ini')
    path = config.get('PATH')
    output = config.get('Output')

    # Загрузка изображений
    face, passport = load_photos(path['source_face_photo'], path['source_passport_photo'])
    if (face is None) or (passport is None):
        print(output['error_loading_images'])
        return

    # запуск анализ изображений
    response = worker.start_job(config, face, passport)

    # Вывод результата
    print(response)

    # Вывод затраченного времени
    # end_rime = time.time()
    # print(f"Работа выполнена за {end_rime-start_time} секунд")


if __name__ == "__main__":
    main()
