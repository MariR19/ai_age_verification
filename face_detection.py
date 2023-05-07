import numpy as np
import face_recognition as fr
import cv2 as cv


def compare_faces():
    """
Сравнение лиц на фотографии с лицом в паспорте
    :return: True, если найдено совпадение, False - если нет
    """
    face = cv.imread("Source/Temp/face_cropped.jpg")
    passport = cv.imread("Source/Temp/passport_cropped.jpg")

    faces_enc = fr.face_encodings(face)
    passport_enc = fr.face_encodings(passport)[0]

    # Сравнение лиц с фотографией в паспорте
    for face_enc in faces_enc:
        if fr.compare_faces([face_enc], passport_enc) == np.True_:
            return True

    return False


def process_faces(face, passport):
    face_faces = fr.face_locations(face)
    passport_faces = fr.face_locations(passport)

    for (top, right, bottom, left) in face_faces:
        faces_cropped = face[top:bottom, left:right]

    for (top, right, bottom, left) in passport_faces:
        passport_cropped = passport[top:bottom, left:right]
        passport_bottom = passport[bottom:, :]

    cv.imwrite("Source/Temp/face_cropped.jpg", faces_cropped)
    cv.imwrite("Source/Temp/passport_cropped.jpg", passport_cropped)
    cv.imwrite("Source/Temp/passport_bottom.jpg", passport_bottom)

    return compare_faces()
