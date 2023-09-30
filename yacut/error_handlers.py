from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    """Custom exception class."""
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=400):
        """Initialize the InvalidAPIUsage."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Convert the exception message for response."""
        return {'message': self.message}


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_api_usage(error):
    """Error handler for InvalidAPIUsage."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def handle_page_not_found(error):
    """Error handler for 404."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def handle_internal_error(error):
    """Error handler for 500."""
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
