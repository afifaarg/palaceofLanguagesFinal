import json
from django.conf import settings
import os

def load_translations(language_code):
    translations_dir = os.path.join(settings.BASE_DIR, 'core/translations')
    print('hellooo herrree', translations_dir)
    file_path = os.path.join(translations_dir, f'{language_code}.json')
    
    try:
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  

def translate(text, language_code):
    print(text, language_code)
    translations = load_translations(language_code)
    return translations.get(text, text)  
    
def translations(request):
    language_code = request.LANGUAGE_CODE 

    translations = load_translations(language_code)

    return {'translations': translations}