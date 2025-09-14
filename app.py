from flask import Flask, request, session
from flask import send_from_directory, render_template
from flask_babel import Babel, gettext as _, get_locale

app = Flask(__name__)

app.template_folder = 'templates'
app.static_folder = 'static'

# 配置 Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'en'  # 默认语言（英语）
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'resources/translations'  # 翻译文件存储目录（默认是 translations）

# 支持的语言列表（可根据需求扩展）
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'zh_CN']

babel = Babel(app)

if __name__ == '__main__':
    app.run(debug=True)
