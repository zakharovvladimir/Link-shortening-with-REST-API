import random
import string

from flask import flash, redirect, render_template, request

from . import app, db
from .forms import UrlForm
from .models import URLMap


def get_unique_short_id():
    """Generate a unique short ID."""
    while True:
        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View function for the index page."""
    form = UrlForm()
    short_url = ''
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        elif URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('index.html', form=form, short=short_url)
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        db.session.add(url_map)
        db.session.commit()
        short_url = f'{request.base_url}{custom_id}'
    return render_template('index.html', form=form, short_url=short_url)


@app.route('/<string:short>', methods=['GET'])
def url_redirect(short):
    """Redirect the user to the original URL."""
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
