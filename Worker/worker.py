from Worker import passport_recognition
from Worker import face_detection


def start_job(cfg, face, passport):
    path = cfg.get('PATH')
    text_rec = cfg.get('Text Recognition')
    output = cfg.get('Output')

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