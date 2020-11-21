from quart import (
    Blueprint,
    render_template
)


site_bp = Blueprint("site", __name__, url_prefix="/")

def get_cms():
    return dict(site=dict(title="Quart Application", 
                          seo=dict(keywords="Quart",
                                   robots="",
                                   description="Python ", 
                                   favicon="/static/favicon.ico"), 
                          theme="default", 
                          themes=["default"], 
                          styles="<style></style>", 
                          scripts="<script></script>"))


@site_bp.route('/')
async def site_home():
    context = dict(cms=get_cms())
    return await render_template('home.html', **context)
