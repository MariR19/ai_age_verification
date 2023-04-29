import cv2
import numpy as np
import cv2 as cv
from pathlib import Path


# Отобразить изображение на экране
def show_photo(window_name, img):
    cv.imshow(window_name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


# Загрузить изображение
def load_photo(file_name):
    loading_photo = cv.imread(str(source_folder/file_name))
    loading_photo = cv2.cvtColor(loading_photo, cv2.COLOR_BGR2GRAY)
    return loading_photo


# Папка с исходными изображениями
source_folder = Path("Source")

# Натренированный классификатор лиц Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Чтение файла
photo = load_photo("Passport.jpg")

# Распознавание лица
faces = face_cascade.detectMultiScale(photo, scaleFactor=1.1, minNeighbors=5)

# Нарисовать прямоугольник вокруг лица
for (x, y, w, h) in faces:
    cv2.rectangle(photo, (x, y), (x+w, y+h), (255, 0, 0), 2)

show_photo("Face", photo)

