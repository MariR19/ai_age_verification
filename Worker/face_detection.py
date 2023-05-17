import numpy as np
import face_recognition as fr
import cv2 as cv


def compare_faces(temp_folder):
    """
Сравнение лиц на фотографии с лицом в паспорте
    :return: True, если найдено совпадение, False - если нет
    """
    try:
        face = cv.imread(temp_folder+'face_cropped.jpg')
        passport = cv.imread(temp_folder+'passport_cropped.jpg')

        faces_enc = fr.face_encodings(face)
        passport_enc = fr.face_encodings(passport)[0]

        # Сравнение лиц с фотографией в паспорте
        for face_enc in faces_enc:
            if fr.compare_faces([face_enc], passport_enc) == np.True_:
                return True
        return False

    except Exception as e:
        print(str(e))
        return None


def process_faces(temp_folder, face, passport):
    faces_cropped = None
    passport_cropped = None
    passport_bottom = None

    try:
        face_faces = fr.face_locations(face)
        passport_faces = fr.face_locations(passport)

        for (top, right, bottom, left) in face_faces:
            faces_cropped = face[top:bottom, left:right]

        for (top, right, bottom, left) in passport_faces:
            passport_cropped = passport[top:bottom, left:right]
            passport_bottom = passport[bottom:, :]

        cv.imwrite(temp_folder+'face_cropped.jpg', faces_cropped)
        cv.imwrite(temp_folder+'passport_cropped.jpg', passport_cropped)
        cv.imwrite(temp_folder+'passport_bottom.jpg', passport_bottom)

        return compare_faces(temp_folder)

    except Exception:
        return None
