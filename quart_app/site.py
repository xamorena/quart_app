from quart import (
    Blueprint,
    render_template
)
from .extensions import (
    get_page,
    get_cms
)


site_bp = Blueprint("site", __name__, url_prefix="/")


@site_bp.route('/')
async def site_home():
    context = dict(cms=get_cms())
    context['page'] = get_page('home.md')
    return await render_template('home.html', **context)


@site_bp.route('/pages/<path:slug>')
async def site_page(slug):
    context = dict(cms=get_cms())
    context['page'] = get_page(f'{slug}.md')
    return await render_template('page.html', **context)


@site_bp.route('/privacy')
async def site_privacy():
    context = dict(cms=get_cms())
    context['page'] = get_page('privacy.md')
    return await render_template('page.html', **context)


@site_bp.route('/terms')
async def site_terms():
    context = dict(cms=get_cms())
    context['page'] = get_page('terms.md')
    return await render_template('page.html', **context)
