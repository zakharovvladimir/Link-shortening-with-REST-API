from datetime import datetime

from flask import url_for

from . import db


class URLMap(db.Model):
    """Model for storing URL map."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(64), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Convert the URLMap to response."""
        return {
            'url': self.original,
            'short_link': url_for('url_redirect', short=self.short, _external=True)
        }

    def from_dict(self, data):
        """Get the URLMap from response dictionary."""
        self.original = data['url']
        self.short = data['custom_id']
