from quart import (
    Blueprint,
    render_template
)
from .extensions import (
    get_page,
    get_cms
)


auth_bp = Blueprint("auth", __name__, url_prefix="/auth/")


@auth_bp.route('/login', methods=["GET", "POST"])
async def auth_login():
    context = dict(cms=get_cms())
    context['page'] = dict(content="")
    return await render_template('auth/login.html', **context)


@auth_bp.route('/register', methods=["GET", "POST"])
async def auth_register():
    context = dict(cms=get_cms())
    context['page'] = dict(content="")
    return await render_template('auth/register.html', **context)
