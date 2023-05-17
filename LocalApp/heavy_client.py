import cv2 as cv
import os
import time
import shutil

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

    # debug
    shutil.copyfile('../Worker/Source/Test/face_female.jpeg', path['source_face_photo'])
    shutil.copyfile('../Worker/Source/Test/pass_female.jpeg', path['source_passport_photo'])
    if not os.path.exists(path['temp_folder']):
        os.mkdir(path['temp_folder'])
    # debug


    # Загрузка изображений
    face, passport = load_photos(path['source_face_photo'], path['source_passport_photo'])
    if (face is None) or (passport is None):
        print(output['error_loading_images'])
        return

    # запуск анализ изображений
    response = worker.start_job(config, face, passport)

    # Вывод результата
    print(response)

    # debug
    try:
        os.remove(path['source_face_photo'])
        os.remove(path['source_passport_photo'])
        shutil.rmtree(path['temp_folder'])
        print('Файлы удалены')
    except Exception as e:
        print("Ошибка удаления файлов: "+str(e))
    # debug

    # Вывод затраченного времени
    # end_rime = time.time()
    # print(f"Работа выполнена за {end_rime-start_time} секунд")


if __name__ == "__main__":
    main()
