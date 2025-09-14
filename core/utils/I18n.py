from flask import request, session

from app import app

def set_language(lang_code):
    """手动设置语言，并存储在 Session 中"""
    if lang_code in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang_code

    return True