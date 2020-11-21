from __future__ import absolute_import
from quart import Quart
from .site import site_bp

def create_app():
    app = Quart(__name__, static_folder="public")
    app.register_blueprint(site_bp)
    return app

