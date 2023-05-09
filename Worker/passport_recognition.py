import cv2 as cv
import pytesseract

from datetime import datetime
from dateutil.relativedelta import relativedelta


# Отобразить изображение на экране
def show_image_cv(cv_image):
    cv.imshow("window", cv_image)
    cv.waitKey(0)
    cv.destroyAllWindows()


# функция преобразования размера изображения
def resize_image(img, coefficient):
    height, width = img.shape[:2]
    new_image = cv.resize(img, (int(height * coefficient), int(width * coefficient)))
    return new_image


def get_text_from_passport(config, img_path):
    """
    Считывает текст с фотографии паспорта
    :param config: Словарь настроек
    :param img_path: Путь к изображению;
    :return: весь текст, найденный на фотографии
    """
    try:
        resize_coefficient = float(config['resize_coefficient'])
        use_blur = bool(config['use_blur'])
        use_morph = bool(config['use_morphological_function'])
        morph_type = int(config['morphological_function_type'])
        kernel_shape = int(config['kernel_matrix_shape'])
        kernel_size = int(config['kernel_matrix_size'])
        psm_mode = int(config['ocr_psm_mode'])

        image = cv.imread(img_path)

        if resize_coefficient != 1.0:
            image = resize_image(image, resize_coefficient)

        # преобразование в оттенки серого
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # небольшой блюр для уменьшения шума
        if use_blur:
            image = cv.GaussianBlur(image, (3, 3), 0)

        # преобразование цвета в бинарный на основе алгоритма OTSU
        image = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

        # Морфологическое преобразования
        if use_morph:
            kernel = cv.getStructuringElement(kernel_shape, (kernel_size, kernel_size))
            image = cv.morphologyEx(image, morph_type, kernel)

        # Извлечение текста
        data = pytesseract.image_to_string(image, config=f'-l eng --psm {psm_mode}')
        return data
    except Exception:
        return None


# Распознает дату рождения из текста паспорта и высчитывает возраст
def extract_age(text):
    mrz_start = "pn"  # начало МЧЗ
    birthdate_start = "rus"  # начало строки с датой рождения

    # преобразование исходного текста
    text = text.lower().replace(' ', '').replace('o', '0')
    text = text.split('\n')

    text_len = len(text)  # длина листа строк
    line = -1  # текущая строка текста
    age = None  # возраст

    # поиск МЧЗ
    for i in range(len(text)):
        if text[i].find(mrz_start) > -1:
            line = i
            break

    # если line остался -1, МЧЗ не найдена
    if line == -1:
        return age

    try:
        # определение даты рождения
        index = text[line+1].find(birthdate_start)+3
        birthday_str = text[line+1][index:index+6]
        # преобразование строки в datetime
        birthday = datetime.strptime(birthday_str, "%y%m%d")
        # расчет возраста
        age = relativedelta(datetime.now(), birthday).years
    finally:
        return age


# принимает фото паспорта (МЧЗ паспорта) и возвращает возраст владельца
def get_age(text_rec_cfg, temp_folder):
    passport_text = get_text_from_passport(text_rec_cfg, temp_folder+'passport_bottom.jpg')
    age = None
    if passport_text is not None:
        age = extract_age(passport_text)
    return age
