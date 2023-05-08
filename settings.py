import configparser as cfg
import os.path


class Settings:

    _settings_file_path = None
    _config = None

    def __init__(self, settings_file_path):
        self._settings_file_path = settings_file_path

        settings = self._export_settings()
        if settings is None:
            settings = self._create_settings()
        self._config = settings

    def _create_settings(self):
        config = cfg.ConfigParser()
        config['PATH'] = {'source_face_photo': 'Source/face.jpg',
                          'source_passport_photo': 'Source/passport.jpg',
                          'temp_folder': 'source/Temp/'}

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

        with open(self._settings_file_path, 'w') as file:
            config.write(file)

        return config

    def _export_settings(self):
        if os.path.exists(self._settings_file_path):
            config = cfg.ConfigParser()
            config.read(self._settings_file_path)
            return config
        else:
            return None

    def get(self, cat, prop='all'):
        if prop == 'all':
            return self._config[cat]
        else:
            return self._config[cat][prop]


