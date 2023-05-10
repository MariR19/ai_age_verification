# Импорт модулей
from Worker import passport_recognition
from Worker import face_detection


# Основная функция модуля принятия решений
def start_job(cfg, face, passport):

    # Извлечение настроек
    path = cfg.get('PATH')
    text_rec = cfg.get('Text Recognition')
    output = cfg.get('Output')

    # Проверка фотографий на правильность считывания
    if (face is None) or (passport is None):
        return output['error_loading_images']

    # Сравнение лиц
    faces_checked = face_detection.process_faces(path['temp_folder'], face, passport)
    # Обработка ошибок сравнения лиц
    if faces_checked is None:
        return output['error_face_recognition']

    # Если лица совпадают, анализ паспорта
    if faces_checked:
        age = passport_recognition.get_age(text_rec, path['temp_folder'])
        # Обработка результата анализа паспорта
        if age is None:  # Ошибка обработки паспорта
            return output['error_age_extraction']
        elif age >= 18:  # Возраст больше 18
            return output['result_success']
        else:  # Возраст меньше 18
            return output['result_bad_age']
    else: # Если лица не совпадают
        return output['result_bad_faces']