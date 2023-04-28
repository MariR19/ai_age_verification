import numpy as np
import cv2 as cv
from pathlib import Path


# Отобразить изображение на экране
def show_photo(window_name, img):
    cv.imshow(window_name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


# Папка с исходными изображениями
source_folder = Path("Source")

# Чтение файла
dude_photo = cv.imread(str(source_folder/"photo-dude.jpg"))

show_photo("dude", dude_photo)
