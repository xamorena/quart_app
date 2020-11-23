import uuid
from quart import (
    Blueprint,
    render_template,
    request,
    session,
    url_for,
    redirect,
    flash,
    g
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
    if request.method == 'POST':
        data = await request.form
        token = data.get("token", None)
        if token == session.get("token") and token is not None:
            user = dict(id=str(uuid.uuid4().hex), name=data.get("username", ""), token=token)
            session["user"] = user
            g.user = user
            redirect_to = request.args.get('redirect', url_for('user.user_board'))
            await flash(f"Welcome {user['name']} logged in")
            return redirect(redirect_to)
        else:
            await flash(f'Bad token {token}.')
    else:
        session['token'] = str(uuid.uuid4().hex)
        context['token'] = session['token']
    return await render_template('auth/login.html', **context)
