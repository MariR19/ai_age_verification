import numpy as np
import face_recognition as fr
import passport_recognition


def compare_faces(face_img_path, passport_photo_img_path):
    """
Сравнение лиц на фотографии с лицом в паспорте
    :param face_img_path: Путь к фотографии с лицом/лицами покупателя/покупателей
    :param passport_photo_img_path: Путь к фотографии с паспортом
    :return: True, если найдено совпадение, False - если нет
    """
    # Загрузка изображений
    faces_img = fr.load_image_file(face_img_path)
    passport_img = fr.load_image_file(passport_photo_img_path)

    # Получение кодировки изображений
    faces_enc = fr.face_encodings(faces_img)
    passport_enc = fr.face_encodings(passport_img)[0]

    # Сравнение лиц с фотографией в паспорте
    for face_enc in faces_enc:
        if fr.compare_faces([face_enc], passport_enc) == np.True_:
            return True

    return False


def main():
    print(compare_faces("Source/guy1.jpeg", "Source/pass_great.jpeg"))
    print(passport_recognition.check_age("Source/pass_great.jpeg"))


if __name__ == "__main__":
    main()
