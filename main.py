import cv2 as cv

import passport_recognition
import face_detection


# Загружает фотографии в виде массива numpy
def load_photos():
    face = cv.imread("Source/guy3.jpeg")
    passport = cv.imread("Source/pass_great.jpeg")
    return face, passport


def main():
    face, passport = load_photos()
    faces_checked = face_detection.process_faces(face, passport)
    if faces_checked:
        age = passport_recognition.get_age("Source/Temp/passport_bottom.jpg")
        print(age)
    else:
        print("Failed")


if __name__ == "__main__":
    main()
