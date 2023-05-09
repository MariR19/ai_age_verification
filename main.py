import cv2 as cv
import numpy as np

import passport_recognition
import face_detection
import settings
import encoder


# Загружает фотографии в виде массива numpy
def load_photos(face_path, passport_path):
    try:
        face = cv.imread(face_path)
        passport = cv.imread(passport_path)
        return face, passport
    except Exception:
        return None, None


def start():
    cfg = settings.Settings('settings.ini')
    path = cfg.get('PATH')
    text_rec = cfg.get('Text Recognition')
    output = cfg.get('Output')

    face, passport = load_photos(path['source_face_photo'], path['source_passport_photo'])

    if (face is None) or (passport is None):
        print(output['error_loading_images'])
        return

    faces_checked = face_detection.process_faces(path['temp_folder'], face, passport)
    if faces_checked is None:
        print(output['error_face_recognition'])
        return

    if faces_checked:
        age = passport_recognition.get_age(text_rec, path['temp_folder'])
        if age is None:
            print(output['error_age_extraction'])
        elif age >= 18:
            print(output['result_success'])
        else:
            print(output['result_bad_age'])
    else:
        print(output['result_bad_faces'])


def main():
    start()



if __name__ == "__main__":
    main()
