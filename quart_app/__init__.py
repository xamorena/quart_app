"""
# Quart-App

Usage: 

```
    quart init_db
    quart run
```
"""
from __future__ import absolute_import
from quart import Quart
import os
from .extensions import get_db_engine
from .site import site_bp
from .user import user_bp
from .auth import auth_bp
from .config import Config
import logging
import click


logger = logging.getLogger(__name__)


def create_app():
    """
    Initialize application:
    
    - extensions
    - blueprints

    """
    app = Quart(__name__, static_folder="public")
    app.config.from_object(Config())
    app.clients = set()
    app.register_blueprint(site_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    @app.cli.command('init_db', with_appcontext=True)
    def init_db():
        try:
            db = get_db_engine()
            with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), mode='r') as file_:
                db.cursor().executescript(file_.read())
            db.commit()
        except Exception as e:
            logger.error(f'init_db error: {e}')

    return app
