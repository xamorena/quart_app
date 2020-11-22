from quart import (
    Blueprint,
    render_template,
    make_response,
    current_app,
    request,
    jsonify,
    session,
    copy_current_request_context
)
import uuid
import asyncio
import logging
import json
import time
import markdown
from .extensions import (
    get_page,
    get_cms
)
from .sse import ServerSentEvent


logger = logging.getLogger(__name__)
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


@site_bp.route('/board')
async def site_board():
    context = dict(cms=get_cms())
    session['enabled'] = request.args.get("enabled", True)
    session['user_id'] = str(uuid.uuid4().hex)
    context['page'] = get_page('board.md')
    context['uuid'] = session['user_id']
    return await render_template('board.html', **context)


@site_bp.route('/api/v1.0/message', methods=['POST'])
async def post_message():
    posted = False
    data = await request.form
    for queue in current_app.clients:
        if data is not None:
            data["posted"] = time.asctime().format("YYYY-M-DD hh:mm:ss")
            data["schema"] = "message"
            try:
                md = markdown.Markdown(extensions=["meta", "extra"])
                data["message"] = md.convert(data.get("message", ""))
                data["conveted"] = True
            except Exception as _e:
                data["conveted"] = False
            msg = json.dumps(data)
            await queue.put(msg)
            posted = True
            logger.warning(f"Message posted: {msg}")
    return jsonify(posted)


@site_bp.route('/api/v1.0/dossier', methods=['POST'])
async def post_dossier():
    posted = False
    data = await request.form
    for queue in current_app.clients:
        if data is not None:
            data["posted"] = time.asctime().format("YYYY-M-DD hh:mm:ss")
            data["schema"] = "dossier"
            try:
                files = await request.files
                dossier = dict(url=f"/api/v1.0/dossiers/{data.get('name')}")
                for f in files:
                    dossier[f.name] = f
                data["dossier"] = dossier
                data["uploaded"] = True
            except Exception as _e:
                data["uploaded"] = False
            msg = json.dumps(data)
            await queue.put(msg)
            posted = True
            logger.warning(f"Dossier posted: {msg}")
    return jsonify(posted)


@site_bp.route('/api/v1.0/painter', methods=['POST'])
async def post_painter():
    posted = False
    data = await request.get_json()
    for queue in current_app.clients:
        if data is not None:
            data["posted"] = time.asctime().format("YYYY-M-DD hh:mm:ss")
            data["schema"] = "painter"
            try:
                data["conveted"] = True
            except Exception as _e:
                data["conveted"] = False
            msg = json.dumps(data)
            await queue.put(msg)
            posted = True
            logger.warning(f"Painter posted: {msg}")
    return jsonify(posted)


@site_bp.route('/api/v1.0/dossiers', methods=['GET'])
async def list_dossiers():
    dossiers = []
    return jsonify(dossiers)



@site_bp.route('/api/v1.0/dossiers/<path:filename>', methods=['GET'])
async def find_dossier(filename):
    dossier = dict(url="", file=filename)
    return jsonify(dossier)



@site_bp.route('/api/v1.0/events', methods=['GET'])
async def list_messages():
    queue = asyncio.Queue()
    current_app.clients.add(queue)
    
    async def send_events():
        enabled = True
        while enabled:
            msg = await queue.get()
            if msg is not None:
                event = ServerSentEvent(msg)
                yield event.encode()

    response = await make_response(
        send_events(),
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    response.timeout = None
    return response
