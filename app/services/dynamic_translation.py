from app.extensions import translator
from flask import session, current_app

def translate_text(text):
    target_language = session.get('language', current_app.config['BABEL_DEFAULT_LOCALE'])
    if target_language == 'en':
        return text
    return translator.translate(text, target_language)