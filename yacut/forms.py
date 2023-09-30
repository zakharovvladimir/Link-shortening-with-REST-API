from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

LONG_URL = 'Длинная ссылка'
SHORT_URL = 'Ваш вариант короткой ссылки'
REQUIRED = 'Обязательное поле'
WRONG_URL = 'Ошибка URL'
URL_LEN_EXCEEDED = 'Длина ссылки не должна превышать 6 символов'
WRONG_SHORT_URL = 'Недопустимое имя короткой ссылки'
SHORT_URL_PATTERN = r'^[a-zA-Z0-9_]+$'


class UrlForm(FlaskForm):
    """Form class for URL input."""
    original_link = StringField(LONG_URL, validators=[
        DataRequired(message=REQUIRED),
        URL(require_tld=True, message=WRONG_URL)
    ])

    custom_id = StringField(SHORT_URL, validators=[
        Length(max=6, message=URL_LEN_EXCEEDED),
        Optional(),
        Regexp(SHORT_URL_PATTERN, message=WRONG_SHORT_URL)
    ])
    submit = SubmitField('Create')
