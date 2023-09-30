import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id

URL_PATTERN = re.compile(r'^[a-z]+://[^\/\?:]+(:[0-9]+)?(\/.*?)?(\?.*)?$')
SHORT_URL_PATTERN = re.compile(r'^[A-Za-z0-9_]{1,6}$')


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    """Retrieve the URLMap object."""
    urlmap = URLMap.query.filter_by(short=short).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify(url=urlmap.original)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Create a short link."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    url = data.get('url')
    custom_id = data.get('custom_id')
    if not url:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not re.match(URL_PATTERN, url):
        raise InvalidAPIUsage('Указан недопустимый URL')

    if not custom_id:
        custom_id = get_unique_short_id()
    else:
        existing_url_map = URLMap.query.filter_by(short=custom_id).first()
        if existing_url_map:
            raise InvalidAPIUsage('Имя "{}" уже занято.'.format(custom_id))
        elif not re.match(SHORT_URL_PATTERN, custom_id):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_map = URLMap()
    url_map.from_dict({'url': url, 'custom_id': custom_id})
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
