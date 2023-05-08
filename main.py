import cv2 as cv

import passport_recognition
import face_detection
import settings


# Загружает фотографии в виде массива numpy
def load_photos():
    face = None
    passport = None
    try:
        face = cv.imread("Source/Pretty_girl.jpg")
        passport = cv.imread("Source/pass_another.jpg")
    finally:
        return face, passport





def main():
    cfg = settings.Settings('settings.ini')
    print(cfg.get('PATH', 'temp_folder'))
    # face, passport = load_photos()
    # if face is None or passport is None:
    #     print("-1\nОшибка загрузки изображений")
    #
    # faces_checked = face_detection.process_faces(face, passport)
    # if faces_checked is None:
    #     print("-2\nОшибка распознавания лиц")
    #     return
    #
    # if faces_checked:
    #     age = passport_recognition.get_age("Source/Temp/passport_bottom.jpg")
    #     if age is None:
    #         print("-3\nОшибка распознавания возраста")
    #     elif age >= 18:
    #         print("0\nПроверка пройдена успешно")
    #     else:
    #         print("1\nПроверка не пройдена - возраст меньше 18")
    # else:
    #     print("2\nПроверка не пройдена - лица не совпадают")


if __name__ == "__main__":
    main()
