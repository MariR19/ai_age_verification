import configparser as cfg
import os.path


# Класс сериализации настроек приложения
class Settings:
    _settings_file_path = None  # Путь к файлу настрое
    _config = None  # Объект настроек

    # Конструктор класса, заполняет переменные класса
    def __init__(self, settings_file_path):
        # заполнение переменной класса пути к файлу настроек
        self._settings_file_path = settings_file_path

        # Экспорт настроек
        settings = self._export_settings()
        # Если экспорт не удался, создание нового файла настроек
        if settings is None:
            settings = self._create_settings()
        # заполнение переменной класса объекта настроек
        self._config = settings

    # Внутренний метод создания файла настроек
    def _create_settings(self):
        # Создание объекта класса ConfigParser
        config = cfg.ConfigParser()

        # Определение стандартных настроек
        config['PATH'] = {'source_face_photo': 'Worker/Source/face.jpg',
                          'source_passport_photo': 'Worker/Source/passport.jpg',
                          'temp_folder': 'Worker/source/Temp/'}

        config['Text Recognition'] = {'resize_coefficient': '1.0',
                                      'use_blur': 'False',
                                      'use_morphological_function': "False",
                                      'morphological_function_type': '2',
                                      'kernel_matrix_shape': '0',
                                      'kernel_matrix_size': '1',
                                      'ocr_psm_mode': '6'}
        config['Output'] = {'error_loading_images': "-1\nОшибка загрузки изображений",
                            'error_face_recognition': "-2\nОшибка распознавания лиц",
                            'error_age_extraction': "-3\nОшибка распознавания возраста",
                            'result_success': "0\nПроверка пройдена успешно",
                            'result_bad_age': "1\nПроверка не пройдена - возраст меньше 18",
                            'result_bad_faces': "2\nПроверка не пройдена - лица не совпадают"}

        # Запись файла настроек
        with open(self._settings_file_path, 'w') as file:
            config.write(file)

        return config

    # Внутренний метод экспорта настроек
    def _export_settings(self):
        # Если файл существует, чтение настроек
        if os.path.exists(self._settings_file_path):
            config = cfg.ConfigParser()
            config.read(self._settings_file_path)
            return config
        else:
            return None

    def get(self, cat, prop='all'):
        """
        Открытый метод получения настроек
        :param cat: Категория настроек
        :param prop: Конкретная настройка
        :return: Строка с настройкой, если указана в параметрах
                 иначе словарь всех настроек категории
        """
        if prop == 'all':
            return self._config[cat]
        else:
            return self._config[cat][prop]
