import os
from quart import (
    g,
    current_app
)
from sqlite3 import dbapi2 as sqlite3
import markdown
import yaml
import logging


logger = logging.getLogger(__name__)


def get_db_engine():
    current_app.config.setdefault('DATABASE_URL', os.path.join(
        os.path.dirname(__file__), 'appsql.db'))
    engine = sqlite3.connect(current_app.config.get('DATABASE_URL'))
    engine.row_factory = sqlite3.Row
    return engine


def get_cms():
    cms = None
    try:
        with open(os.path.join(os.path.dirname(__file__), "contents", "config.yml"), mode="r") as _f:
            cms = yaml.load(_f, Loader=yaml.FullLoader)
    except Exception as _e:
        logger.warning(f"CMS config file not loaded: {_e}")
        cms = dict(site=dict(title="Quart Application",
                             brand=dict(label="Brand",
                                        image=None),
                             seo=dict(keywords="Quart",
                                      robots="",
                                      description="Python ",
                                      favicon="/static/images/favicon.ico"),
                             theme="default",
                             themes=["default"],
                             styles="<style></style>",
                             scripts="<script></script>",
                             copyright="Company"),
                   menus=dict(main=[],
                              util=[],
                              auth=[],
                              info=[]
                              ))
    finally:
        return cms


def get_db():
    if not hasattr(g, 'db_engine'):
        g.db_engine = get_db_engine()
    return g.db_engine


def get_page(path: str) -> dict:
    page = dict(origin=path, content="")
    try:
        with open(os.path.join(os.path.dirname(__file__), "contents", "pages", path), mode="r") as f:
            md = markdown.Markdown(extensions=['meta'])
            page["source"] = f.read()
            page["content"] = md.convert(page["source"])
            page.update(getattr(md, 'Meta'))
    except Exception as e:
        page["error"] = f"{e}"
    finally:
        return page
