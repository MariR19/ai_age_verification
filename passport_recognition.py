import cv2 as cv
import pytesseract


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


def get_text_from_passport(img_path,
                           resize_coefficient=1.0,
                           use_blur=False,
                           use_morph=False,
                           morph_type=2,
                           kernel_shape=cv.MORPH_RECT,
                           kernel_size=1,
                           psm_mode=6):
    """
    Считывает текст с фотографии паспорта
    :param img_path: Путь к изображению;
    :param resize_coefficient: Коэффициент масштабирования изображения;
    :param use_blur: Использовать размытие;
    :param use_morph: Использовать морфологическое преобразование;
    :param morph_type: Тип морфологического преобразования;
    :param kernel_shape: Форма матрицы ядра для морф. преобразования;
    :param kernel_size: Размер матрицы ядра для морф. преобразования;
    :param psm_mode: Режим страничной сегментации pytesseract
    :return: весь текст, найденный на фотографии
    """

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
    data = pytesseract.image_to_string(image, config=f'-l eng --psm 6 {psm_mode}')
    return data


def check_age(img_path):
    passport_text = get_text_from_passport(img_path)
    return False
